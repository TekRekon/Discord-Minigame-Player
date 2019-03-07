import discord
from discord.ext import commands

client = commands.Bot(command_prefix='.')

class hi():
    just_started = True
    prev_author = "something"

#####STARTUP
@client.event
async def on_ready():
    print("I am ready")
    await client.change_presence(game=discord.Game(name="CorruptReaktor.py"), status=None, afk=False)
    hi.just_started = True


@client.event
async def on_message(message):
    #####VARIABLES
    bot_testing_commands_channel = discord.utils.get(message.server.channels, name='bot  testing  commands')
    one_word_story_channel = discord.utils.get(message.server.channels, name="1  word  story")
    server = message.server

    #####UPVOTING AUTO REACTIONS
    await client.add_reaction(message, "⏬")
    await client.add_reaction(message, emoji="⭐")
    await client.add_reaction(message, emoji="⏫")

    #####MANAGING 1 WORD STORY CHANNEL
    if ' ' in message.content:
        if message.channel is one_word_story_channel:
            await client.send_message(message.author, "You may only type one word")
            await client.delete_message(message=message)
    elif message.author is hi.prev_author:
        if message.channel is one_word_story_channel:
            await client.delete_message(message=message)
            await client.send_message(message.author, "You may only type after another person")
    elif message.channel is one_word_story_channel:
        hi.prev_author = message.author


@client.event
async def on_member_update(x, y):

    #####VARIABLES
    bot_testing_commands_channel = discord.utils.get(y.server.channels, name="bot  testing  commands")
    DJ = discord.utils.get(y.server.roles, name='DJ')
    GetsAds = discord.utils.get(y.server.roles, name='GetsAds')
    GetsNotifs = discord.utils.get(y.server.roles, name='GetsNotifs')
    GameNotifs = discord.utils.get(y.server.roles, name='GameNotifs')
    Moderator = discord.utils.get(y.server.roles, name='Moderator')
    new_role_list = y.roles
    old_role_list = x.roles

    #####ASSIGNING/MANAGING MOD ROLES
    if Moderator in new_role_list:
        await client.add_roles(y, DJ, GameNotifs, GetsAds, GetsNotifs)

    if Moderator in old_role_list:
        if not DJ in new_role_list or not GetsNotifs in new_role_list or not GetsAds in new_role_list or not GameNotifs in new_role_list:
            await client.send_message(y, content='Sorry, but Moderators are required to to have this role. Please use command !6 if you need to review the requirements.')




client.run("NTEzODMyNzk3NjM5NTQwNzM5.D12Yzw.dUzzYz2y5k886Azzll2QPqMLeiM")
