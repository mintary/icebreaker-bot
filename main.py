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
async def on_ready():
    print(f'{bot.user.name} has connected to discord :)')
    await bot.change_presence( activity=discord.Game(
        name='tort bot | wip'
        ))

@bot.command(name='hello')
async def hello(ctx):
    await ctx.send(f'hello there, {ctx.author}')

@bot.command(name='shutdown')
async def shutdown(ctx):
    await ctx.bot.close()
    print('goodbye')

async def load_cogs(): 
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            try:
                await bot.load_extension(f'cogs.{filename[:-3]}')
                print(f'Loaded cog for {filename[:-3]} successfully.')
            except:
                print(f"Couldn't load cog for {filename[:-3]} successfully.")

async def main():
    async with bot:
        await load_cogs()
        await bot.start(os.getenv('TOKEN'))

asyncio.run(main())