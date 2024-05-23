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

# Run the bot with the token
bot.run('MY_TOKEN')
