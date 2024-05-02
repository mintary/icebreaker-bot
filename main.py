import asyncio
import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv() 

intents = discord.Intents.all()
intents.members = True

class Bot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix='/', intents=discord.Intents.all(), help_command=commands.DefaultHelpCommand())

        self.extension_list = []
    
    async def on_ready(self):
        print(f'{bot.user.name} has connected to Discord :)')
        synced = await self.tree.sync()
        print(f"Synced {len(synced)} command(s).")
        await bot.change_presence(activity=discord.Game(name='Icebreaker bot | WIP'))
    
    @commands.command(name="hello", description="Says hello to bot, testing if it is responding to commands.")
    async def hello(self, ctx):
        await ctx.send(f'Hello there, {ctx.author}!')

    async def setup_hook(self):
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                try:
                    await bot.load_extension(f'cogs.{filename[:-3]}')
                    print(f'Loaded cog for {filename[:-3]} successfully.')
                except:
                    print(f"Couldn't load cog for {filename[:-3]} successfully, or no commands were added from that class.")

bot = Bot()

bot.run(os.getenv('TOKEN'))