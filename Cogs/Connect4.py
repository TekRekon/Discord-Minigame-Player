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
        result = TicTacToe.checkBoardWin(board)
        if result == 'TIE':
            return 0
        elif result == bot_mark and isMaximizing:
            return 10-depth
        elif result == p_mark and not isMaximizing:
            return -10+depth
        elif result == bot_mark:
            return 10
        elif result == p_mark:
            return -10

        if isMaximizing:
            bestScore = -math.inf
            for i in range(len(board)):
                if board[i] not in ['X', 'O']:
                    oldKey = board[i]
                    board[i] = bot_mark
                    bestScore = max(bestScore, TicTacToe.minimax(board, depth + 1, not isMaximizing, bot_mark, p_mark))
                    board[i] = oldKey
            return bestScore
        else:
            bestScore = math.inf
            for i in range(len(board)):
                if board[i] not in ['X', 'O']:
                    oldKey = board[i]
                    board[i] = p_mark
                    bestScore = min(bestScore, TicTacToe.minimax(board, depth + 1, not isMaximizing, bot_mark, p_mark))
                    board[i] = oldKey
            return bestScore

    @staticmethod
    def bestMove(board, botMark, pMark):
        bestScore = -math.inf
        move = 0
        for i in range(len(board)):
            if board[i] not in ['X', 'O']:
                oldMark = board[i]
                board[i] = botMark
                score = TicTacToe.minimax(board, 0, False, botMark, pMark)
                board[i] = oldMark
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
                if reaction.emoji in ['📲', '🤖', '💢']:
                    return reaction.message.id == sent_embed.id and user == ctx.author
                if reaction.emoji in reactions:
                    return reaction.message.id == sent_embed.id and user == current_player
                return False

            embed = discord.Embed(description=f'{ctx.author.mention} is waiting... \n 📲: Join the game \n 🤖: Add a bot \n 💢: Add an unbeatable bot', color=0xff0000)
            embed.set_author(name='Tic Tac Toe', icon_url='https://cdn.discordapp.com/attachments/488700267060133889/695373427204292658/ezgif-7-895df30489d9.gif')
            sent_embed = await ctx.send(embed=embed)
            await sent_embed.add_reaction('📲')
            await sent_embed.add_reaction('🤖')
            await sent_embed.add_reaction('💢')
            reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=check_reaction)
            await sent_embed.delete()

            alt_mark = cycle(['X', 'O'])
            p1 = ctx.author
            working = True
            board = ['🇦', '🇧', '🇨',
                     '🇩', '🇪', '🇫',
                     '🇬', '🇭', '🇮']

            if reaction.emoji == '💢':

                p2 = self.bot.user
                pList = [p1, p2]
                random.shuffle(pList)
                alt_player = cycle(pList)
                reactions = ['🇦', '🇧', '🇨', '🇩', '🇪', '🇫', '🇬', '🇭', '🇮']

                while working:
                    current_player = next(alt_player)
                    current_mark = next(alt_mark)

                    # Player's turn
                    if current_player == p1:
                        print('player turn')
                        print(board)
                        TicTacToe.convertBoard(board, False)
                        embed = discord.Embed(description=f'{p1.mention}({TicTacToe.convert(current_mark)}) Make your move \n \n {board[0]}|{board[1]}|{board[2]} \n {board[3]}|{board[4]}|{board[5]} \n {board[6]}|{board[7]}|{board[8]}', color=0xff0000)
                        embed.set_author(name='Tic Tac Toe (Unbeatable Mode)', icon_url='https://cdn.discordapp.com/attachments/488700267060133889/695373427204292658/ezgif-7-895df30489d9.gif')
                        sent_embed = await ctx.send(embed=embed)
                        for emoji in reactions:
                            await sent_embed.add_reaction(emoji)

                        reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=check_reaction)
                        await sent_embed.delete()
                        reactions.remove(reaction.emoji)
                        for i in range(len(board)):
                            if board[i] == reaction.emoji:
                                board[i] = TicTacToe.convert(current_mark)
                                break

                    # AI's turn
                    if current_player == p2:
                        TicTacToe.convertBoard(board, True)
                        print('ai turn')
                        print(board)
                        index = TicTacToe.bestMove(board=board, botMark=current_mark, pMark=next(alt_mark))
                        TicTacToe.convertBoard(board, False)
                        reactions.remove(board[index])
                        board[index] = TicTacToe.convert(current_mark)
                        next(alt_mark)

                    # Evaluate Board
                    TicTacToe.convertBoard(board, True)
                    result = TicTacToe.checkBoardWin(board)
                    TicTacToe.convertBoard(board, False)
                    if result == 'TIE':
                        working = False
                        embed.description = f'Tie between {current_player.mention}({TicTacToe.convert(current_mark)}) and {next(alt_player).mention}({TicTacToe.convert(next(alt_mark))}) \n \n {board[0]}|{board[1]}|{board[2]} \n {board[3]}|{board[4]}|{board[5]} \n {board[6]}|{board[7]}|{board[8]}'
                        await ctx.send(embed=embed)
                    elif result in ['X', 'O']:
                        working = False
                        embed.description = f'{current_player.mention}({TicTacToe.convert(current_mark)}) Wins \n \n {board[0]}|{board[1]}|{board[2]} \n {board[3]}|{board[4]}|{board[5]} \n {board[6]}|{board[7]}|{board[8]}'
                        await ctx.send(embed=embed)