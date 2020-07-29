from discord.ext import commands
from bs4 import BeautifulSoup
import asyncio
import requests
import discord
from Cogs.Tools import JsonTools


class DailyPoll(commands.Cog):
    dailyPollChannel = None
    dailyPollChannel2 = None

    def __init__(self, bot):
        self.bot = bot
        DailyPoll.dailyPollChannel = self.bot.get_channel(725540024912707686)
        self.bot.loop.create_task(self.print_daily_poll())

    @staticmethod
    async def print_daily_poll():
        while True:
            pollButtons = ['🇦', '🇧', '🇨', '🇩', '🇪', '🇫', '🇬', '🇭', '🇮', '🇯']
            daily_poll_answers = []
            daily_poll_website_html = requests.get('https://www.swagbucks.com/polls')
            daily_poll_website_string = BeautifulSoup(daily_poll_website_html.text, 'html.parser')
            daily_poll_question = daily_poll_website_string.find('span', attrs={'class': 'pollQuestion'}).text
            daily_poll_answers_html = daily_poll_website_string.find_all('td', attrs={'class': 'indivAnswerText'})
            prevQuestion = JsonTools.getData('constants', 'prevQuestion')
            if daily_poll_question != prevQuestion:
                print(f'new question: {daily_poll_answers} DOES not equal old question: {prevQuestion}')
                JsonTools.changeData('constants', 'prevQuestion', daily_poll_question)
                for x in daily_poll_answers_html:
                    daily_poll_answers.append(x.text)
                daily_poll_embed = discord.Embed(title=daily_poll_question, color=0xff0000)
                for x, answer in enumerate(daily_poll_answers):
                    daily_poll_embed.add_field(name='\u200b', value=pollButtons[x] + ' ' + answer, inline=False)
                sent_message = await DailyPoll.dailyPollChannel.send(embed=daily_poll_embed)
                for i in range(len(daily_poll_answers)):
                    await sent_message.add_reaction(emoji=pollButtons[i])
            await asyncio.sleep(5000)


def setup(bot):
    bot.add_cog(DailyPoll(bot))
