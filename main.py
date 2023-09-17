import discord
from discord.ext import commands

token = ''

intents = discord.Intents.all()
client = commands.Bot(command_prefix='!', intents=intents)

@client.event
async def on_ready():
    print("Bot is online :)")

@client.command()
async def ping(ctx):
    await ctx.send("ping")

@client.command()
async def addition(ctx, num1, num2):
    sum = int(num1) + int(num2)
    await ctx.send(sum)

client.run(token)