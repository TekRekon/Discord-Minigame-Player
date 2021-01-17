from discord.ext import commands


# A callable to retrieve the current guild's prefix
# def prefix(bot, message):
#     return JsonTools.getData(str(message.guild.id), 'prefix')


# pass in the callable to support per-server prefixes
# bot = commands.Bot(command_prefix=prefix)
bot = commands.Bot(command_prefix='.')

@bot.event
async def on_ready():
    print('Rigged for silent running')

# bot.load_extension('Cogs.PostgresTest')
# print('PostgresTest initiated')

# ^^ Archived Cogs ^^ #

bot.load_extension('Cogs.CarouselStatus')
print('CarouselStatus initiated')

bot.load_extension('Cogs.OnDemandEmbed')
print('OnDemandEmbed initiated')

bot.load_extension('Cogs.ConfigBot')
print('jsonExperiment initiated')

bot.load_extension('Cogs.Fun')
print('Fun initiated')

bot.load_extension('Cogs.TicTacToe')
print("TicTacToe initiated")

# bot.load_extension('Cogs.errorHandler')
# print("errorHandler initiated")

bot.load_extension('Cogs.Connect4')
print("Connect4 initiated")


bot.run('Nzc5MzY4NzU2MTk5MTYxODY2.X7fhtw.YJwxfNWZnI6r6NXNIoRcx21e7OM')
# NTEzODMyNzk3NjM5NTQwNzM5.W_HeFQ.k086ADDikscfQ3bEju-LKfTXqGA
# Nzc5MzY4NzU2MTk5MTYxODY2.X7fhtw.YJwxfNWZnI6r6NXNIoRcx21e7OM
