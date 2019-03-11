import discord
from discord.ext import commands
import time
import requests
from bs4 import BeautifulSoup
import asyncio

client = commands.Bot(command_prefix='.')


#####STARTUP
@client.event
async def on_ready():
    print("I am ready")
    await client.change_presence(game=discord.Game(name="CorruptReaktor.py"), status=None, afk=False)
    await printDailyPoll()

class storage():
    client.wait_until_ready()
    prev_author = "something"

#Print the daily poll
async def printDailyPoll():
    while True:
        daily_poll_channel = client.get_channel('553760889778733073')
        daily_poll_website_html = requests.get('https://www.swagbucks.com/polls')
        daily_poll_huge_string = BeautifulSoup(daily_poll_website_html.text, 'html.parser')
        daily_poll_question = daily_poll_huge_string.find('span', attrs={'class':'pollQuestion'}).text
        daily_poll_answers_html = daily_poll_huge_string.find_all('td', attrs={'class':'indivAnswerText'})
        daily_poll_answers = []
        test = ['🇦', '🇧', '🇨', '🇩', '🇪', '🇫', '🇬', '🇭', '🇮', '🇯']
        for x in daily_poll_answers_html:
            daily_poll_answers.append(x.text)
        daily_poll_embed = discord.Embed(title=daily_poll_question, color=0xff0000)
        counter = 0
        for x in daily_poll_answers:
            daily_poll_embed.add_field(name='\u200b', value=test[counter] + ' ' + x, inline=False)
            counter += 1
        sent_message = await client.send_message(daily_poll_channel, embed=daily_poll_embed)
        for i in range(counter):
            await client.add_reaction(sent_message, emoji=test[i])
        await asyncio.sleep(86400)

@client.event
async def on_message(message):

    #VARIABLES
    bot_testing_commands_channel = discord.utils.get(message.server.channels, name='bot  testing  commands')
    one_word_story_channel = discord.utils.get(message.server.channels, name="1  word  story")
    daily_poll_channel = client.get_channel('553760889778733073')
    server = message.server

    # UPVOTING AUTO REACTIONS
    if message.channel != daily_poll_channel:
        await client.add_reaction(message, emoji="⏬")
        await client.add_reaction(message, emoji="⭐")
        await client.add_reaction(message, emoji="⏫")

    #MANAGING 1 WORD STORY CHANNEL
    if ' ' in message.content:
        if message.channel is one_word_story_channel:
            if message.author != client.user:
                my_message = await client.send_message(message.channel, "You may only type one word" + message.author.mention)
                time.sleep(2)
                await client.delete_message(message=my_message)
                await client.delete_message(message=message)
    elif message.author is storage.prev_author:
        if message.channel is one_word_story_channel:
            if message.author != client.user:
                my_message = await client.send_message(message.channel, "You may only type after another person" + message.author.mention)
                time.sleep(2)
                await client.delete_message(message=my_message)
                await client.delete_message(message=message)
    elif message.channel is one_word_story_channel:
        storage.prev_author = message.author

@client.event
async def on_member_update(x, y):

    #VARIABLES
    bot_testing_commands_channel = discord.utils.get(y.server.channels, name="bot  testing  commands")
    DJ = discord.utils.get(y.server.roles, name='DJ')
    GetsAds = discord.utils.get(y.server.roles, name='GetsAds')
    GetsNotifs = discord.utils.get(y.server.roles, name='GetsNotifs')
    GameNotifs = discord.utils.get(y.server.roles, name='GameNotifs')
    Moderator = discord.utils.get(y.server.roles, name='Moderator')
    bot_reports = discord.utils.get(x.server.channels, name = 'bot  reports')
    new_role_list = y.roles
    old_role_list = x.roles

    #####ASSIGNING/MANAGING MOD ROLES
    if Moderator in new_role_list:
        await client.add_roles(y, DJ, GameNotifs, GetsAds, GetsNotifs)

    if Moderator in old_role_list:
        if not DJ in new_role_list or not GetsNotifs in new_role_list or not GetsAds in new_role_list or not GameNotifs in new_role_list:
            await client.send_message(bot_reports, content='Sorry, but Moderators are required to to have this role. '
                                                           'Please use command !6 if you need to review the requirements.' + x.mention)


client.run("NTEzODMyNzk3NjM5NTQwNzM5.D12Yzw.dUzzYz2y5k886Azzll2QPqMLeiM")
