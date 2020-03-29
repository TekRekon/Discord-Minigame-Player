from discord.ext import commands
import asyncio
import discord


class CarouselStatus(commands.Cog):
    statusNames = ['Made By TekRekon', 'K̴̢̢̲̼̺̖̩̼̫̃̈́͛̑͌̄̚͠Í̵̢̬̺̠̼͖̲̫̲̦͘͝L̵̰̔L̶̛̘̟̖̪̺̜̈́̏̈́̄̾̎͘͝ ̵̡̎̏̑͌̈́́̈́̿̕͠͝͝E̸̛̝͕̹̝̰̲̣̗͊̑̏̂̀͜ͅͅṾ̴̖̪̥͍̫̓̇̈́͐͐͐̐̌͋͘͠ͅE̸͛̃͆̆̇̔̀̍̋̕͠͝ͅŖ̵̧̫̼̮͓̗̻̠͊̎̔̆̆̈̂̓ͅͅY̷̢̙̱̠̰̰̳͚͎̟̼̜͐̇̇̃̈͌͛̓͆͗Ö̴͎̲̥̺̦͎͓͎̳͉̹̪́̇̆̈́̋̀̊͛̒N̶̢̢̩̺̿̀͂̓͗̃̍̕͘E̸̢̟̟͕̫͚̯̟̞̮̫͓̔', 'CorruptReaktor.py', 'K̴̢̢̲̼̺̖̩̼̫̃̈́͛̑͌̄̚͠Í̵̢̬̺̠̼͖̲̫̲̦͘͝L̵̰̔L̶̛̘̟̖̪̺̜̈́̏̈́̄̾̎͘͝ ̵̡̎̏̑͌̈́́̈́̿̕͠͝͝E̸̛̝͕̹̝̰̲̣̗͊̑̏̂̀͜ͅͅṾ̴̖̪̥͍̫̓̇̈́͐͐͐̐̌͋͘͠ͅE̸͛̃͆̆̇̔̀̍̋̕͠͝ͅŖ̵̧̫̼̮͓̗̻̠͊̎̔̆̆̈̂̓ͅͅY̷̢̙̱̠̰̰̳͚͎̟̼̜͐̇̇̃̈͌͛̓͆͗Ö̴͎̲̥̺̦͎͓͎̳͉̹̪́̇̆̈́̋̀̊͛̒N̶̢̢̩̺̿̀͂̓͗̃̍̕͘E̸̢̟̟͕̫͚̯̟̞̮̫͓̔']

    def __init__(self, bot):
        self.bot = bot
        self.bot.loop.create_task(self.carousel_status())

    async def carousel_status(self):
        while True:
            for n, x in enumerate(CarouselStatus.statusNames):
                await self.bot.change_presence(status=discord.Status.online,
                                               activity=discord.Game(x), afk=False)
                if n % 2 == 0:
                    await asyncio.sleep(2)
                else:
                    await asyncio.sleep(0.5)


def setup(bot):
    bot.add_cog(CarouselStatus(bot))
