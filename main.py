import discord
from discord.ext import commands

client = commands.Bot(command_prefix='.')

@client.event
async def on_ready():
    print("I am ready")
    await client.change_presence(game=discord.Game(name="CorruptReaktor.py"), status=None, afk=False)


@client.event
async def on_message(message):
    await client.add_reaction(message, "⏬")
    await client.add_reaction(message, emoji="⭐")
    await client.add_reaction(message, emoji="⏫")

@client.event
async def on_member_update():
    if discord.Member.display_name == "TekRekon":
        await client.send_message(destination="514591632327442432", content="worked")

client.run("NTEzODMyNzk3NjM5NTQwNzM5.D12Yzw.dUzzYz2y5k886Azzll2QPqMLeiM")
