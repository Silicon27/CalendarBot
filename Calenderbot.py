import discord
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext

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
async def give_role(ctx, member: discord.Member, role: discord.Role):
    if ctx.guild.me.guild_permissions.manage_roles:
        await member.add_role(role)
        await ctx.send(f'Successfully given {role.name} to {member.display_name}')
    else:
        await ctx.send("Permission was denied")

@slash.slash(name="remove_role", description="Remove a role from someone")
async def removerole(ctx, member: discord.Member, role: discord.Role):
    # Check if the bot has permission to manage roles
    if ctx.guild.me.guild_permissions.manage_roles:
        await member.remove_roles(role)
        await ctx.send(f'Successfully removed {role.name} from {member.display_name}')
    else:
        await ctx.send('I do not have permission to manage roles.')

# Run the bot with the token
bot.run('BOT_TOKEN')
