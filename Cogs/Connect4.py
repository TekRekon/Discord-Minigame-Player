from discord.ext import commands
import discord
from Cogs.Tools import MessageTools
from itertools import cycle
import random
import math
import time


class Connect4(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    def convert(emoji):
        if emoji == 'X':
            return '🔴'
        elif emoji == 'O':
            return '🔵'
        elif emoji == '🔵':  # Blue
            return 'O'
        elif emoji == '🔴':  # Red
            return 'X'
        elif emoji == '⚪':  # White
            return ' '
        elif emoji == ' ':
            return '⚪'
        else:
            return emoji

    @staticmethod
    def getValidLocations(board, playerPiece, botPiece):
        Connect4.convertBoard(board, simple=True)
        validMoves = []
        badMoves = []
        for i in range(0, 7):
            column = [row[i] for row in board]
            for n in reversed(range(0, 6)):
                if list(column)[n] == ' ':
                    # Single turn win anticipation
                    board[n][i] = playerPiece
                    if Connect4.checkBoardWin(board) == playerPiece:
                        validMoves = [[n, i]]
                        board[n][i] = ' '
                        return validMoves

                    # Double turn win anticipation
                    board[n][i] = botPiece
                    for k in range(0, 7):
                        column = [row[k] for row in board]
                        for j in reversed(range(0, 6)):
                            if list(column)[j] == ' ':
                                board[j][k] = playerPiece
                                if Connect4.checkBoardWin(board) == playerPiece:
                                    badMoves.append([n, i])
                                board[j][k] = ' '
                                break
                    if [n, i] not in badMoves:
                        validMoves.append([n, i])
                    board[n][i] = ' '
                    break

        if (len(validMoves)) == 0:
            return badMoves

        return validMoves

    @staticmethod
    def convertBoard(board, simple):
        if simple:
            for i in range(len(board)):
                for j in range(len(board[i])):
                    if board[i][j] in ['🔵', '🔴', '⚪']:
                        board[i][j] = Connect4.convert(board[i][j])

        else:
            for i in range(len(board)):
                for j in range(len(board[i])):
                    if board[i][j] in ['X', 'O', ' ']:
                        board[i][j] = Connect4.convert(board[i][j])

    @staticmethod
    def getPosValue(i, j):
        if i == 5 or i == 0:
            if j == 3:
                return 7
            if j == 2 or j == 4:
                return 5
            if j == 1 or j == 5:
                return 4
            else:
                return 3

        if i == 4 or i == 1:
            if j == 3:
                return 10
            if j == 2 or j == 4:
                return 8
            if j == 1 or j == 5:
                return 6
            else:
                return 4

        else:
            if j == 3:
                return 13
            if j == 2 or j == 4:
                return 11
            if j == 1 or j == 5:
                return 8
            else:
                return 5

    @staticmethod
    def boardHeuristic(board, bot_mark, p_mark):
        pScore = 0
        botScore = 0
        for n, list in enumerate(board):
            for i, cell in enumerate(list):
                if cell in ['X', 'O']:

                    # Positional Values
                    if board[n][i] == bot_mark:
                        botScore += Connect4.getPosValue(n, i)
                    if board[n][i] == p_mark:
                        pScore += Connect4.getPosValue(n, i)

                    # (3) up right hole *2
                    # (3) up left hole * 2
                    # (3) vertical hole * 2
                    # (3) horizontal hole * 2
                    if (i < 4 and n > 2 and (board[n][i] == board[n - 2][i + 2] == board[n - 3][i + 3])) \
                            or (i < 4 and n > 2 and (board[n][i] == board[n - 1][i + 1] == board[n - 3][i + 3])) \
                            or (i > 2 and n > 2 and (board[n][i] == board[n - 2][i - 2] == board[n - 3][i - 3])) \
                            or (i > 2 and n > 2 and (board[n][i] == board[n - 1][i - 1] == board[n - 3][i - 3])) \
                            or (n < 3 and (board[n][i] == board[n + 2][i] == board[n + 3][i])) \
                            or (n < 3 and (board[n][i] == board[n + 1][i] == board[n + 3][i])) \
                            or (i < 4 and (board[n][i] == board[n][i + 2] == board[n][i + 3])) \
                            or (i < 4 and (board[n][i] == board[n][i + 1] == board[n][i + 3])):
                        if cell == bot_mark:
                            botScore += 250
                        else:
                            pScore += 260

                    # (3) up right
                    # (3) up left
                    # (3) vertical
                    # (3) horizontal
                    if (i < 5 and n > 1 and (board[n][i] == board[n - 1][i + 1] == board[n - 2][i + 2])) \
                            or (i > 1 and n > 1 and (board[n][i] == board[n - 1][i - 1] == board[n - 2][i - 2])) \
                            or (n < 4 and (board[n][i] == board[n + 1][i] == board[n + 2][i])) \
                            or (i < 5 and (board[n][i] == board[n][i + 1] == board[n][i + 2])):
                        if cell == bot_mark:
                            botScore += 200
                        else:
                            pScore += 210

                    # (2) up right
                    # (2) up left
                    # (2) vertical
                    # (2) horizontal
                    if (i < 6 and n > 0 and (board[n][i] == board[n - 1][i + 1])) \
                            or (i > 0 and n > 0 and (board[n][i] == board[n - 1][i - 1])) \
                            or (n < 5 and (board[n][i] == board[n + 1][i])) \
                            or (i < 6 and (board[n][i] == board[n][i + 1])):
                        if cell == bot_mark:
                            botScore += 50
                        else:
                            pScore += 60
        return botScore - pScore

    @staticmethod
    def minimax(board, depth, isMaximizing, bot_mark, p_mark, alpha, beta):
        result = Connect4.checkBoardWin(board)
        if result == 'TIE':
            return 0
        elif result == bot_mark:
            return 100000
        elif result == p_mark:
            return -100000
        elif depth == 0:
            return Connect4.boardHeuristic(board, bot_mark, p_mark)

        if isMaximizing:
            bestScore = -math.inf
            for move in Connect4.getValidLocations(board, p_mark, bot_mark):
                board[move[0]][move[1]] = bot_mark
                bestScore = max(bestScore,
                                Connect4.minimax(board, depth - 1, not isMaximizing, bot_mark, p_mark, alpha, beta))
                alpha = max(alpha, bestScore)
                board[move[0]][move[1]] = ' '
                if beta <= alpha:
                    break
            return bestScore
        else:
            bestScore = math.inf
            for move in Connect4.getValidLocations(board, p_mark, bot_mark):
                board[move[0]][move[1]] = p_mark
                bestScore = min(bestScore,
                                Connect4.minimax(board, depth - 1, not isMaximizing, bot_mark, p_mark, alpha, beta))
                beta = min(beta, bestScore)
                board[move[0]][move[1]] = ' '
                if beta <= alpha:
                    break
            return bestScore

    @staticmethod
    def bestMove(board, botMark, pMark, depth):
        bestScore = -math.inf
        bestMove = []
        for move in Connect4.getValidLocations(board, pMark, botMark):
            board[move[0]][move[1]] = botMark
            score = Connect4.minimax(board, depth, False, botMark, pMark, -math.inf, math.inf)
            board[move[0]][move[1]] = ' '
            if score > bestScore:
                bestScore = score
                bestMove = [move[0], move[1]]
        return bestMove

    @staticmethod
    def checkBoardWin(board):
        for n, list in enumerate(board):
            for i, cell in enumerate(list):
                if cell in ['X', 'O']:
                    if i < 4 and n > 2 and (
                            board[n][i] == board[n - 1][i + 1] == board[n - 2][i + 2] == board[n - 3][i + 3]):
                        return cell
                    if i > 2 and n > 2 and (
                            board[n][i] == board[n - 1][i - 1] == board[n - 2][i - 2] == board[n - 3][i - 3]):
                        return cell
                    if n < 3 and (board[n][i] == board[n + 1][i] == board[n + 2][i] == board[n + 3][i]):
                        return cell
                    if i < 4 and (board[n][i] == board[n][i + 1] == board[n][i + 2] == board[n][i + 3]):
                        return cell
                    if n == 0 and ' ' not in board[n]:
                        return 'TIE'
        return 'NO_END'

    # async def editMSG(self, board, botTurn, embed, sentEmbed):
    #
    #

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def connect4(self, ctx):
        try:
            if MessageTools.correct_command_use(ctx, mod_command=False):

                reactions = ['🇦', '🇧', '🇨', '🇩', '🇪', '🇫', '🇬']
                # board = [[' ']*7 for i in range(6)]
                board = [[' ', ' ', ' ', ' ', ' ', ' ', ' '],  # board[0][0-6]
                         [' ', ' ', ' ', ' ', ' ', ' ', ' '],  # board[1][0-6}
                         [' ', ' ', ' ', ' ', ' ', ' ', ' '],
                         [' ', ' ', ' ', ' ', ' ', ' ', ' '],
                         [' ', ' ', ' ', ' ', ' ', ' ', ' '],
                         [' ', ' ', ' ', ' ', ' ', ' ', ' ']]

                def check_reaction(reaction, user):
                    if reaction.emoji in ['🤖', '💢']:
                        return reaction.message.id == sent_embed.id and user == ctx.author
                    if reaction.emoji == '📲':
                        return reaction.message.id == sent_embed.id and user != ctx.author
                    if reaction.emoji in reactions:
                        for i, emoji in enumerate(reactions):
                            if emoji == reaction.emoji:
                                if board[0][i] == '⚪':
                                    return reaction.message.id == sent_embed.id and user == current_player
                    return False

                embed = discord.Embed(
                    description=f'{ctx.author.mention} is waiting... \n 📲: Join the game (not implemented) \n 🤖: **Spectate two bots fight** \n 💢: **Add a smart AI**',
                    color=0xff0000)
                embed.set_author(name='Connect Four',
                                 icon_url='https://cdn.discordapp.com/attachments/488700267060133889/699343937965654122/ezgif-7-6d4bab9dedb9.gif')
                sent_embed = await ctx.send(embed=embed)
                await sent_embed.add_reaction('📲')
                await sent_embed.add_reaction('🤖')
                await sent_embed.add_reaction('💢')
                reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=check_reaction)
                await sent_embed.clear_reactions()
                alt_mark = cycle(['X', 'O'])
                p1 = ctx.author
                working = True

                # Unbeatable? Mode #
                if reaction.emoji == '💢':

                    # Constants #
                    depth = 5
                    ####################################################################################################
                    temp = 0
                    botTime = 10
                    p2 = self.bot.user
                    pList = [p1, p2]
                    random.shuffle(pList)
                    alt_player = cycle(pList)
                    longestTime = 0
                    lowestScore = 0
                    highestScore = 0
                    odd = False
                    if (next(alt_player) == self.bot.user):
                        odd = True
                        print('Bot is odd')
                    next(alt_player)
                    print('human is odd')



                    # Loading Connect4 #
                    embed.set_author(name='Connect Four (Smart Mode)',
                                     icon_url='https://cdn.discordapp.com/attachments/488700267060133889/699343937965654122/ezgif-7-6d4bab9dedb9.gif')
                    embed.description = 'Loading...'
                    await sent_embed.edit(embed=embed)
                    for emoji in reactions:
                        await sent_embed.add_reaction(emoji)
                    sent_embed = await self.bot.get_channel(ctx.channel.id).fetch_message(sent_embed.id)

                    # Actual Game #
                    while working:
                        current_player = next(alt_player)
                        current_mark = next(alt_mark)
                        Connect4.convertBoard(board, simple=True)
                        if current_player == self.bot.user:
                            currentHeursitic = Connect4.boardHeuristic(board, current_mark, next(alt_mark))
                            next(alt_mark)
                        else:
                            currentHeursitic = Connect4.boardHeuristic(board, next(alt_mark), next(alt_mark))

                        if currentHeursitic < lowestScore:
                            lowestScore = currentHeursitic
                        elif currentHeursitic > highestScore:
                            highestScore = currentHeursitic
                        if botTime > longestTime:
                            longestTime = botTime

                        # Player's turn
                        if current_player == p1:
                            Connect4.convertBoard(board, simple=False)
                            embed.description = f'{p1.mention}({Connect4.convert(current_mark)}) Make your move \n \n Current bot score: **{currentHeursitic}** \n \n I took **{round(botTime, 1)} seconds** \n \n I\'m planning ahead with depth **{depth}** \n \n {"|".join(reactions)} \n {"|".join(board[0])} \n {"|".join(board[1])} \n {"|".join(board[2])} \n {"|".join(board[3])} \n {"|".join(board[4])} \n {"|".join(board[5])}'
                            embed.set_footer(text='Move not registering? Try double tapping')
                            await sent_embed.edit(embed=embed)
                            start = time.time()
                            reaction, user = await self.bot.wait_for('reaction_add', timeout=300.0,
                                                                     check=check_reaction)
                            end = time.time()
                            await sent_embed.remove_reaction(reaction.emoji, user)
                            for i, emoji in enumerate(reactions):
                                if emoji == reaction.emoji:
                                    for list in reversed(board):
                                        if list[i] == '⚪':
                                            list[i] = Connect4.convert(current_mark)
                                            break
                            if botTime < 4:
                                temp += 1
                                if temp == 2:
                                    depth += 1
                                    temp = 0
                            embed.description = f'{p2.mention}({Connect4.convert(next(alt_mark))}) is thinking... \n \n Current bot score: **{currentHeursitic}** \n \n You took **{round(end - start, 1)} seconds** \n \n I\'m planning ahead with depth **{depth}** \n \n {"|".join(reactions)} \n {"|".join(board[0])} \n {"|".join(board[1])} \n {"|".join(board[2])} \n {"|".join(board[3])} \n {"|".join(board[4])} \n {"|".join(board[5])}'
                            await sent_embed.edit(embed=embed)
                            next(alt_mark)

                        # AI's turn
                        elif current_player == p2:
                            start = time.time()
                            move = Connect4.bestMove(board=board, botMark=current_mark, pMark=next(alt_mark),
                                                     depth=depth)
                            board[move[0]][move[1]] = current_mark
                            next(alt_mark)
                            end = time.time()
                            botTime = end - start

                        # Evaluate Board #
                        Connect4.convertBoard(board, simple=True)
                        result = Connect4.checkBoardWin(board)
                        Connect4.convertBoard(board, simple=False)
                        if result == 'TIE':
                            working = False
                            embed.description = f'Tie between {current_player.mention}({Connect4.convert(current_mark)}) and {next(alt_player).mention}({Connect4.convert(next(alt_mark))}) \n \n {"|".join(reactions)} \n {"|".join(board[0])} \n {"|".join(board[1])} \n {"|".join(board[2])} \n {"|".join(board[3])} \n {"|".join(board[4])} \n {"|".join(board[5])}'
                            embed.set_footer(text='')
                            await sent_embed.edit(embed=embed)
                            await sent_embed.clear_reactions()
                        elif result in ['X', 'O']:
                            working = False
                            embed.description = f'{current_player.mention}({Connect4.convert(current_mark)}) Wins \n {next(alt_player).mention}({Connect4.convert(next(alt_mark))}) Loses \n My **highest score** was **{highestScore}** \n My **lowest score** was **{lowestScore}** \n My **longest move** took **{round(longestTime, 1)} seconds** \n I ended with depth **{depth}** \n \n {"|".join(reactions)} \n {"|".join(board[0])} \n {"|".join(board[1])} \n {"|".join(board[2])} \n {"|".join(board[3])} \n {"|".join(board[4])} \n {"|".join(board[5])}'
                            embed.set_footer(text='')
                            await sent_embed.edit(embed=embed)
                            await sent_embed.clear_reactions()

                if reaction.emoji == '🤖':

                    # Constants #
                    depth1 = 5
                    depth2 = 5
                    #############################################################################################################
                    temp1 = 0
                    temp2 = 0
                    bot1Time = 10
                    bot2Time = 10
                    pList = ['P1', 'P2']
                    random.shuffle(pList)
                    alt_player = cycle(pList)

                    # Loading Connect4 #
                    embed.set_author(name='Connect Four (Spectator Mode)',
                                     icon_url='https://cdn.discordapp.com/attachments/488700267060133889/699343937965654122/ezgif-7-6d4bab9dedb9.gif')
                    embed.description = 'Loading...'
                    await sent_embed.edit(embed=embed)
                    sent_embed_id = sent_embed.id
                    sent_embed = await self.bot.get_channel(ctx.channel.id).fetch_message(sent_embed.id)

                    # Actual Game #
                    while working:
                        current_player = next(alt_player)
                        current_mark = next(alt_mark)
                        Connect4.convertBoard(board, simple=True)

                        # AI 1 turn
                        if current_player == 'P1':
                            if bot1Time < 5:
                                temp1 += 1
                                if temp1 == 2:
                                    depth1 += 1
                                    temp1 = 0
                            start = time.time()
                            move = Connect4.bestMove(board=board, botMark=current_mark, pMark=next(alt_mark),
                                                     depth=depth1)
                            board[move[0]][move[1]] = current_mark
                            next(alt_mark)
                            end = time.time()
                            bot1Time = end - start

                            Connect4.convertBoard(board, simple=False)
                            embed.description = f'**P2** ({Connect4.convert(next(alt_mark))}) is thinking... \n \n **P1** took **{round(bot1Time, 1)} seconds** \n \n **P2** planning with depth **{depth2}** \n \n {"|".join(reactions)} \n {"|".join(board[0])} \n {"|".join(board[1])} \n {"|".join(board[2])} \n {"|".join(board[3])} \n {"|".join(board[4])} \n {"|".join(board[5])}'
                            await sent_embed.edit(embed=embed)
                            next(alt_mark)

                        # AI 2 turn
                        elif current_player == 'P2':
                            if bot2Time < 4:
                                temp2 += 1
                                if temp2 == 2:
                                    depth2 += 1
                                    temp2 = 0
                            start = time.time()
                            move = Connect4.bestMove(board=board, botMark=current_mark, pMark=next(alt_mark),
                                                     depth=depth2)
                            board[move[0]][move[1]] = current_mark
                            next(alt_mark)
                            end = time.time()
                            bot2Time = end - start

                            Connect4.convertBoard(board, simple=False)
                            embed.description = f'**P1**({Connect4.convert(next(alt_mark))}) is thinking... \n \n **P2** took **{round(bot2Time, 1)} seconds** \n \n **P1** planning with depth **{depth1}** \n \n {"|".join(reactions)} \n {"|".join(board[0])} \n {"|".join(board[1])} \n {"|".join(board[2])} \n {"|".join(board[3])} \n {"|".join(board[4])} \n {"|".join(board[5])}'
                            await sent_embed.edit(embed=embed)
                            next(alt_mark)

                        # Evaluate Board #
                        Connect4.convertBoard(board, simple=True)
                        result = Connect4.checkBoardWin(board)
                        Connect4.convertBoard(board, simple=False)
                        if result == 'TIE':
                            working = False
                            embed.description = f'Tie between {current_player}({Connect4.convert(current_mark)}) and {next(alt_player)}({Connect4.convert(next(alt_mark))}) \n \n {"|".join(reactions)} \n {"|".join(board[0])} \n {"|".join(board[1])} \n {"|".join(board[2])} \n {"|".join(board[3])} \n {"|".join(board[4])} \n {"|".join(board[5])}'
                            embed.set_footer(text='')
                            await sent_embed.edit(embed=embed)
                            await sent_embed.clear_reactions()
                        elif result in ['X', 'O']:
                            working = False
                            embed.description = f'**{current_player}**({Connect4.convert(current_mark)}) Wins \n \n {"|".join(reactions)} \n {"|".join(board[0])} \n {"|".join(board[1])} \n {"|".join(board[2])} \n {"|".join(board[3])} \n {"|".join(board[4])} \n {"|".join(board[5])}'
                            embed.set_footer(text='')
                            await sent_embed.edit(embed=embed)
                            await sent_embed.clear_reactions()

                # if reaction.emoji == '📲':
                #
                #     p2 = self.bot.user
                #     pList = [p1, p2]
                #     random.shuffle(pList)
                #     alt_player = cycle(pList)
                #     embed.set_author(name='Connect Four (Maybe beatable? mode)', icon_url='https://cdn.discordapp.com/attachments/488700267060133889/699343937965654122/ezgif-7-6d4bab9dedb9.gif')
                #     embed.description = 'Loading...'
                #     await sent_embed.edit(embed=embed)
                #     for emoji in reactions:
                #         await sent_embed.add_reaction(emoji)
                #     sent_embed_id = sent_embed.id
                #     sent_embed = await self.bot.get_channel(ctx.channel.id).fetch_message(sent_embed.id)
                #
                #     while working:
                #         current_player = next(alt_player)
                #         current_mark = next(alt_mark)
                #
                #         # Player's turn
                #         if current_player == p1:
                #             ###########################
                #             Connect4.convertBoard(board, simple=False)
                #             #############################
                #             embed.description = f'{p1.mention}({Connect4.convert(current_mark)}) Make your move \n \n {"|".join(reactions)} \n {"|".join(board[0])} \n {"|".join(board[1])} \n {"|".join(board[2])} \n {"|".join(board[3])} \n {"|".join(board[4])} \n {"|".join(board[5])}'
                #             embed.set_footer(text='Move not registering? Try double tapping')
                #             await sent_embed.edit(embed=embed)
                #
                #             reaction, user = await self.bot.wait_for('reaction_add', timeout=300.0, check=check_reaction)
                #             await sent_embed.remove_reaction(reaction.emoji, user)
                #             for i, emoji in enumerate(reactions):
                #                 if emoji == reaction.emoji:
                #                     for list in reversed(board):
                #                         if list[i] == '⚪':
                #                             list[i] = Connect4.convert(current_mark)
                #                             break
                #             embed.description = f'{p2.mention}({Connect4.convert(next(alt_mark))}) is thinking... \n \n {"|".join(reactions)} \n {"|".join(board[0])} \n {"|".join(board[1])} \n {"|".join(board[2])} \n {"|".join(board[3])} \n {"|".join(board[4])} \n {"|".join(board[5])}'
                #             await sent_embed.edit(embed=embed)
                #             next(alt_mark)
                #
                #         # AI's turn
                #         if current_player == p2:
                #             move = Connect4.bestMove(board=board, botMark=current_mark, pMark=next(alt_mark))
                #             board[move[0]][move[1]] = current_mark
                #             next(alt_mark)
                #
                #         # Evaluate Board
                #         result = Connect4.checkBoardWin(board)
                #         Connect4.convertBoard(board, False)
                #         if result == 'TIE':
                #             working = False
                #             embed.description = f'Tie between {current_player.mention}({Connect4.convert(current_mark)}) and {next(alt_player).mention}({Connect4.convert(next(alt_mark))}) \n \n {"|".join(reactions)} \n {"|".join(board[0])} \n {"|".join(board[1])} \n {"|".join(board[2])} \n {"|".join(board[3])} \n {"|".join(board[4])} \n {"|".join(board[5])}'
                #             embed.set_footer(text='')
                #             await sent_embed.edit(embed=embed)
                #             await sent_embed.clear_reactions()
                #         elif result in ['X', 'O']:
                #             working = False
                #             embed.description = f'{current_player.mention}({Connect4.convert(current_mark)}) Wins \n \n {"|".join(reactions)} \n {"|".join(board[0])} \n {"|".join(board[1])} \n {"|".join(board[2])} \n {"|".join(board[3])} \n {"|".join(board[4])} \n {"|".join(board[5])}'
                #             embed.set_footer(text='')
                #             await sent_embed.edit(embed=embed)
                #             await sent_embed.clear_reactions()

        except TimeoutError:
            print('TIMEOUT ERROR in connect4')
            pass


def setup(bot):
    bot.add_cog(Connect4(bot))
