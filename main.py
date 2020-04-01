from discord.ext import commands
import json


# A callable to discern the current guild's set prefix
def prefix(bot, message):
    with open('data.json', 'r') as f:
        data = json.load(f)
        f.close()
    return data[message.guild.name]['prefix']


# pass in the callable to support per-server prefixes
bot = commands.Bot(command_prefix=prefix)


@bot.event
async def on_ready():
    bot.load_extension('Cogs.DailyPoll')
    print('DailyPoll initiated')

    bot.load_extension('Cogs.CarouselStatus')
    print('CarouselStatus initiated')

    bot.load_extension('Cogs.AutoStar')
    print('AutoStar initiated')

    bot.load_extension('Cogs.OneWordStoryEnforcer')
    print('OneWordStoryEnforcer Initiated')

    bot.load_extension('Cogs.AutoFormatNewGit')
    print('AutoFormatNewGit Initiated')

    bot.load_extension('Cogs.RoleEnforcer')
    print('RoleEnforcer initiated')

    bot.load_extension('Cogs.OnDemandEmbed')
    print('OnDemandEmbed initiated')

    bot.load_extension('Cogs.ConfigBot')
    print('jsonExperiment initiated')

    print('Rigged for silent running')

bot.run('NTEzODMyNzk3NjM5NTQwNzM5.Xn_2cg.wXn3h9HJl-AcVA2s1gnh0hRQE7U')
