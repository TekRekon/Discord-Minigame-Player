import discord
from discord.ext import commands

client = commands.Bot(command_prefix='.')

TOKEN = open("secret.txt", "r")

@client.event
async def on_ready():
    print("I am ready")
    await client.change_presence(game=discord.Game(name="CorruptReaktor.py"), status=None, afk=False)


@client.event
async def on_message(message):
    await client.add_reaction(message, emoji="⏫")
    await client.add_reaction(message, "⏬")
    await client.add_reaction(message, emoji="⭐")

client.run(TOKEN.read())
