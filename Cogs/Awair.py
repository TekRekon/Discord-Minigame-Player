from discord.ext import commands, tasks
import asyncio
import aiohttp
import time
# ['data'][0]['sensors']
# ['data'][0]['indices']


class Awair(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.autoHepaToggler.start()

    @staticmethod
    async def getSensorData():
        async with aiohttp.ClientSession(headers={'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoiNjUwMjgifQ.xWoxiowcYJlamDta5SXaageYOMh0DR4c86xkxltFalQ'}) as session:
            async with session.get(url='https://developer-apis.awair.is/v1/users/self/devices/awair-element/794/air-data/latest?fahrenheit=true') as r:
                if r.status == 429:
                    print('Calls to Awair are being rate limited')
                    result = await r.json()
                    return result
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

    @tasks.loop(seconds=300.0)
    async def autoHepaToggler(self):
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

            print(f"{dust_level} and {voc_level}")
            if dust_level > 0 or voc_level > 1:
                await Awair.switchHepa(True)
            elif dust_level == 0 and voc_level <= 1:
                await Awair.switchHepa(False)

        # Data returned is empty if device is offline
        except IndexError:
            print('indexError in Awair')
        # Anomaly
        except TypeError:
            pass



def setup(bot):
    bot.add_cog(Awair(bot))
