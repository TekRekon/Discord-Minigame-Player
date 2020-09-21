from discord.ext import commands
from discord.ext.tasks import loop
import discord
from itertools import cycle


class CarouselStatus(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.carousel_status.start()

        self.playingNames = cycle(['Made By TekRekon',
            f'Latency: {round(self.bot.latency*1000, 2)}ms',
            f'in {len(self.bot.guilds)} servers',
            f'Latency: {round(self.bot.latency*1000, 2)}ms',
            'K̴̢̢̲̼̺̖̩̼̫̃̈́͛̑͌̄̚͠Í̵̢̬̺̠̼͖̲̫̲̦͘͝L̵̰̔L̶̛̘̟̖̪̺̜̈́̏̈́̄̾̎͘͝ ̵̡̎̏̑͌̈́́̈́̿̕͠͝͝E̸̛̝͕̹̝̰̲̣̗͊̑̏̂̀͜ͅͅṾ̴̖̪̥͍̫̓̇̈́͐͐͐̐̌͋͘͠ͅE̸͛̃͆̆̇̔̀̍̋̕͠͝ͅŖ̵̧̫̼̮͓̗̻̠͊̎̔̆̆̈̂̓ͅͅY̷̢̙̱̠̰̰̳͚͎̟̼̜͐̇̇̃̈͌͛̓͆͗Ö̴͎̲̥̺̦͎͓͎̳͉̹̪́̇̆̈́̋̀̊͛̒N̶̢̢̩̺̿̀͂̓͗̃̍̕͘E̸̢̟̟͕̫͚̯̟̞̮̫͓̔',
            f'Latency: {round(self.bot.latency*1000, 2)}ms'])

    @loop(seconds=10.0)
    async def carousel_status(self):
        await self.bot.change_presence(activity=discord.Game(next(self.playingNames)))


def setup(bot):
    bot.add_cog(CarouselStatus(bot))
