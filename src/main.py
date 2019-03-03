import discord
from discord.ext import commands

client = commands.Bot(command_prefix='.')

TOKEN = open("secret.txt", "r")

game = "CorruptReaktor"


@client.event
async def on_ready():
    print("I am ready")
    await client.change_presence(game=discord.Game(name="CorruptReaktor.py"), status=None, afk=False)


client.run(TOKEN.read())
