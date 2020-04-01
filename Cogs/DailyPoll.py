from discord.ext import commands
from bs4 import BeautifulSoup
import asyncio
import requests
import discord
import json


class DailyPoll(commands.Cog):
    pollButtons = ['🇦', '🇧', '🇨', '🇩', '🇪', '🇫', '🇬', '🇭', '🇮', '🇯']
    dailyPollChannel = None

    def __init__(self, bot):
        self.bot = bot
        DailyPoll.dailyPollChannel = self.bot.get_channel(553760889778733073)
        self.bot.loop.create_task(self.print_daily_poll())

    @staticmethod
    async def print_daily_poll():
        daily_poll_answers = []
        daily_poll_website_html = requests.get('https://www.swagbucks.com/polls')
        daily_poll_website_string = BeautifulSoup(daily_poll_website_html.text, 'html.parser')
        daily_poll_question = daily_poll_website_string.find('span', attrs={'class': 'pollQuestion'}).text
        daily_poll_answers_html = daily_poll_website_string.find_all('td', attrs={'class': 'indivAnswerText'})
        with open('data.json', 'r') as f:
            data = json.load(f)
        prevQuestion = data[str('prevQuestion')]
        while True:
            if daily_poll_question != prevQuestion:
                data[str('prevQuestion')] = daily_poll_question
                with open('data.json', 'w') as f:
                    json.dump(data, f)
                for x in daily_poll_answers_html:
                    daily_poll_answers.append(x.text)
                daily_poll_embed = discord.Embed(title=daily_poll_question, color=0xff0000)
                counter = 0
                for x in daily_poll_answers:
                    daily_poll_embed.add_field(name='\u200b', value=DailyPoll.pollButtons[counter] + ' ' + x,
                                               inline=False)
                    counter += 1
                sent_message = await DailyPoll.dailyPollChannel.send(embed=daily_poll_embed)
                for i in range(counter):
                    await sent_message.add_reaction(emoji=DailyPoll.pollButtons[i])
            await asyncio.sleep(5000)


def setup(bot):
    bot.add_cog(DailyPoll(bot))
