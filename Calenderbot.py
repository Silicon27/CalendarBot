import discord
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext, SelectMenu, SelectOption


# Initialize the bot with a command prefix
bot = commands.Bot(command_prefix="!")
slash = SlashCommand(bot, sync_commands=True)  # Creating a SlashCommand instance

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

# Define a command
@bot.command()
async def hello(ctx):
    await ctx.send('Hello!')

@slash.slash(name="ping", description="Check the bot's latency")
async def ping(ctx: SlashContext):  # Use SlashContext instead of discord.Interaction
    latency = bot.latency * 1000  # Convert latency to milliseconds
    print(f'{ctx.author.name} requested ping from {ctx.guild.name} -----  [User: {ctx.author.id}]  <-->  [Server: {ctx.guild.id}]  <--> [Channel: {ctx.channel.id}]')

    await ctx.send(f'Pong! Latency: {latency:.2f} ms')

@slash.slash(name="server_details", description="Check the server details")
async def server_details(ctx: SlashContext):
    await ctx.send(f'[Server Name: {ctx.guild.name}   <>   Server ID: {ctx.guild.id}] ----  [User: {ctx.author.id}]  ')

@slash.slash(name="give_role", description="Give a role to someone")
async def assign_roles(ctx: SlashContext):
    guild = ctx.guild
    roles = guild.roles[1:]  # Exclude @everyone role
    options = [SelectOption(role.name, str(role.id)) for role in roles]

    select_menu = SelectMenu(
        custom_id="role_menu",
        placeholder="Select roles",
        options=options,
        max_values=len(roles),  # Set maximum number of roles user can select
        min_values=1            # Set minimum number of roles user must select
    )
    await ctx.send("Select the roles you want to assign:", components=[select_menu])

@bot.component("role_menu")
async def role_menu_handler(ctx: SlashContext, values: list):
    member = ctx.author
    guild = ctx.guild
    for role_id in values:
        role = discord.utils.get(guild.roles, id=int(role_id))
        if role:
            await member.add_roles(role)
            await ctx.send(f"Role {role.name} assigned to {member.display_name}")
        else:
            await ctx.send(f"Role with ID {role_id} not found")

@slash.slash(name="remove_role", description="Remove a role from yourself")
async def remove_role(ctx: SlashContext):
    member = ctx.author
    roles = member.roles[1:]  # Exclude @everyone role
    options = [SelectOption(role.name, str(role.id)) for role in roles]

    select_menu = SelectMenu(
        custom_id="remove_role_menu",
        placeholder="Select roles to remove",
        options=options,
        max_values=len(roles),  # Set maximum number of roles user can select
        min_values=1            # Set minimum number of roles user must select
    )
    await ctx.send("Select the roles you want to remove:", components=[select_menu])

@bot.component("remove_role_menu")
async def remove_role_menu_handler(ctx: SlashContext, values: list):
    member = ctx.author
    guild = ctx.guild
    for role_id in values:
        role = discord.utils.get(guild.roles, id=int(role_id))
        if role:
            await member.remove_roles(role)
            await ctx.send(f"Role {role.name} removed from {member.display_name}")
        else:
            await ctx.send(f"Role with ID {role_id} not found")

@slash.slash(name="create_notification", description="Make a notification for a set time", options=[
                SelectOption("January", "january"),
                SelectOption("February", "february"),
                SelectOption("March", "march"),
                SelectOption("April", "april"),
                SelectOption("May", "may"),
                SelectOption("June", "june"),
                SelectOption("July", "july"),
                SelectOption("August", "august"),
                SelectOption("September", "september"),
                SelectOption("October", "october"),
                SelectOption("November", "november"),
                SelectOption("December", "december")
            ])
async def createNotification(ctx, value: str):
    await ctx.send(f"You selected: {value}")


# Run the bot with the token
bot.run('BOT_TOKEN')
