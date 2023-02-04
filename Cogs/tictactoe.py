from discord.ext import commands
import discord
from Cogs.Tools import DatabaseTools
from itertools import cycle
import random
import asyncio
import randfacts


class TicTacToe(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    def checkBoardWin(board):
        x = None
        if board[0] == board[1] == board[2]: x = board[0]
        elif board[3] == board[4] == board[5]: x = board[3]
        elif board[6] == board[7] == board[8]: x = board[6]
        elif board[0] == board[3] == board[6]: x = board[0]
        elif board[1] == board[4] == board[7]: x = board[1]
        elif board[2] == board[5] == board[8]: x = board[2]
        elif board[0] == board[4] == board[8]: x = board[0]
        elif board[2] == board[4] == board[6]: x = board[2]

        if x is not None:
            return x
        elif all(cell == '❌' or cell == '⭕' for cell in board):
            return 'TIE'
        return 'NO_END'

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command()
    @commands.guild_only()
    @commands.bot_has_permissions(manage_messages=True)
    async def tictactoe(self, ctx):

        availableReactions = ['🇦', '🇧', '🇨', '🇩', '🇪', '🇫', '🇬', '🇭', '🇮']

        def check_reaction(reaction, user):
            if reaction.emoji in ['🤖']:
                return reaction.message.id == sent_embed.id and user == ctx.author
            if reaction.emoji == '📲':
                return reaction.message.id == sent_embed.id and user != ctx.author
            if reaction.emoji in availableReactions:
                return reaction.message.id == sent_embed.id and user == current_player
            return False

        # TODO add game confirmation
        # TODO add prompt timed out exceptions
        embed = discord.Embed(description=f'{ctx.author.mention} is waiting... \n 📲: Join the game \n 🤖: Add a bot '
                                          f'(wins/losses don\'t count)', color=0x2596be)
        embed.set_author(name='Tic Tac Toe', icon_url='https://cdn.discordapp.com/attachments/488700267060133889'
                                                      '/695373427204292658/ezgif-7-895df30489d9.gif')
        embed.set_footer(text='React to continue')
        sent_embed = await ctx.send(embed=embed)
        await sent_embed.add_reaction('📲')
        await sent_embed.add_reaction('🤖')
        reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=check_reaction)
        await sent_embed.clear_reactions()
        alt_mark = cycle(['❌', '⭕'])
        p1 = ctx.author
        working = True
        board = ['🇦', '🇧', '🇨',
                 '🇩', '🇪', '🇫',
                 '🇬', '🇭', '🇮']


        if reaction.emoji == '🤖':

            p2 = self.bot.user
            pList = [p1, p2]
            random.shuffle(pList)
            alt_player = cycle(pList)
            embed.set_author(name=f'Tic Tac Toe (AI)', icon_url='https://cdn.discordapp.com/attachments/'
                            '488700267060133889/695373427204292658/ezgif-7-895df30489d9.gif')
            embed.description = 'Loading...'
            embed.set_footer(text='')
            await sent_embed.edit(embed=embed)
            for emoji in availableReactions:
                await sent_embed.add_reaction(emoji)
            embed.set_footer(text='Move not registering? Try double tapping')

            while working:
                current_player = next(alt_player)
                current_mark = next(alt_mark)

                # Player's turn
                if current_player == p1:
                    embed.description = f'{p1.mention}({current_mark}) Make your move \n \n {board[0]}|{board[1]}|' \
                                        f'{board[2]} \n {board[3]}|{board[4]}|{board[5]} \n {board[6]}|{board[7]}|' \
                                        f'{board[8]}'
                    await sent_embed.edit(embed=embed)

                    reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=check_reaction)
                    availableReactions.remove(reaction.emoji)
                    await sent_embed.clear_reaction(reaction.emoji)
                    for i in range(len(board)):
                        if board[i] == reaction.emoji:
                            board[i] = current_mark
                            break

                # AI's turn
                if current_player == p2:
                    validMoves = []
                    for i in range(0, 9):
                        if board[i] not in ['❌', '⭕']:
                            validMoves.append(i)
                    index = random.choice(validMoves)
                    availableReactions.remove(board[index])
                    await sent_embed.clear_reaction(board[index])
                    board[index] = current_mark

                # Evaluate Board
                result = TicTacToe.checkBoardWin(board)
                if result != "NO_END":
                    if result == 'TIE':
                        working = False
                        embed.description = f'Tie between {current_player.mention}({current_mark}) and ' \
                                            f'{next(alt_player).mention}({next(alt_mark)}) \n \n {board[0]}|' \
                                            f'{board[1]}|{board[2]} \n {board[3]}|{board[4]}|{board[5]} \n ' \
                                            f'{board[6]}|{board[7]}|{board[8]}'
                        embed.set_footer(text='')
                        await sent_embed.edit(embed=embed)
                        await sent_embed.clear_reactions()
                    elif result in ['❌', '⭕']:
                        working = False
                        embed.description = f'{current_player.mention}({current_mark}) Wins \n ' \
                                            f'{next(alt_player).mention}({next(alt_mark)}) Loses \n \n ' \
                                            f'{board[0]}|{board[1]}|{board[2]} \n {board[3]}|{board[4]}|{board[5]} ' \
                                            f'\n {board[6]}|{board[7]}|{board[8]}'
                        embed.set_footer(text='')
                        await sent_embed.edit(embed=embed)
                        await sent_embed.clear_reactions()

        if reaction.emoji == '📲':
            p2 = user
            pList = [p1, p2]
            random.shuffle(pList)
            alt_player = cycle(pList)
            embed.set_author(name='Tic Tac Toe (2 player)', icon_url='https://cdn.discordapp.com/attachments/'
                                                                     '488700267060133889/695373427204292658/'
                                                                     'ezgif-7-895df30489d9.gif')
            embed.description = 'Loading...'
            embed.set_footer(text=random.choice(['Move not registering? Try double tapping.', 'Looking good',
                                                 'You have 3 minutes to make a move before receiving a loss.',
                                                 randfacts.getFact(filter=True), 'Don\'t fat-finger the reactions.']))
            await sent_embed.edit(embed=embed)
            for emoji in availableReactions:
                await sent_embed.add_reaction(emoji)
            sent_embed = await self.bot.get_channel(ctx.channel.id).fetch_message(sent_embed.id)


            while working:

                # P1 and P2 turns
                current_player = next(alt_player)
                current_mark = next(alt_mark)
                other_player = next(alt_player)
                other_mark = next(alt_mark)
                next(alt_player)
                next(alt_mark)

                embed.description = f'{current_player.mention}({current_mark}) Make your move \n \n {board[0]}|' \
                                    f'{board[1]}|{board[2]} \n {board[3]}|{board[4]}|{board[5]} \n {board[6]}|' \
                                    f'{board[7]}|{board[8]}'
                embed.set_footer(text='Move not registering? Try double tapping')
                await sent_embed.edit(embed=embed)
                for reaction in sent_embed.reactions:
                    if reaction.emoji not in availableReactions:
                        await sent_embed.clear_reaction(reaction.emoji)

                try:
                    reaction, user = await self.bot.wait_for('reaction_add', timeout=180.0, check=check_reaction)
                except asyncio.TimeoutError:
                    embed.description = f'{other_player.mention}({other_mark}) Wins \n {current_player.mention}' \
                                        f'({current_mark}) Loses \n \n "Player turn timed out \n \n {board[0]}|' \
                                        f'{board[1]}|{board[2]} \n {board[3]}|{board[4]}|{board[5]} \n {board[6]}|' \
                                        f'{board[7]}|{board[8]}'
                    embed.set_footer(text='')
                    await sent_embed.edit(embed=embed)
                    await sent_embed.clear_reactions()
                    DatabaseTools.addPlayer(current_player.id, current_player.name, 'tictactoe')
                    DatabaseTools.addPlayer(other_player.id, other_player.name, 'tictactoe')
                    DatabaseTools.editPlayerScore(current_player.id, False, 'tictactoe')
                    DatabaseTools.editPlayerScore(other_player.id, True, 'tictactoe')
                    return

                availableReactions.remove(reaction.emoji)
                for i in range(len(board)):
                    if board[i] == reaction.emoji:
                        board[i] = current_mark
                        break

                # Evaluate Board
                result = TicTacToe.checkBoardWin(board)
                if result != "NO_END":
                    if result == 'TIE':
                        working = False
                        embed.description = f'Tie between {current_player.mention}({current_mark}) and ' \
                                            f'{other_player.mention}({other_mark}) \n \n {board[0]}|{board[1]}|' \
                                            f'{board[2]} \n {board[3]}|{board[4]}|{board[5]} \n {board[6]}|' \
                                            f'{board[7]}|{board[8]}'
                        embed.set_footer(text='')
                        await sent_embed.edit(embed=embed)
                        await sent_embed.clear_reactions()
                        DatabaseTools.addPlayer(current_player.id, current_player.name, 'tictactoe')
                        DatabaseTools.addPlayer(other_player.id, other_player.name, 'tictactoe')
                        DatabaseTools.editPlayerScore(current_player.id, True, 'tictactoe')
                        DatabaseTools.editPlayerScore(other_player.id, True, 'tictactoe')
                    elif result in ['❌', '⭕']:
                        working = False
                        embed.description = f'{current_player.mention}({current_mark}) Wins \n ' \
                                            f'{other_player.mention}({other_mark}) Loses \n \n {board[0]}|{board[1]}' \
                                            f'|{board[2]} \n {board[3]}|{board[4]}|{board[5]} \n {board[6]}|' \
                                            f'{board[7]}|{board[8]}'
                        embed.set_footer(text='')
                        await sent_embed.edit(embed=embed)
                        await sent_embed.clear_reactions()
                        DatabaseTools.addPlayer(current_player.id, current_player.name, 'tictactoe')
                        DatabaseTools.addPlayer(other_player.id, other_player.name, 'tictactoe')
                        DatabaseTools.editPlayerScore(current_player.id, True, 'tictactoe')
                        DatabaseTools.editPlayerScore(other_player.id, False, 'tictactoe')

def setup(bot):
    bot.add_cog(TicTacToe(bot))
