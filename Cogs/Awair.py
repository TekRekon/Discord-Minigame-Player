from discord.ext import commands, tasks
import asyncio
import aiohttp
import time
# ['data'][0]['sensors']
# ['data'][0]['indices']


class Awair(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.autoHepaToggler.start()

    @staticmethod
    async def getSensorData():
        async with aiohttp.ClientSession(headers={'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoiNjUwMjgifQ.xWoxiowcYJlamDta5SXaageYOMh0DR4c86xkxltFalQ'}) as session:
            async with session.get(url='https://developer-apis.awair.is/v1/users/self/devices/awair-element/794/air-data/latest?fahrenheit=true') as r:
                if r.status == 429:
                    print('Calls to Awair are being rate limited')
                    return None
                else:
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

    @tasks.loop(seconds=144.0)
    async def autoHepaToggler(self):
        # Conserve calls by only working during the day
        if 9 <= time.localtime().tm_hour < 21:

            # Get sensor dust/voc level and act on it
            dust_level = None
            voc_level = None
            try:
                f = await Awair.getSensorData()
                for sensor in f['data'][0]['indices']:
                    if sensor['comp'] == 'pm25':
                        dust_level = sensor['value']
                    if sensor['comp'] == 'voc':
                        voc_level = sensor['value']

                if dust_level > 0 or voc_level > 0:
                    print(f'Hepa ON at {time.localtime()}')
                    await Awair.switchHepa(True)
                else:
                    print(f'Hepa OFF at {time.localtime()}')
                    await Awair.switchHepa(False)

            # Data returned is empty if device offline. The following tries to reset the device
            except IndexError:
                print('indexError in Awair')
                # await Awair.reset()
            except TypeError:
                print('<ignoring> Data was a NoneType')

        elif time.localtime().tm_hour == 21:
            await Awair.switchHepa(False)
            await asyncio.sleep(3600)


def setup(bot):
    bot.add_cog(Awair(bot))
