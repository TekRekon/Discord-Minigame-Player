from discord.ext import commands
from Cogs.Tools import JsonTools


# A callable to retrieve the current guild's prefix
def prefix(bot, message):
    return JsonTools.getData(str(message.guild.id), 'prefix')


# pass in the callable to support per-server prefixes
bot = commands.Bot(command_prefix=prefix)


@bot.event
async def on_ready():
    bot.load_extension('Cogs.DailyPoll')
    print('DailyPoll initiated')

    bot.load_extension('Cogs.CarouselStatus')
    print('CarouselStatus initiated')

    # bot.load_extension('Cogs.OneWordStoryEnforcer')
    # print('OneWordStoryEnforcer Initiated')

    # bot.load_extension('Cogs.AutoFormatNewGit')
    # print('AutoFormatNewGit Initiated')

    # bot.load_extension('Cogs.RoleEnforcer')
    # print('RoleEnforcer initiated')

    bot.load_extension('Cogs.OnDemandEmbed')
    print('OnDemandEmbed initiated')

    bot.load_extension('Cogs.ConfigBot')
    print('jsonExperiment initiated')

    bot.load_extension('Cogs.Fun')
    print('Fun initiated')

    bot.load_extension('Cogs.Awair')
    print("Awair initiated")

    bot.load_extension('Cogs.TicTacToe')
    print("TicTacToe initiated")

    bot.load_extension('Cogs.Connect4')
    print("Connect4 initiated")

    bot.load_extension('Cogs.errorHandler')
    print("errorHandler initiated")

    print('Rigged for silent running')

bot.run('NTEzODMyNzk3NjM5NTQwNzM5.Xxmt_g.fVG5cqBrAn9Z7HAx5_SecAG7DiM')
