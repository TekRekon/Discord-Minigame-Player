from discord.ext import commands
import discord
from Cogs.Tools import MessageTools
from itertools import cycle
import random
import math


class Connect4(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    def convert(emoji):
        if emoji == 'X':
            return '🔴'
        elif emoji == 'O':
            return '🔵'
        elif emoji == '🔵': # Blue
            return 'O'
        elif emoji == '🔴': # Red
            return 'X'
        elif emoji == '⚪': # White
            return ' '
        elif emoji == ' ':
            return '⚪'
        else:
            return emoji

    @staticmethod
    def getValidLocations(board):
        validMoves = []
        for i in range(0, 7):
            column = [row[i] for row in board]
            for n in reversed(range(0, 6)):
                if list(column)[n] == ' ':
                    validMoves.append([n, i])
                    break
        return validMoves

    @staticmethod
    def convertBoard(board, simple):
        if simple:
            for i in range(len(board)):
                for j in range(len(board[i])):
                    if board[i][j] == '⚪':
                        board[i][j] = ' '
                    elif board[i][j] in ['🔵', '🔴']:
                        board[i][j] = Connect4.convert(board[i][j])

        else:
            for i in range(len(board)):
                for j in range(len(board[i])):
                    if board[i][j] == ' ':
                        board[i][j] = '⚪'
                    elif board[i][j] in ['X', 'O']:
                        board[i][j] = Connect4.convert(board[i][j])

    @staticmethod
    def minimax(board, depth, isMaximizing, bot_mark, p_mark):
        result = Connect4.checkBoardWin(board)
        if result == 'TIE':
            print('bot tied')
            return 0
        elif result == bot_mark:
            print('bot Won')
            return 10
        elif result == p_mark:
            print('bot tied')
            return -10

        if isMaximizing:
            score = -math.inf
            for move in Connect4.getValidLocations(board):
                board[move[0]][move[1]] = bot_mark
                score = Connect4.minimax(board, depth + 1, not isMaximizing, bot_mark, p_mark)
                board[move[0]][move[1]] = ' '
            return score
        else:
            score = math.inf
            for move in Connect4.getValidLocations(board):
                board[move[0]][move[1]] = p_mark
                score = Connect4.minimax(board, depth + 1, not isMaximizing, bot_mark, p_mark)
                board[move[0]][move[1]] = ' '
            return score

    @staticmethod
    def bestMove(board, botMark, pMark):
        bestScore = -math.inf
        bestMove = []
        for move in Connect4.getValidLocations(board):
            board[move[0]][move[1]] = botMark
            score = Connect4.minimax(board, 0, False, botMark, pMark)
            print('did one minimax completely')
            board[move[0]][move[1]] = ' '
            if score > bestScore:
                bestScore = score
                bestMove = [move[0], move[1]]
        return bestMove

    @staticmethod
    def checkBoardWin(board):
        for n, list in enumerate(board):
            for i, cell in enumerate(list):
                try:
                    print(f'Trying list:({n}-{list}) and cell: ({i}-{cell})')
                    print(f'{board[n][i]} == {board[n][i+1]} == {board[n][i+2]} == {board[n][i+3]}')
                    print((board[n][i] == board[n][i+1] == board[n][i+2] == board[n][i+3]))
                    if (board[n][i] == board[n-1][i+1] == board[n-2][i+2] == board[n-3][i+3]):
                        print(f'X Won with DIAGONAL <{board[n][i]} at {n}, {i}>')
                    if (board[n][i] == board[n-1][i-1] == board[n-2][i-2] == board[n-3][i-3]):
                        print(f'X Won with DIAGONAL <{board[n][i]} at {n}, {i}>')
                    if (board[n][i] == board[n+1][i] == board[n+2][i] == board[n+3][i]):
                        print(f'X Won with VERTICAL <{board[n][i]} at {n}, {i}>')
                    if (board[n][i] == board[n][i+1] == board[n][i+2] == board[n][i+3]):
                        print(f'X Won with HORIZONTAL <{board[n][i]} at {n}, {i}>')

                        # print(board[0])
                        # print(board[1])
                        # print(board[2])
                        # print(board[3])
                        # print(board[4])
                        # print(board[5])

                except IndexError:
                    pass

        for n, list in enumerate(board):
            for i, cell in enumerate(list):
                if board[n][i] == ' ':
                    print('Keep playing')
                    # print(board[0])
                    # print(board[1])
                    # print(board[2])
                    # print(board[3])
                    # print(board[4])
                    # print(board[5])
                    return 'NO_END'

        print('TIE')
        # print(board[0])
        # print(board[1])
        # print(board[2])
        # print(board[3])
        # print(board[4])
        # print(board[5])
        return 'TIE'

    @commands.command()
    async def connect4(self, ctx):
        if MessageTools.correct_command_use(ctx, mod_command=False):

            board = [[' ']*7 for i in range(6)]
            board = [['O', 'O', 'O', 'X', 'O', ' ', ' '],
                     ['X', 'X', 'X', 'O', 'O', 'X', 'O'],
                     ['O', 'O', 'O', 'X', 'O', 'O', 'O'],
                     ['X', 'X', 'X', 'O', 'X', 'X', 'X'],
                     ['O', 'O', 'O', 'X', 'O', 'O', 'O'],
                     ['X', 'X', 'X', 'X', 'O', 'X', 'X']]
            Connect4.checkBoardWin(board)
            board = [['O', 'O', 'O', 'X', 'O', 'X', ' '],
                     ['X', 'X', 'X', 'O', 'X', 'X', 'O'],
                     ['O', 'O', 'O', 'X', 'O', 'O', 'O'],
                     ['X', 'X', 'X', 'O', 'X', 'X', 'X'],
                     ['O', 'O', 'O', 'X', 'O', 'O', 'O'],
                     ['X', 'X', 'X', 'X', 'O', 'X', 'X']]
            Connect4.checkBoardWin(board)

            def check_reaction(reaction, user):
                if reaction.emoji in ['📲', '🤖', '💢']:
                    return reaction.message.id == sent_embed.id and user == ctx.author
                if reaction.emoji in reactions:
                    for i, emoji in enumerate(reactions):
                        if emoji == reaction.emoji:
                            if board[0][i] == '⚪':
                                return reaction.message.id == sent_embed_id and user == current_player
                return False

            embed = discord.Embed(description=f'{ctx.author.mention} is waiting... \n 📲: Join the game \n 🤖: Add a bot \n 💢: Add an unbeatable bot', color=0xff0000)
            embed.set_author(name='Connect Four', icon_url='https://cdn.discordapp.com/attachments/488700267060133889/699343937965654122/ezgif-7-6d4bab9dedb9.gif')
            sent_embed = await ctx.send(embed=embed)
            await sent_embed.add_reaction('📲')
            await sent_embed.add_reaction('🤖')
            await sent_embed.add_reaction('💢')
            reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=check_reaction)
            await sent_embed.clear_reactions()
            reactions = ['🇦', '🇧', '🇨', '🇩', '🇪', '🇫', '🇬']
            alt_mark = cycle(['X', 'O'])
            p1 = ctx.author
            working = True

            if reaction.emoji == '💢':

                p2 = self.bot.user
                pList = [p1, p2]
                random.shuffle(pList)
                alt_player = cycle(pList)
                embed.set_author(name='Connect Four (Unbeatable Mode)', icon_url='https://cdn.discordapp.com/attachments/488700267060133889/699343937965654122/ezgif-7-6d4bab9dedb9.gif')
                embed.description = 'Loading...'
                await sent_embed.edit(embed=embed)
                for emoji in reactions:
                    await sent_embed.add_reaction(emoji)
                sent_embed_id = sent_embed.id
                sent_embed = await self.bot.get_channel(ctx.channel.id).fetch_message(sent_embed.id)

                while working:
                    current_player = next(alt_player)
                    current_mark = next(alt_mark)

                    # Player's turn
                    if current_player == p1:
                        ###########################
                        Connect4.convertBoard(board, simple=False)
                        #############################
                        embed.description = f'{p1.mention}({Connect4.convert(current_mark)}) Make your move \n \n {"|".join(reactions)} \n {"|".join(board[0])} \n {"|".join(board[1])} \n {"|".join(board[2])} \n {"|".join(board[3])} \n {"|".join(board[4])} \n {"|".join(board[5])}'
                        await sent_embed.edit(embed=embed)

                        reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=check_reaction)
                        await sent_embed.remove_reaction(reaction.emoji, user)
                        for i, emoji in enumerate(reactions):
                            if emoji == reaction.emoji:
                                for list in reversed(board):
                                    if list[i] == '⚪':
                                        list[i] = Connect4.convert(current_mark)
                                        break

                    # AI's turn
                    if current_player == p2:
                        print('AI move')
                        print(board)
                        print(Connect4.getValidLocations(board))
                        ##########
                        Connect4.convertBoard(board, simple=True)
                        ###########
                        move = Connect4.bestMove(board=board, botMark=current_mark, pMark=next(alt_mark))
                        print('got ai move')
                        #########
                        Connect4.convertBoard(board, simple=False)
                        #######
                        board[move[0]][move[1]] = Connect4.convert(current_mark)
                        next(alt_mark)

                    # Evaluate Board
                    Connect4.convertBoard(board, True)
                    result = Connect4.checkBoardWin(board)
                    Connect4.convertBoard(board, False)
                    if result == 'TIE':
                        working = False
                        embed.description = f'Tie between {current_player.mention}({Connect4.convert(current_mark)}) and {next(alt_player).mention}({Connect4.convert(next(alt_mark))}) \n \n {board[0]}|{board[1]}|{board[2]} \n {board[3]}|{board[4]}|{board[5]} \n {board[6]}|{board[7]}|{board[8]}'
                        await sent_embed.edit(embed=embed)
                        await sent_embed.clear_reactions()
                    elif result in ['X', 'O']:
                        working = False
                        embed.description = f'{current_player.mention}({Connect4.convert(current_mark)}) Wins \n \n {board[0]}|{board[1]}|{board[2]} \n {board[3]}|{board[4]}|{board[5]} \n {board[6]}|{board[7]}|{board[8]}'
                        await sent_embed.edit(embed=embed)
                        await sent_embed.clear_reactions()


def setup(bot):
    bot.add_cog(Connect4(bot))
