import asyncio
import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv() 

intents = discord.Intents.all()
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents) 

@bot.event
async def on_ready(): # Triggers when bot has connected to Discord
    print(f'{bot.user.name} has connected to discord :)')
    await bot.change_presence( activity=discord.Game(
        name='tort bot | wip'
        )) # Sets "game bot is playing" to 'tort bot | wip'

@bot.command(name='hello') # Test command to make sure bot is responding to commands
async def hello(ctx):
    await ctx.send(f'hello there, {ctx.author}')

async def load_cogs(): # Load all commands stored in cogs (found in the cogs folder)
    for filename in os.listdir('./cogs'): # cogs folder
        if filename.endswith('.py'): 
            try:
                await bot.load_extension(f'cogs.{filename[:-3]}')
                print(f'Loaded cog for {filename[:-3]} successfully.')
            except:
                print(f"Couldn't load cog for {filename[:-3]} successfully, or no commands were added from that class.")

async def main():
    async with bot:
        await load_cogs()
        await bot.start(os.getenv('TOKEN')) # Get stored token in .env file

asyncio.run(main())