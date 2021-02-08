from discord.ext import commands
import discord

# A callable to retrieve the current guild's prefix
# def prefix(bot, message):
#     return JsonTools.getData(str(message.guild.id), 'prefix')


# pass in the callable to support per-server prefixes
# bot = commands.Bot(command_prefix=prefix)
bot = commands.Bot(command_prefix='+', help_command=None)


# TODO add win % prediction
@bot.event
async def on_ready():
    print('Rigged for silent running')


@bot.command()
@commands.cooldown(1, 5, commands.BucketType.user)
@commands.guild_only()
async def help(ctx):
    me = bot.get_user(285879705989677058)
    await me.send(f"help initiated")

    embed = discord.Embed(color=0x2596be)
    embed.set_author(name='Help Menu', icon_url='https://cdn.discordapp.com/attachments/488700267060133889/694687205469323284/settingjif.gif')
    embed.description = '`<>` = required argument \n `[]` = optional argument \n `+` = bot prefix'
    embed.add_field(name='​\n 🎮 Games', value=f'`+connect4` \n > Initiates a connect four game \n \n `+tictactoe` \n > Initiates a tic-tac-toe game \n \n `+othello` \n > Initiates an Othello (Reversi) game', inline=False)
    embed.add_field(name='​\n 📈 Statistics', value=f'`+profile <user mention> <connect4/tictactoe/othello>` \n > Gives you the game statistics of a user \n \n `+leaderboard <connect4/tictactoe/othello> [starting point]` \n > Check who the top 10 players are, or provide a starting point from which 9 additional users will be displayed. Make sure your starting point is less than the total number of ranked users', inline=False)
    embed.add_field(name='​\n 🔘 Extras', value='`+bug <message>` \n > Report a bug (limit once every three minutes) \n \n | [Discord Invite](https://discord.gg/tK8ThrC2DV) | [Invite Concision](https://discord.com/api/oauth2/authorize?client_id=779368756199161866&permissions=11456&scope=bot) |')

    await ctx.send(embed=embed)



bot.load_extension('Cogs.CarouselStatus')
print('CarouselStatus initiated')

bot.load_extension('Cogs.errorHandler')
print("errorHandler initiated")

bot.load_extension('Cogs.Connect4')
print("Connect4 initiated")

# bot.load_extension('Cogs.admin')
# print("admin initiated")

bot.load_extension('Cogs.tictactoe')
print("tictactoe initiated")

bot.load_extension('Cogs.DataCommands')
print("DataCommands initiated")

bot.load_extension('Cogs.Othello')
print("Othello initiated")

#bot.run('ODA1MTQ5MjkyNjkwOTMxNzIy.YBWrtg.e3qcrff7obkbCdMqrhD4lqy6XSc') # Reaktor01
#bot.run('NTEzODMyNzk3NjM5NTQwNzM5.W_HeFQ.k086ADDikscfQ3bEju-LKfTXqGA')  # CorruptBot
bot.run('Nzc5MzY4NzU2MTk5MTYxODY2.X7fhtw.YJwxfNWZnI6r6NXNIoRcx21e7OM')  # GameBot

