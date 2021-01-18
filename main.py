from discord.ext import commands
from Cogs.Tools import MessageTools
import asyncio
import discord


# A callable to retrieve the current guild's prefix
# def prefix(bot, message):
#     return JsonTools.getData(str(message.guild.id), 'prefix')


# pass in the callable to support per-server prefixes
# bot = commands.Bot(command_prefix=prefix)
bot = commands.Bot(command_prefix='.', help_command=None)

@bot.event
async def on_ready():
    print('Rigged for silent running')

@bot.command()
@commands.cooldown(1, 15, commands.BucketType.user)
async def help(ctx):
    def check_reaction(reaction, user):
        if reaction.emoji in ['👤', '🏆', '🎮', '🛑', '↩', '🆘']:
            return reaction.message.id == sent_embed.id and user == ctx.author
        return False

    embed = discord.Embed(description=f'{ctx.author.mention}, what can I help you with? \n 👤: **.profile** \n 🏆: **.leaderboard** \n 🎮: **.connect4** \n 🆘: **I need more help** \n 🛑: **Quit** \n ↩: **Return to this page**', color=0xff0000)
    embed.set_author(name='Help Menu', icon_url='https://cdn.discordapp.com/attachments/488700267060133889/694687205469323284/settingjif.gif')
    embed.set_footer(text='Reaction not working? Try double-tapping.')
    sent_embed = await ctx.send(embed=embed)
    for reaction in ['👤', '🏆', '🎮', '🆘', '🛑', '↩']:
        await sent_embed.add_reaction(reaction)

    working = True
    current_page = '↩'

    while working:
        try:
            reaction, user = await bot.wait_for('reaction_add', timeout=30.0, check=check_reaction)
        except TimeoutError:
            await MessageTools.sendSimpleEmbed(ctx, f"{ctx.author.mention}: Operation timed out", False)

        await sent_embed.remove_reaction(reaction.emoji, user)

        if reaction.emoji == '👤' and current_page != '👤':
            current_page = '👤'
            embed.description = f'**Usage**: .profile (mention a user) \n **Frequency**: can be used once every 15 seconds \n **Description**: Shows you the statistics of the mentioned player'
        elif reaction.emoji == '🏆' and current_page != '🏆':
            current_page = '🏆'
            embed.description = f'**Usage**: .leaderboard \n **Frequency**: can be used once every 15 seconds \n **Description**: Displays the top 10 connect four players'
        elif reaction.emoji == '🎮' and current_page != '🎮':
            current_page = '🎮'
            embed.description = f'**Usage**: .connect4 \n **Frequency**: can be used once every 15 seconds \n **Description**: Initiates a connect four game. You can play the first person to react with 📲'
        elif reaction.emoji == '🛑' and current_page != '🛑':
            working = False
            break
        elif reaction.emoji == '↩' and current_page != '↩':
            current_page = '↩'
            embed.description = f'{ctx.author.mention}, what can I help you with? \n 👤: **.profile** \n 🏆: **.leaderboard** \n 🎮: **.connect4** \n 🆘: **I need more help** \n 🛑: **Quit** \n ↩: **Home**'
        elif reaction.emoji == '🆘' and current_page != '🆘':
            current_page = '🆘'
            embed.description = f'A support server should be coming soon. In the mean time, send us an email at discordgamebothelp@gmail.com'
        await sent_embed.edit(embed=embed)
        await asyncio.sleep(1)

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
