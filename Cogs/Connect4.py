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
            return '🟡'
        elif emoji == '🟡': # Yellow
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
    def convertBoard(board, simple):
        if simple:
            for i in range(len(board)):
                for j in range(len(board[i])):
                    if board[i][j] == '⚪':
                        board[i][j] = ' '
                    elif board[i][j] in ['🟡', '🔴']:
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
                    bestScore = max(bestScore, Connect4.minimax(board, depth + 1, not isMaximizing, bot_mark, p_mark))
                    board[i] = oldKey
            return bestScore
        else:
            bestScore = math.inf
            for i in range(len(board)):
                if board[i] not in ['X', 'O']:
                    oldKey = board[i]
                    board[i] = p_mark
                    bestScore = min(bestScore, Connect4.minimax(board, depth + 1, not isMaximizing, bot_mark, p_mark))
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
                score = Connect4.minimax(board, 0, False, botMark, pMark)
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
    async def connect4(self, ctx):
        if MessageTools.correct_command_use(ctx, mod_command=False):

            def check_reaction(reaction, user):
                if reaction.emoji in ['📲', '🤖', '💢']:
                    return reaction.message.id == sent_embed.id and user == ctx.author
                if reaction.emoji in reactions:
                    for i, emoji in enumerate(reactions):
                        if emoji == reaction.emoji:
                            print(f'reaction: {emoji} is equal to one in list: {reaction.emoji}')
                            if board[0][i] == '⚪':
                                print(f'{board[0][1]} is empty')
                                print(f'{reaction.message.id} and {sent_embed_id}')
                                return reaction.message.id == sent_embed_id and user == current_player
                print('False')
                return False

            embed = discord.Embed(description=f'{ctx.author.mention} is waiting... \n 📲: Join the game \n 🤖: Add a bot \n 💢: Add an unbeatable bot', color=0xff0000)
            embed.set_author(name='Connect Four', icon_url='https://cdn.discordapp.com/attachments/488700267060133889/695373427204292658/ezgif-7-895df30489d9.gif')
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
            board = [[' ']*7 for i in range(6)]

            if reaction.emoji == '💢':

                p2 = self.bot.user
                pList = [p1, p2]
                random.shuffle(pList)
                alt_player = cycle(pList)
                embed.set_author(name='Connect Four (Unbeatable Mode)', icon_url='https://cdn.discordapp.com/attachments/488700267060133889/695373427204292658/ezgif-7-895df30489d9.gif')
                embed.description = 'Loading...'
                await sent_embed.edit(embed=embed)
                for emoji in reactions:
                    await sent_embed.add_reaction(emoji)
                sent_embed_id = sent_embed.id
                sent_embed = await self.bot.get_channel(ctx.channel.id).fetch_message(sent_embed.id)

                while working:
                    current_player = p1 # next(alt_player)
                    current_mark = next(alt_mark)

                    # Player's turn
                    if current_player == p1:
                        ###########################
                        Connect4.convertBoard(board, simple=False)
                        #############################
                        embed.set_author(name='Tic Tac Toe (Unbeatable Mode)', icon_url='https://cdn.discordapp.com/attachments/488700267060133889/695373427204292658/ezgif-7-895df30489d9.gif')
                        embed.description = f'{p1.mention}({Connect4.convert(current_mark)}) Make your move \n \n {"|".join(reactions)} \n {"|".join(board[0])} \n {"|".join(board[1])} \n {"|".join(board[2])} \n {"|".join(board[3])} \n {"|".join(board[4])} \n {"|".join(board[5])}'
                        await sent_embed.edit(embed=embed)

                        reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=check_reaction)
                        await sent_embed.remove_reaction(reaction.emoji, user)
                        for i, emoji in enumerate(reactions):
                            print(f'i:{i}, emoji:{emoji}, reaction:{reaction.emoji}')
                            print(reaction.emoji == emoji)
                            if emoji == reaction.emoji:
                                print('emoji is reaction.emoji')
                                for list in reversed(board):
                                    if list[i] == '⚪':
                                        list[i] = Connect4.convert(current_mark)
                                        break

                    # AI's turn
                    if current_player == p2:
                        Connect4.convertBoard(board, simple=True)
                        index = Connect4.bestMove(board=board, botMark=current_mark, pMark=next(alt_mark))
                        Connect4.convertBoard(board, simple=False)
                        reactions.remove(board[index])
                        board[index] = Connect4.convert(current_mark)
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
