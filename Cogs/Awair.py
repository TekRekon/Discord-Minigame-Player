from discord.ext import commands
import asyncio
from Cogs.Tools import JsonTools
import aiohttp
import time
import random
# ['data'][0]['sensors']
# ['data'][0]['indices']


class Awair(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.bot.loop.create_task(self.autoHepaToggler())

    @staticmethod
    async def getSensorData():
        async with aiohttp.ClientSession(headers={'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoiNjUwMjgifQ.xWoxiowcYJlamDta5SXaageYOMh0DR4c86xkxltFalQ'}) as session:
            async with session.get(url='https://developer-apis.awair.is/v1/users/self/devices/awair-element/794/air-data/latest?fahrenheit=true') as r:
                if r.status == 200:
                    result = await r.json()
                    return result

    @staticmethod
    async def autoHepaToggler():
        while True:
            print('looping')
            # Check to make sure we don't go over the call limit + conserve calls by only working during the day
            if 9 <= time.localtime().tm_hour < 21 and JsonTools.getData('awair', 'calls') < 301:
                print(f'time correct: Hour {time.localtime().tm_hour}')

                # Increment call count
                JsonTools.changeData('awair', 'calls', JsonTools.getData('awair', 'calls')+1)

                # Get sensor dust level
                f = await Awair.getSensorData()
                for sensor in f['data'][0]['indices']:
                    if sensor['comp'] == 'pm25':
                        print('found sensor')
                        dustLevel = sensor['value']
                        print('assigned sensor')

                        if dustLevel > 0 and not JsonTools.getData('awair', 'hepaOn'):
                            print('turning on hepa')
                            async with aiohttp.ClientSession() as session:
                                await session.post('https://maker.ifttt.com/trigger/hepa_on/with/key/dcUi_OJn4aUvDWuT3TO1jB')
                            JsonTools.changeData('awair', 'hepaOn', True)
                            print(f'{dustLevel} --> Hepa On')

                        elif dustLevel < 1 and JsonTools.getData('awair', 'hepaOn'):
                            print('turning off hepa')
                            async with aiohttp.ClientSession() as session:
                                await session.post('https://maker.ifttt.com/trigger/hepa_off/with/key/dcUi_OJn4aUvDWuT3TO1jB')
                            JsonTools.changeData('awair', 'hepaOn', False)
                            print(f'{dustLevel} --> Hepa Off')

                        print(f'Level: {dustLevel} and Hepa is {JsonTools.getData("awair", "hepaOn")}')

            elif JsonTools.getData('awair', 'calls') > 0 and time.localtime().tm_hour == 21:
                print('it is now 9 oclock, turning off')
                JsonTools.changeData('awair', 'hepaOn', False)
                JsonTools.changeData('awair', 'calls', 0)
                async with aiohttp.ClientSession() as session:
                    await session.post('https://maker.ifttt.com/trigger/hepa_off/with/key/dcUi_OJn4aUvDWuT3TO1jB')
                print(f'Time: {time.localtime().tm_hour} --> Hepa Off')

            await asyncio.sleep(144)


def setup(bot):
    bot.add_cog(Awair(bot))
