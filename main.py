from discord.ext import commands
from Cogs.Tools import MessageTools
import asyncio
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


# TODO handle timout
@bot.command()
@commands.cooldown(1, 5, commands.BucketType.user)
@commands.guild_only()
async def help(ctx, arg: str = None):
    me = bot.get_user(285879705989677058)
    await me.send(f"help initiated")
    def check_reaction(reaction, user):
        if reaction.emoji in ['👤', '🏆', '🎮', '❌', '🛑', '↩', '🆘']:
            return reaction.message.id == sent_embed.id and user == ctx.author
        return False

    embed = discord.Embed(color=0xff0000)
    embed.set_author(name='Help Menu', icon_url='https://cdn.discordapp.com/attachments/488700267060133889/694687205469323284/settingjif.gif')
    embed.set_image(url='https://cdn.discordapp.com/attachments/488700267060133889/803420849155473438/rgb.gif')

    if arg is not None:
        if arg.lower() == 'a':
            embed.description = f'**Usage**: +profile <user mention> <mode> \n **Frequency**: can be used once every 5 seconds \n **Description**: Shows you the statistics of the mentioned player in the specified game mode'
            embed.add_field(name='<user mention>', value='an @ mention')
            embed.add_field(name='<mode>', value='connect4, tictactoe')
        elif arg.lower() == 'b':
            embed.description = f'**Usage**: +leaderboard <mode> <starting point> \n **Frequency**: can be used once every 5 seconds \n **Description**: Displays 10 connect four players by order of win % from the given starting point, or the best players if left blank'
            embed.add_field(name='<mode>', value='connect4, tictactoe')
            embed.add_field(name='<starting point>', value='OPTIONAL: A number starting at one but less than the total number of ranked players')
        elif arg.lower() == 'c':
            embed.description = f'**Usage**: +connect4 \n **Frequency**: can be used once every 5 seconds \n **Description**: Initiates a connect four game. You can play the first person to react with 📲 within 60 seconds'
        elif arg.lower() == 'd':
            embed.description = f'**Usage**: +tictactoe \n **Frequency**: can be used once every 5 seconds \n **Description**: Initiates a tic-tac-toe game. You can play the first person to react with 📲 within 60 seconds, or play a bot by reacting with 🤖'
        elif arg.lower() == 'e':
            embed.description = f'A support server should be coming soon. In the mean time, send us an email at discordgamebothelp@gmail.com'
        else:
            embed.description = f'🚫 That page does not exist'
        await ctx.send(embed=embed)

    elif not ctx.guild.me.guild_permissions.manage_messages:
        embed.description = f'{ctx.author.mention}, I do not have the manage messages permission. Bot functionality is limited and the help pages will have to be navigated manually. Use \n ```+help <letter>``` to navigate the menu \n \n 🇦: **+profile** \n 🇧: **+leaderboard** \n 🇨: **+connect4** \n 🇩: **+tictactoe** \n 🇪: **I need more help**'
        await ctx.send(embed=embed)

    else:
        embed.description = f'{ctx.author.mention}, what can I help you with? \n 👤: **+profile** \n 🏆: **+leaderboard** \n 🎮: **+connect4** \n ❌: **+tictactoe** \n 🆘: **I need more help** \n 🛑: **Quit** \n ↩: **Return to this page**'
        embed.set_footer(text='Reaction not working? Try double-tapping.')
        sent_embed = await ctx.send(embed=embed)
        for reaction in ['👤', '🏆', '🎮', '❌', '🆘', '🛑', '↩']:
            await sent_embed.add_reaction(reaction)

        working = True
        current_page = '↩'

        while working:
            try:
                reaction, user = await bot.wait_for('reaction_add', timeout=60.0, check=check_reaction)
            except TimeoutError:
                await MessageTools.sendSimpleEmbed(ctx, f"{ctx.author.mention}: Operation timed out", False)

            await sent_embed.remove_reaction(reaction.emoji, user)

            if reaction.emoji == '👤' and current_page != '👤':
                current_page = '👤'
                embed.description = f'**Usage**: +profile <user mention> <mode> \n **Frequency**: can be used once every 5 seconds \n **Description**: Shows you the statistics of the mentioned player in the specified game mode'
                embed.add_field(name='<user mention>', value='an @ mention')
                embed.add_field(name='<mode>', value='connect4, tictactoe')
            elif reaction.emoji == '🏆' and current_page != '🏆':
                current_page = '🏆'
                embed.description = f'**Usage**: +leaderboard <mode> <starting point> \n **Frequency**: can be used once every 5 seconds \n **Description**: Displays 10 connect four players by order of win % from the given starting point, or the best players if left blank'
                embed.add_field(name='<mode>', value='connect4, tictactoe')
                embed.add_field(name='<starting point>', value='OPTIONAL: A number starting at one but less than the total number of ranked players')
            elif reaction.emoji == '🎮' and current_page != '🎮':
                current_page = '🎮'
                embed.description = f'**Usage**: +connect4 \n **Frequency**: can be used once every 5 seconds \n **Description**: Initiates a connect four game. You can play the first person to react with 📲 within 60 seconds'
            elif reaction.emoji == '❌' and current_page != '❌':
                current_page = '❌'
                embed.description = f'**Usage**: +tictactoe \n **Frequency**: can be used once every 5 seconds \n **Description**: Initiates a tic-tac-toe game. You can play the first person to react with 📲 within 60 seconds, or play a bot by reacting with 🤖'
            elif reaction.emoji == '🛑' and current_page != '🛑':
                await sent_embed.clear_reactions()
                embed.description = f'Have a good day!'
                embed.set_footer(text='')
                embed.clear_fields()
                await sent_embed.edit(embed=embed)
                await sent_embed.delete(delay=2)
                working = False
                break
            elif reaction.emoji == '↩' and current_page != '↩':
                current_page = '↩'
                embed.description = f'{ctx.author.mention}, what can I help you with? \n 👤: **+profile** \n 🏆: **+leaderboard** \n 🎮: **+connect4** \n ❌: **+tictactoe** \n 🆘: **I need more help** \n 🛑: **Quit** \n ↩: **Return to this page**'
            elif reaction.emoji == '🆘' and current_page != '🆘':
                current_page = '🆘'
                embed.description = f'A support server should be coming soon. In the mean time, send us an email at discordgamebothelp@gmail.com'
            await sent_embed.edit(embed=embed)
            embed.clear_fields()
            await asyncio.sleep(1)


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

#bot.run('NTEzODMyNzk3NjM5NTQwNzM5.W_HeFQ.k086ADDikscfQ3bEju-LKfTXqGA')  # CorruptBot
bot.run('Nzc5MzY4NzU2MTk5MTYxODY2.X7fhtw.YJwxfNWZnI6r6NXNIoRcx21e7OM')  # GameBot

