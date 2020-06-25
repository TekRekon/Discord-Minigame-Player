from discord.ext import commands
import discord
from Cogs.Tools import MessageTools
from itertools import cycle
import random
import math


class TicTacToe(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    def convert(emoji):
        if emoji == 'X':
            return '❌'
        elif emoji == 'O':
            return '⭕'
        elif emoji == '⭕':
            return 'O'
        elif emoji == '❌':
            return 'X'
        else:
            return emoji

    @staticmethod
    def convertBoard(board, simple):
        reactions = ['🇦', '🇧', '🇨', '🇩', '🇪', '🇫', '🇬', '🇭', '🇮']
        if simple:
            for i in range(len(board)):
                if board[i] in reactions:
                    board[i] = ' '
                elif board[i] in ['❌', '⭕']:
                    board[i] = TicTacToe.convert(board[i])
        else:
            for i in range(len(board)):
                if board[i] == ' ':
                    board[i] = reactions[i]
                elif board[i] in ['X', 'O']:
                    board[i] = TicTacToe.convert(board[i])

    @staticmethod
    def minimax(board, depth, isMaximizing, bot_mark, p_mark):
        print (f'doing minimax with depth {depth}')
        result = TicTacToe.checkBoardWin(board)
        if depth == 0:
            return 0
        elif result == 'TIE':
            return 0
        elif result == bot_mark:
            return 10
        elif result == p_mark:
            return -10

        if isMaximizing:
            bestScore = -math.inf
            for i in range(len(board)):
                if board[i] == ' ':
                    board[i] = bot_mark
                    bestScore = max(TicTacToe.minimax(board, depth-1, not isMaximizing, bot_mark, p_mark), bestScore)
                    board[i] = ' '
            return bestScore
        else:
            bestScore = math.inf
            for i in range(len(board)):
                if board[i] == ' ':
                    board[i] = p_mark
                    bestScore = min(TicTacToe.minimax(board, depth-1, not isMaximizing, bot_mark, p_mark), bestScore)
                    board[i] = ' '
            return bestScore

    @staticmethod
    def bestMove(board, depth, botMark, pMark):
        bestScore = -math.inf
        move = 0
        for i in range(len(board)):
            if board[i] == ' ':
                board[i] = botMark
                score = TicTacToe.minimax(board, depth, False, botMark, pMark)
                board[i] = ' '
                if score > bestScore:
                    bestScore = score
                    move = i
        return move

    @staticmethod
    def checkBoardWin(board):
        if (board[0] == board[1] == board[2] == 'X' or
                board[3] == board[4] == board[5] == 'X' or
                board[6] == board[7] == board[8] == 'X' or
                board[0] == board[3] == board[6] == 'X' or
                board[1] == board[4] == board[7] == 'X' or
                board[2] == board[5] == board[8] == 'X' or
                board[0] == board[4] == board[8] == 'X' or
                board[2] == board[4] == board[6] == 'X'):
            return 'X'
        elif (board[0] == board[1] == board[2] == 'O' or
              board[3] == board[4] == board[5] == 'O' or
              board[6] == board[7] == board[8] == 'O' or
              board[0] == board[3] == board[6] == 'O' or
              board[1] == board[4] == board[7] == 'O' or
              board[2] == board[5] == board[8] == 'O' or
              board[0] == board[4] == board[8] == 'O' or
              board[2] == board[4] == board[6] == 'O'):
            return 'O'
        else:
            if all(cell == 'X' or cell == 'O' for cell in board):
                return 'TIE'
            return 'NO_END'

    @commands.command()
    async def tictactoe(self, ctx):
        if MessageTools.correct_command_use(ctx, mod_command=False):

            def check_reaction(reaction, user):
                if reaction.emoji in ['🤖', '💢', '☮']:
                    return reaction.message.id == sent_embed.id and user == ctx.author
                if reaction.emoji == '📲':
                    return reaction.message.id == sent_embed.id and user != ctx.author
                if reaction.emoji in availableReactions:
                    return reaction.message.id == sent_embed.id and user == current_player
                return False

            embed = discord.Embed(description=f'{ctx.author.mention} is waiting... \n 📲: Join the game \n ☮: Add a **retarded** bot \n 🤖: Add a **normal** bot \n 💢: Add an **unbeatable** bot', color=0xff0000)
            embed.set_author(name='Tic Tac Toe', icon_url='https://cdn.discordapp.com/attachments/488700267060133889/695373427204292658/ezgif-7-895df30489d9.gif')
            embed.set_footer(text='React to continue')
            sent_embed = await ctx.send(embed=embed)
            await sent_embed.add_reaction('📲')
            await sent_embed.add_reaction('☮')
            await sent_embed.add_reaction('🤖')
            await sent_embed.add_reaction('💢')
            reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=check_reaction)
            await sent_embed.clear_reactions()
            alt_mark = cycle(['X', 'O'])
            p1 = ctx.author
            working = True
            board = ['🇦', '🇧', '🇨',
                     '🇩', '🇪', '🇫',
                     '🇬', '🇭', '🇮']
            availableReactions = ['🇦', '🇧', '🇨', '🇩', '🇪', '🇫', '🇬', '🇭', '🇮']


            if reaction.emoji in ['💢', '🤖', '☮']:
                if reaction.emoji == '💢':
                    depth = 100
                    mode = 'Unbeatable'
                elif reaction.emoji == '🤖':
                    depth = 5
                    mode = 'Normal'
                else:
                    depth = 1
                    mode = 'Easy'

                p2 = self.bot.user
                pList = [p1, p2]
                random.shuffle(pList)
                alt_player = cycle(pList)
                embed.set_author(name=f'Tic Tac Toe ({mode})', icon_url='https://cdn.discordapp.com/attachments/488700267060133889/695373427204292658/ezgif-7-895df30489d9.gif')
                embed.description = 'Loading...'
                embed.set_footer(text='')
                await sent_embed.edit(embed=embed)
                for emoji in availableReactions:
                    await sent_embed.add_reaction(emoji)
                sent_embed = await self.bot.get_channel(ctx.channel.id).fetch_message(sent_embed.id)

                while working:
                    current_player = next(alt_player)
                    current_mark = next(alt_mark)

                    # Player's turn
                    if current_player == p1:
                        TicTacToe.convertBoard(board, False)
                        embed.description = f'{p1.mention}({TicTacToe.convert(current_mark)}) Make your move \n \n {board[0]}|{board[1]}|{board[2]} \n {board[3]}|{board[4]}|{board[5]} \n {board[6]}|{board[7]}|{board[8]}'
                        embed.set_footer(text='Move not registering? Try double tapping')
                        await sent_embed.edit(embed=embed)
                        for reaction in sent_embed.reactions:
                            if reaction.emoji not in availableReactions:
                                await sent_embed.clear_reaction(reaction.emoji)

                        reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=check_reaction)
                        availableReactions.remove(reaction.emoji)
                        for i in range(len(board)):
                            if board[i] == reaction.emoji:
                                board[i] = TicTacToe.convert(current_mark)
                                break

                    # AI's turn
                    if current_player == p2:
                        TicTacToe.convertBoard(board, True)
                        index = TicTacToe.bestMove(board=board, depth=depth, botMark=current_mark, pMark=next(alt_mark))
                        TicTacToe.convertBoard(board, False)
                        availableReactions.remove(board[index])
                        board[index] = TicTacToe.convert(current_mark)
                        next(alt_mark)

                    # Evaluate Board
                    TicTacToe.convertBoard(board, True)
                    result = TicTacToe.checkBoardWin(board)
                    TicTacToe.convertBoard(board, False)
                    if result == 'TIE':
                        working = False
                        embed.description = f'Tie between {current_player.mention}({TicTacToe.convert(current_mark)}) and {next(alt_player).mention}({TicTacToe.convert(next(alt_mark))}) \n \n {board[0]}|{board[1]}|{board[2]} \n {board[3]}|{board[4]}|{board[5]} \n {board[6]}|{board[7]}|{board[8]}'
                        embed.set_footer(text='')
                        await sent_embed.edit(embed=embed)
                        await sent_embed.clear_reactions()
                    elif result in ['X', 'O']:
                        working = False
                        embed.description = f'{current_player.mention}({TicTacToe.convert(current_mark)}) Wins \n \n {board[0]}|{board[1]}|{board[2]} \n {board[3]}|{board[4]}|{board[5]} \n {board[6]}|{board[7]}|{board[8]}'
                        embed.set_footer(text='')
                        await sent_embed.edit(embed=embed)
                        await sent_embed.clear_reactions()

            if reaction.emoji == '📲':
                p2 = user
                pList = [p1, p2]
                random.shuffle(pList)
                alt_player = cycle(pList)
                embed.set_author(name='Tic Tac Toe (2 player)', icon_url='https://cdn.discordapp.com/attachments/488700267060133889/695373427204292658/ezgif-7-895df30489d9.gif')
                embed.description = 'Loading...'
                embed.set_footer(text='')
                await sent_embed.edit(embed=embed)
                for emoji in availableReactions:
                    await sent_embed.add_reaction(emoji)
                sent_embed = await self.bot.get_channel(ctx.channel.id).fetch_message(sent_embed.id)
                TicTacToe.convertBoard(board, simple=False)


                while working:

                        # P1 and P2 turns
                        current_player = next(alt_player)
                        current_mark = next(alt_mark)

                        embed.description = f'{current_player.mention}({TicTacToe.convert(current_mark)}) Make your move \n \n {board[0]}|{board[1]}|{board[2]} \n {board[3]}|{board[4]}|{board[5]} \n {board[6]}|{board[7]}|{board[8]}'
                        embed.set_footer(text='Move not registering? Try double tapping')
                        await sent_embed.edit(embed=embed)
                        for reaction in sent_embed.reactions:
                            if reaction.emoji not in availableReactions:
                                await sent_embed.clear_reaction(reaction.emoji)

                        reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=check_reaction)
                        availableReactions.remove(reaction.emoji)
                        for i in range(len(board)):
                            if board[i] == reaction.emoji:
                                board[i] = TicTacToe.convert(current_mark)
                                break

                        # Evaluate Board
                        TicTacToe.convertBoard(board, True)
                        result = TicTacToe.checkBoardWin(board)
                        TicTacToe.convertBoard(board, False)
                        if result == 'TIE':
                            working = False
                            embed.description = f'Tie between {current_player.mention}({TicTacToe.convert(current_mark)}) and {next(alt_player).mention}({TicTacToe.convert(next(alt_mark))}) \n \n {board[0]}|{board[1]}|{board[2]} \n {board[3]}|{board[4]}|{board[5]} \n {board[6]}|{board[7]}|{board[8]}'
                            embed.set_footer(text='')
                            await sent_embed.edit(embed=embed)
                            await sent_embed.clear_reactions()
                        elif result in ['X', 'O']:
                            working = False
                            embed.description = f'{current_player.mention}({TicTacToe.convert(current_mark)}) Wins \n \n {board[0]}|{board[1]}|{board[2]} \n {board[3]}|{board[4]}|{board[5]} \n {board[6]}|{board[7]}|{board[8]}'
                            embed.set_footer(text='')
                            await sent_embed.edit(embed=embed)
                            await sent_embed.clear_reactions()



def setup(bot):
    bot.add_cog(TicTacToe(bot))
