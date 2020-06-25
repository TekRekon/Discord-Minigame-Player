from discord.ext import commands
import asyncio
import discord


class CarouselStatus(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.bot.loop.create_task(self.carousel_status())

    async def carousel_status(self):
        playingNames = ['Made By TekRekon',
                       'K̴̢̢̲̼̺̖̩̼̫̃̈́͛̑͌̄̚͠Í̵̢̬̺̠̼͖̲̫̲̦͘͝L̵̰̔L̶̛̘̟̖̪̺̜̈́̏̈́̄̾̎͘͝ ̵̡̎̏̑͌̈́́̈́̿̕͠͝͝E̸̛̝͕̹̝̰̲̣̗͊̑̏̂̀͜ͅͅṾ̴̖̪̥͍̫̓̇̈́͐͐͐̐̌͋͘͠ͅE̸͛̃͆̆̇̔̀̍̋̕͠͝ͅŖ̵̧̫̼̮͓̗̻̠͊̎̔̆̆̈̂̓ͅͅY̷̢̙̱̠̰̰̳͚͎̟̼̜͐̇̇̃̈͌͛̓͆͗Ö̴͎̲̥̺̦͎͓͎̳͉̹̪́̇̆̈́̋̀̊͛̒N̶̢̢̩̺̿̀͂̓͗̃̍̕͘E̸̢̟̟͕̫͚̯̟̞̮̫͓̔',
                       f'in {len(self.bot.guilds)} servers',
                        'use .tictactoe',
                           'K̴̢̢̲̼̺̖̩̼̫̃̈́͛̑͌̄̚͠Í̵̢̬̺̠̼͖̲̫̲̦͘͝L̵̰̔L̶̛̘̟̖̪̺̜̈́̏̈́̄̾̎͘͝ ̵̡̎̏̑͌̈́́̈́̿̕͠͝͝E̸̛̝͕̹̝̰̲̣̗͊̑̏̂̀͜ͅͅṾ̴̖̪̥͍̫̓̇̈́͐͐͐̐̌͋͘͠ͅE̸͛̃͆̆̇̔̀̍̋̕͠͝ͅŖ̵̧̫̼̮͓̗̻̠͊̎̔̆̆̈̂̓ͅͅY̷̢̙̱̠̰̰̳͚͎̟̼̜͐̇̇̃̈͌͛̓͆͗Ö̴͎̲̥̺̦͎͓͎̳͉̹̪́̇̆̈́̋̀̊͛̒N̶̢̢̩̺̿̀͂̓͗̃̍̕͘E̸̢̟̟͕̫͚̯̟̞̮̫͓̔',
                        'Visit dailyPoll channel!',
                        f'Latency: {round(self.bot.latency*1000, 2)}ms',
                        'K̴̢̢̲̼̺̖̩̼̫̃̈́͛̑͌̄̚͠Í̵̢̬̺̠̼͖̲̫̲̦͘͝L̵̰̔L̶̛̘̟̖̪̺̜̈́̏̈́̄̾̎͘͝ ̵̡̎̏̑͌̈́́̈́̿̕͠͝͝E̸̛̝͕̹̝̰̲̣̗͊̑̏̂̀͜ͅͅṾ̴̖̪̥͍̫̓̇̈́͐͐͐̐̌͋͘͠ͅE̸͛̃͆̆̇̔̀̍̋̕͠͝ͅŖ̵̧̫̼̮͓̗̻̠͊̎̔̆̆̈̂̓ͅͅY̷̢̙̱̠̰̰̳͚͎̟̼̜͐̇̇̃̈͌͛̓͆͗Ö̴͎̲̥̺̦͎͓͎̳͉̹̪́̇̆̈́̋̀̊͛̒N̶̢̢̩̺̿̀͂̓͗̃̍̕͘E̸̢̟̟͕̫͚̯̟̞̮̫͓̔',
                        'use .embed']

        while True:
            for x in playingNames:
                await self.bot.change_presence(status=discord.Status.online, activity=discord.Game(x), afk=False)
                await asyncio.sleep(3)


def setup(bot):
    bot.add_cog(CarouselStatus(bot))
