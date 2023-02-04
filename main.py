from discord.ext import commands
import discord
import config

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
    me = bot.get_user(config.personal_id)
    embed = discord.Embed(color=0x2596be)
    embed.set_author(name='Help Menu', icon_url='https://cdn.discordapp.com/attachments/488700267060133889/'
                                                '694687205469323284/settingjif.gif')
    embed.description = '`<>` = required argument \n `[]` = optional argument \n `+` = bot prefix'
    embed.add_field(name='​\n 🎮 Games', value=f'`+connect4` \n > Initiates a connect four game \n \n `+tictactoe` '
                                              f'\n > Initiates a tic-tac-toe game \n \n `+othello` \n > Initiates an '
                                              f'Othello (Reversi) game \n \n `+rps` \n > Initiates a '
                                              f'rock-paper-scissors game', inline=False)
    embed.add_field(name='​\n 📈 Statistics', value=f'`+profile <user mention> <connect4/tictactoe/othello/rps>` '
                                                   f'\n > Gives you the game statistics of a user \n \n `+leaderboard '
                                                   f'<connect4/tictactoe/othello/rps> [starting point]` \n > Check who '
                                                   f'the top 10 players are, or provide a starting point from which 9 '
                                                   f'additional users will be displayed', inline=False)
    embed.add_field(name='​\n 🔘 Extras', value='`+bug <message>` \n > Report a bug '
                                               '(limit once every three minutes) \n \n | [Discord]'
                                               '(https://discord.gg/tK8ThrC2DV) | [Invite Concision]'
                                               '(https://discord.com/api/oauth2/authorize?client_id=779368756199161866'
                                               '&permissions=11456&scope=bot) |')
    await ctx.send(embed=embed)


@bot.command()
@commands.cooldown(1, 5, commands.BucketType.user)
async def guildNum(ctx):
    x = bot.guilds
    sum = 0
    for f in x:
        sum += len(f.members)

    me = bot.get_user(config.personal_id)
    await me.send(f"{sum} members are using me")


bot.load_extension('Cogs.CarouselStatus')
print('CarouselStatus initiated')

bot.load_extension('Cogs.errorHandler')
print("errorHandler initiated")

bot.load_extension('Cogs.Connect4')
print("Connect4 initiated")

bot.load_extension('Cogs.admin')
print("admin initiated")

bot.load_extension('Cogs.tictactoe')
print("tictactoe initiated")

bot.load_extension('Cogs.DataCommands')
print("DataCommands initiated")

bot.load_extension('Cogs.Othello')
print("Othello initiated")

bot.load_extension('Cogs.rockpaperscissors')
print("rockpaperscissors initiated")

bot.run(config.bot_token)

