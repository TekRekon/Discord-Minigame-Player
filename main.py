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
async def on_member_update(x, y):
    server = client.get_server(id="477829362771689484")
    DJ = discord.utils.get(server.roles, name="DJ")
    mod_roles = [discord.utils.get(server.roles, name="DJ"), "GetsNotifs", "getsAds", "GameNotifs"]
    await client.send_message(destination="514591632327442432", content="I detected a member update")
    role_list = y.roles
    Moderator = False
    for i in range(len(role_list)):
        if role_list[i] == "Moderator":
            Moderator = True
            await client.send_message(destination="514591632327442432",
                                      content="I detected a member update to role Moderator")
            await client.add_roles(y, mod_roles)
            await client.add_roles(y, DJ)
    else:
        await client.send_message(destination="514591632327442432",
                                  content="I detected a member update that did not include role Moderator")

    await client.send_message(destination="514591632327442432", content="worked")




client.run("NTEzODMyNzk3NjM5NTQwNzM5.D12Yzw.dUzzYz2y5k886Azzll2QPqMLeiM")
