from discord.ext import commands

bot = commands.Bot(command_prefix='.')

@bot.event
async def on_ready():
    await bot.wait_until_ready()
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

    print('Rigged for silent running')

bot.run('NTEzODMyNzk3NjM5NTQwNzM5.Xn_2cg.wXn3h9HJl-AcVA2s1gnh0hRQE7U')
