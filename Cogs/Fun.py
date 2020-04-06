from discord.ext import commands
from Cogs.Tools import JsonTools, MessageTools
import discord
from itertools import cycle
import asyncio
import random


class Fun(commands.Cog):

    classAttribute = " "

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):

        # Check for an original exception, if present
        error = getattr(error, 'original', error)

        if isinstance(error, discord.errors.Forbidden):
            # Raises another Forbidden error if error message sent in channel without access
            pass
        elif isinstance(error, discord.ext.commands.errors.BadArgument) or isinstance(error, ValueError):
            await MessageTools.sendSimpleEmbed(ctx, f'{ctx.author.name}: Not valid input. Use .help for assistance',
                                               delete=True)
        elif isinstance(error, commands.DisabledCommand):
            await MessageTools.sendSimpleEmbed(ctx, f'{ctx.author.name}: {ctx.command} has been disabled',
                                               delete=True)
        elif isinstance(error, asyncio.TimeoutError):
            await MessageTools.sendSimpleEmbed(ctx.message.channel, f'{ctx.author.name}: Operation timed out',
                                               delete=False)
        # else:
        #     await ctx.send('YES! YOU FOUND AN ERROR:')
        #     await ctx.send(error)

    @commands.command()
    async def roast(self, ctx, arg: discord.Member):
        print('was good')
        if MessageTools.correct_command_use(ctx, False):
            # Find the custom emoji needed uploaded in my server
            for m in self.bot.get_guild(JsonTools.getData('477829362771689484', 'guildID')).emojis:
                if m.name == 'BoiGif':
                    if arg == self.bot.user:
                        await ctx.message.add_reaction(m)
                        await MessageTools.sendSimpleEmbed(ctx, f'{ctx.author.mention}, You roast me I roast you',
                                                           delete=False)
                    elif arg == ctx.author:
                        await ctx.message.add_reaction(m)
                    else:
                        async for message in ctx.channel.history(limit=50):
                            if message.author == arg:
                                await message.add_reaction(m)

    @commands.command()
    async def purge(self, ctx, num: int):
        if MessageTools.correct_command_use(ctx, mod_command=True):
            await ctx.message.delete()
            await ctx.channel.purge(limit=num)

    @commands.command()
    async def tictactoe(self, ctx):
        if MessageTools.correct_command_use(ctx, mod_command=False):
            def check_reaction(reaction, user):
                if reaction.emoji == '📲':
                    return reaction.message.id == sent_home_embed.id and user != ctx.author
                elif reaction.emoji == '🤖':
                    return reaction.message.id == sent_home_embed.id and user == ctx.author
                elif reaction.emoji in reactions:
                    return reaction.message.id == sent_game_embed.id and user == current_player

            reactions = ['🇦', '🇧', '🇨', '🇩', '🇪', '🇫', '🇬', '🇭', '🇮']
            alt_emoji = cycle(['❌', '⭕'])
            p1 = ctx.author
            turns = 0
            working = True
            board = {1: '🇦', 2: '🇧', 3: '🇨',
                     4: '🇩', 5: '🇪', 6: '🇫',
                     7: '🇬', 8: '🇭', 9: '🇮'}

            async def checkBoardWin(p):
                nonlocal working
                nonlocal turns
                if turns > 4 and (board[1] == board[2] == board[3] or
                                  board[4] == board[5] == board[6] or
                                  board[7] == board[8] == board[9] or
                                  board[1] == board[4] == board[7] or
                                  board[2] == board[5] == board[8] or
                                  board[3] == board[6] == board[9] or
                                  board[1] == board[5] == board[9] or
                                  board[3] == board[5] == board[7]):

                    embed = discord.Embed(description=f'{p.mention} is the winner \n \n {board[1]}|{board[2]}|'
                                          f'{board[3]} \n {board[4]}|{board[5]}|{board[6]} \n {board[7]}|{board[8]}|'
                                          f'{board[9]}', color=0xff0000)
                    embed.set_author(name='Tic Tac Toe', icon_url='https://cdn.discordapp.com/attachments/488700267060'
                                     '133889/695373427204292658/ezgif-7-895df30489d9.gif')
                    await ctx.send(embed=embed)
                    working = False
                elif turns == 9:
                    embed = discord.Embed(description=f'Tie between {p1.mention}(❌) and {p2.mention}(⭕) \n \n '
                                          f'{board[1]}|{board[2]}|{board[3]} \n {board[4]}|{board[5]}|{board[6]} \n '
                                          f'{board[7]}|{board[8]}|{board[9]}', color=0xff0000)
                    embed.set_author(name='Tic Tac Toe', icon_url='https://cdn.discordapp.com/attachments/488700267060'
                                     '133889/695373427204292658/ezgif-7-895df30489d9.gif')
                    await ctx.send(embed=embed)
                    working = False

            home_embed = discord.Embed(description=f'{ctx.author.mention} is waiting... \n 📲: Join the game \n 🤖: '
                                       f'Add a bot', color=0xff0000)
            home_embed.set_author(name='Tic Tac Toe', icon_url='https://cdn.discordapp.com/attachments/488700267060133'
                                  '889/695373427204292658/ezgif-7-895df30489d9.gif')
            sent_home_embed = await ctx.send(embed=home_embed)
            await sent_home_embed.add_reaction('📲')
            await sent_home_embed.add_reaction('🤖')

            reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=check_reaction)
            await sent_home_embed.delete()

            if reaction.emoji == '📲':
                p2 = user
                alt_player = cycle([p1, p2])

                while working:
                    current_player = next(alt_player)
                    current_mark = next(alt_emoji)
                    game_embed = discord.Embed(description=f'{current_player.mention}({current_mark})   Make your move '
                                               f'\n \n {board[1]}|{board[2]}|{board[3]} \n {board[4]}|{board[5]}|'
                                               f'{board[6]} \n {board[7]}|{board[8]}|{board[9]}', color=0xff0000)
                    game_embed.set_author(name='Tic Tac Toe', icon_url='https://cdn.discordapp.com/attachments/488700'
                                          '267060133889/695373427204292658/ezgif-7-895df30489d9.gif')
                    sent_game_embed = await ctx.send(embed=game_embed)
                    for emoji in reactions:
                        await sent_game_embed.add_reaction(emoji)
                    reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=check_reaction)
                    reactions.remove(reaction.emoji)
                    for key in board:
                        if board[key] == reaction.emoji:
                            board[key] = current_mark
                            break
                    await sent_game_embed.delete()
                    turns += 1

                    # Check for a win
                    await checkBoardWin(current_player)

            elif reaction.emoji == '🤖':
                p2 = self.bot.user

                while working:
                    current_player = p1
                    game_embed = discord.Embed(description=f'{p1.mention}(❌)   Make your move \n \n {board[1]}|'
                                               f'{board[2]}|{board[3]} \n {board[4]}|{board[5]}|{board[6]} \n '
                                               f'{board[7]}|{board[8]}|{board[9]}', color=0xff0000)
                    game_embed.set_author(name='Tic Tac Toe', icon_url='https://cdn.discordapp.com/attachments/4887002'
                                          '67060133889/695373427204292658/ezgif-7-895df30489d9.gif')
                    sent_game_embed = await ctx.send(embed=game_embed)
                    for emoji in reactions:
                        await sent_game_embed.add_reaction(emoji)
                    reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=check_reaction)
                    reactions.remove(reaction.emoji)
                    for key in board:
                        if board[key] == reaction.emoji:
                            board[key] = next(alt_emoji)
                            break
                    turns += 1
                    await checkBoardWin(p1)
                    if working:
                        bot_reaction = random.choice(reactions)
                        reactions.remove(bot_reaction)
                        for key in board:
                            if board[key] == bot_reaction:
                                board[key] = next(alt_emoji)
                                break
                        turns += 1
                        await checkBoardWin(p2)
                    await sent_game_embed.delete()


def setup(bot):
    bot.add_cog(Fun(bot))
