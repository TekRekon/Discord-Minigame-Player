from discord.ext import commands
from Cogs.Tools import MessageTools
import discord


# A callable to retrieve the current guild's prefix
# def prefix(bot, message):
#     return JsonTools.getData(str(message.guild.id), 'prefix')


# pass in the callable to support per-server prefixes
# bot = commands.Bot(command_prefix=prefix)
bot = commands.Bot(command_prefix='.')

@bot.event
async def on_ready():
    print('Rigged for silent running')

@bot.event
async def on_guild_join(guild):
    bot_entry = await guild.audit_logs(action=discord.AuditLogAction.bot_add).flatten()
    await MessageTools.sendSimpleEmbed(bot_entry[0].user, "Hello, human! My name is GameBot. To get started, use the command ```.help```", False)

bot.load_extension('Cogs.CarouselStatus')
print('CarouselStatus initiated')

bot.load_extension('Cogs.errorHandler')
print("errorHandler initiated")

bot.load_extension('Cogs.Connect4')
print("Connect4 initiated")


bot.run('Nzc5MzY4NzU2MTk5MTYxODY2.X7fhtw.YJwxfNWZnI6r6NXNIoRcx21e7OM')
# NTEzODMyNzk3NjM5NTQwNzM5.W_HeFQ.k086ADDikscfQ3bEju-LKfTXqGA
# Nzc5MzY4NzU2MTk5MTYxODY2.X7fhtw.YJwxfNWZnI6r6NXNIoRcx21e7OM
