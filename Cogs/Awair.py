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
    async def switchHepa(state):
        async with aiohttp.ClientSession() as session:
            if state:
                await session.post('https://maker.ifttt.com/trigger/hepa_on/with/key/dcUi_OJn4aUvDWuT3TO1jB')
            else:
                await session.post('https://maker.ifttt.com/trigger/hepa_off/with/key/dcUi_OJn4aUvDWuT3TO1jB')

    @staticmethod
    async def reset():
        async with aiohttp.ClientSession() as session:
            await session.post('https://maker.ifttt.com/trigger/awair_off/with/key/dcUi_OJn4aUvDWuT3TO1jB')
            await asyncio.sleep(10)
            await session.post('https://maker.ifttt.com/trigger/awair_on/with/key/dcUi_OJn4aUvDWuT3TO1jB')

    @staticmethod
    async def autoHepaToggler():
        while True:
            # Check to make sure we don't go over the call limit + conserve calls by only working during the day
            if 9 <= time.localtime().tm_hour < 21 and JsonTools.getData('awair', 'calls') < 301:

                # Increment call count
                JsonTools.changeData('awair', 'calls', JsonTools.getData('awair', 'calls')+1)

                # Get sensor dust/voc level and act on it
                try:
                    f = await Awair.getSensorData()
                    for sensor in f['data'][0]['indices']:
                        if sensor['comp'] == 'pm25':
                            dust_level = sensor['value']
                        if sensor['comp'] == 'voc':
                            voc_level = sensor['value']

                    if dust_level > 0 or voc_level > 0:
                        if not JsonTools.getData('awair', 'hepaOn'):
                            await Awair.switchHepa(True)
                            JsonTools.changeData('awair', 'hepaOn', True)

                    elif dust_level < 1 or voc_level < 1:
                        if JsonTools.getData('awair', 'hepaOn'):
                            await Awair.switchHepa(False)
                            JsonTools.changeData('awair', 'hepaOn', False)

                # Data returned is empty if device offline. The following tries to reset the device
                except IndexError:
                    print('reseting awair')
                    await Awair.reset()
                except TypeError:
                    print('<ignoring> Data was a NoneType')

            elif JsonTools.getData('awair', 'calls') > 0 and time.localtime().tm_hour == 21:
                JsonTools.changeData('awair', 'hepaOn', False)
                JsonTools.changeData('awair', 'calls', 0)
                await Awair.switchHepa(False)
                async with aiohttp.ClientSession() as session:
                    await session.post('https://maker.ifttt.com/trigger/awair_off/with/key/dcUi_OJn4aUvDWuT3TO1jB')
                    await asyncio.sleep(3600)

            await asyncio.sleep(144)


def setup(bot):
    bot.add_cog(Awair(bot))
