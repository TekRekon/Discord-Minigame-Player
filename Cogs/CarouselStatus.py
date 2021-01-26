from discord.ext import commands, tasks
import discord
from itertools import cycle


class CarouselStatus(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.playingNames = cycle([f'Latency: {round(self.bot.latency*1000, 2)}ms', f'in {len(self.bot.guilds)} servers', '+help'])
        self.carousel_status.start()

    @tasks.loop(seconds=15.0)
    async def carousel_status(self):
        await self.bot.change_presence(activity=discord.Game(next(self.playingNames)))


def setup(bot):
    bot.add_cog(CarouselStatus(bot))
