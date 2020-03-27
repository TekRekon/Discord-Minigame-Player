import asyncio
import discord
import requests
from bs4 import BeautifulSoup
from discord.ext import commands

client = commands.Bot(command_prefix='.')


class S:
    guild = None

    djRole = None
    getsAdsRole = None
    getsNotifsRole = None
    gameNotifsRole = None
    botNotifsRole = None
    moderatorRole = None
    extraCategoryRole = None
    levelCategoryRole = None
    profileCategoryRole = None
    modRequiredRoles = None
    memberRequiredRoles = None

    dailyPollChannel = None
    botUpdatesChannel = None
    oneWordStoryChannel = None
    botReportsChannel = None
    frontDeskChannel = None

    prevAuthor = "something"
    prevQuestion = "When ordering a soft pretzel, do you prefer salted or unsalted?"
    statusNames = ['Made By TekRekon', 'CorruptReaktor.py']
    pollButtons = ['🇦', '🇧', '🇨', '🇩', '🇪', '🇫', '🇬', '🇭', '🇮', '🇯']


async def carousel_status():
    await client.wait_until_ready()
    while True:
        for x in S.statusNames:
            await client.change_presence(status=discord.Status.online, activity=discord.Game(x), afk=False)
            await asyncio.sleep(3)


async def print_daily_poll():
    await client.wait_until_ready()
    daily_poll_answers = []
    daily_poll_website_html = requests.get('https://www.swagbucks.com/polls')
    daily_poll_website_string = BeautifulSoup(daily_poll_website_html.text, 'html.parser')
    daily_poll_question = daily_poll_website_string.find('span', attrs={'class': 'pollQuestion'}).text
    daily_poll_answers_html = daily_poll_website_string.find_all('td', attrs={'class': 'indivAnswerText'})
    while True:
        if daily_poll_question != S.prevQuestion:
            S.prevQuestion = daily_poll_question
            for x in daily_poll_answers_html:
                daily_poll_answers.append(x.text)
            daily_poll_embed = discord.Embed(title=daily_poll_question, color=0xff0000)
            counter = 0
            for x in daily_poll_answers:
                daily_poll_embed.add_field(name='\u200b', value=S.pollButtons[counter] + ' ' + x, inline=False)
                counter += 1
            sent_message = await S.dailyPollChannel.send(embed=daily_poll_embed)
            for i in range(counter):
                await sent_message.add_reaction(emoji=S.pollButtons[i])
        await asyncio.sleep(100)


@client.event
async def on_message(message):
    await client.wait_until_ready()
    author = message.author
    channel = message.channel
    content = message.content
    try:
        # One Word Story Channel Manager
        if channel is S.oneWordStoryChannel:
            if ' ' in content or author is S.prevAuthor:
                if author != client.user:
                    await message.delete()
                    warn_message = await channel.send("You may only type ONE word after another person has gone"
                                                      + author.mention)
                    await warn_message.delete(delay=2)
            else:
                S.prevAuthor = author
                await message.add_reaction(emoji="⭐")

        # Bot Auto Star Reaction
        elif channel != S.dailyPollChannel and channel != S.botUpdatesChannel:
            if author != client.user:
                await message.add_reaction(emoji="⭐")

    # Catch + Handle Error If User Blocked Bot
    except discord.errors.Forbidden:
        await message.delete()
        warn_message = await S.oneWordStoryChannel.send("Please unblock " + client.user.mention
                                                        + " to participate " + author.mention)
        await warn_message.delete(delay=5)

    # Bot Update Channel Mentioning
    if channel is S.botUpdatesChannel:
        if author != client.user:
            await S.botUpdatesChannel.send(S.botNotifsRole.mention)


@client.event
async def on_member_update(old_member, new_member):
    await client.wait_until_ready()
    # Enforce Member-Required Roles
    if old_member.roles.sort() != new_member.roles.sort():
        for role in S.memberRequiredRoles:
            if role not in new_member.roles:
                await new_member.user.add_roles(role)
                await S.botReportsChannel.send(content='WARNING ' + new_member.mention
                                                       + ": " + role.name + ' is a REQUIRED role')

    # Enforce Mod-Required Roles
    if S.moderatorRole in new_member.roles:
        for role in S.modRequiredRoles:
            if role not in new_member.roles:
                await new_member.add_roles(role)
                await S.botReportsChannel.send(content='WARNING ' + new_member.mention
                                                       + ': Moderators are required to have the ' + role.name
                                                       + ' role')


@client.event
async def on_ready():
    await client.wait_until_ready()

    S.guild = client.get_guild(477829362771689484)

    S.djRole = S.guild.get_role(490183595386863636)
    S.getsAdsRole = S.guild.get_role(515548066871246888)
    S.getsNotifsRole = S.guild.get_role(511316628013580309)
    S.gameNotifsRole = S.guild.get_role(513767484571254816)
    S.botNotifsRole = S.guild.get_role(556277198361722900)
    S.moderatorRole = S.guild.get_role(488756415738150922)
    S.extraCategoryRole = S.guild.get_role(513535344449159188)
    S.levelCategoryRole = S.guild.get_role(513535057110106134)
    S.profileCategoryRole = S.guild.get_role(513536050434539540)
    S.modRequiredRoles = [S.djRole, S.getsAdsRole, S.getsNotifsRole, S.gameNotifsRole, S.botNotifsRole,
                          S.profileCategoryRole, S.levelCategoryRole, S.extraCategoryRole]
    S.memberRequiredRoles = [S.levelCategoryRole, S.profileCategoryRole, S.extraCategoryRole]

    S.dailyPollChannel = client.get_channel(553760889778733073)
    S.botUpdatesChannel = client.get_channel(554807470288011264)
    S.oneWordStoryChannel = client.get_channel(552130564031774760)
    S.botReportsChannel = client.get_channel(488726201607782421)
    S.frontDeskChannel = client.get_channel(488745422773551107)
    client.loop.create_task(carousel_status())
    client.loop.create_task(print_daily_poll())
    print("Rigged for silent running")


client.run("NTEzODMyNzk3NjM5NTQwNzM5.D12Yzw.dUzzYz2y5k886Azzll2QPqMLeiM")
