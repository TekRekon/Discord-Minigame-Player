from discord.ext import commands
import discord
from Cogs.Tools import MessageTools
from itertools import cycle
import random


class TicTacToe(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    def minimax(self, board, isMaximizing, bot_mark, p_mark):
        print('executing minimax with board: ')
        print(board[1]+board[2]+board[3])
        print(board[4]+board[5]+board[6])
        print(board[7]+board[8]+board[9])
        if TicTacToe.checkBoardWin(board) == 'TIE':
            print('reached tie')
            return 0
        elif TicTacToe.checkBoardWin(board) == bot_mark:
            print('reached win')
            return 10
        elif TicTacToe.checkBoardWin(board) == p_mark:
            print('reached loss')
            return -10

        if isMaximizing:
            bestScore = None
            for key in board:
                if board[key] not in ['❌', '⭕']:
                    oldKey = board[key]
                    board[key] = bot_mark
                    score = self.minimax(board, False, bot_mark, p_mark)
                    print('score: ' + score)
                    board[key] = oldKey
                    bestScore = max(score, bestScore)
            return bestScore
        else:
            bestScore = 100000000
            for key in board:
                if board[key] not in ['❌', '⭕']:
                    oldKey = board[key]
                    board[key] = p_mark
                    score = self.minimax(board, True, bot_mark, p_mark)
                    print('score: ')
                    board[key] = oldKey
                    bestScore = min(score, bestScore)

            return bestScore

    def bestMove(self, board, botMark, pMark):
        bestScore = -100000
        move = 0
        for key in board:
            if board[key] != botMark and board[key] != botMark:
                oldMark = board[key]
                board[key] = botMark
                score = self.minimax(board, False, botMark, pMark)
                board[key] = oldMark
                if score > bestScore:
                    bestScore = score
                    move = key
        return move

    @staticmethod
    def checkBoardWin(board):
        reactions = ['🇦', '🇧', '🇨', '🇩', '🇪', '🇫', '🇬', '🇭', '🇮']
        if (board[1] == board[2] == board[3] == '❌' or
                          board[4] == board[5] == board[6] == '❌' or
                          board[7] == board[8] == board[9] == '❌' or
                          board[1] == board[4] == board[7] == '❌' or
                          board[2] == board[5] == board[8] == '❌' or
                          board[3] == board[6] == board[9] == '❌' or
                          board[1] == board[5] == board[9] == '❌' or
                          board[3] == board[5] == board[7] == '❌'):
            return '❌'
        elif (board[1] == board[2] == board[3] == '⭕' or
                            board[4] == board[5] == board[6] == '⭕' or
                            board[7] == board[8] == board[9] == '⭕' or
                            board[1] == board[4] == board[7] == '⭕' or
                            board[2] == board[5] == board[8] == '⭕' or
                            board[3] == board[6] == board[9] == '⭕' or
                            board[1] == board[5] == board[9] == '⭕' or
                            board[3] == board[5] == board[7] == '⭕'):
            return '⭕'
        else:
            if all(elem == '❌' or elem == '⭕' for elem in board.values()):
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

            embed = discord.Embed(description=f'{ctx.author.mention} is waiting... \n 📲: Join the game \n 🤖: '
            f'Add a disabled bot \n 💢: Add a hard mode bot', color=0xff0000)
            embed.set_author(name='Tic Tac Toe', icon_url='https://cdn.discordapp.com/attachments/488700267060133'
                                                               '889/695373427204292658/ezgif-7-895df30489d9.gif')
            sent_embed = await ctx.send(embed=embed)
            await sent_embed.add_reaction('📲')
            await sent_embed.add_reaction('🤖')
            await sent_embed.add_reaction('💢')

            reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=check_reaction)
            await sent_embed.delete()

            reactions = ['🇦', '🇧', '🇨', '🇩', '🇪', '🇫', '🇬', '🇭', '🇮']
            alt_mark = cycle(['❌', '⭕'])
            p1 = ctx.author
            turns = 0
            working = True
            board = {1: '🇦', 2: '🇧', 3: '🇨',
                     4: '🇩', 5: '🇪', 6: '🇫',
                     7: '🇬', 8: '🇭', 9: '🇮'}

            if reaction.emoji == '🤖':
                p2 = self.bot.user
                pList = [p1, p2]
                random.shuffle(pList)
                alt_player = cycle(pList)

                while working:
                    current_player = next(alt_player)
                    current_mark = next(alt_mark)

                    # Player's turn
                    if current_player == p1:
                        embed = discord.Embed(description=f'{p1.mention}({current_mark}) Make your move \n \n {board[1]}|'
                                                          f'{board[2]}|{board[3]} \n {board[4]}|{board[5]}|{board[6]} \n '
                                                          f'{board[7]}|{board[8]}|{board[9]}', color=0xff0000)
                        embed.set_author(name='Tic Tac Toe', icon_url='https://cdn.discordapp.com/attachments/4887002'
                                         '67060133889/695373427204292658/ezgif-7-895df30489d9.gif')
                        sent_embed = await ctx.send(embed=embed)
                        for emoji in reactions:
                            await sent_embed.add_reaction(emoji)
                        reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=check_reaction)
                        await sent_embed.delete()
                        reactions.remove(reaction.emoji)
                        for key in board:
                            if board[key] == reaction.emoji:
                                board[key] = current_mark
                                break
                        turns += 1
                        if TicTacToe.checkBoardWin(board) is None:
                            working = False
                            embed.description = f'Tie between {current_player.mention}({current_mark}) and {next(alt_player).mention}({next(alt_mark)}) \n \n {board[1]}|{board[2]}|{board[3]} \n {board[4]}|{board[5]}|{board[6]} \n {board[7]}|{board[8]}|{board[9]}'
                            await ctx.send(embed=embed)
                        elif TicTacToe.checkBoardWin(board):
                            working = False
                            embed.description = f'{current_player.mention}({current_mark}) Wins \n \n {board[1]}|{board[2]}|{board[3]} \n {board[4]}|{board[5]}|{board[6]} \n {board[7]}|{board[8]}|{board[9]}'
                            await ctx.send(embed=embed)

                    # AI's turn
                    if current_player == p2:
                        turns += 1

                        # Implement MiniMax Here
                        bot_reaction = random.choice(reactions)

                        # Bot inputs chosen reaction
                        reactions.remove(bot_reaction)
                        for key in board:
                            if board[key] == bot_reaction:
                                board[key] = current_mark
                                break
                        if TicTacToe.checkBoardWin(board) is None:
                            working = False
                            embed.description = f'Tie between {current_player.mention}({current_mark}) and {next(alt_player).mention}({next(alt_mark)}) \n \n {board[1]}|{board[2]}|{board[3]} \n {board[4]}|{board[5]}|{board[6]} \n {board[7]}|{board[8]}|{board[9]}'
                            await ctx.send(embed=embed)
                        elif TicTacToe.checkBoardWin(board):
                            working = False
                            embed.description = f'{current_player.mention}({current_mark}) Wins \n \n {board[1]}|{board[2]}|{board[3]} \n {board[4]}|{board[5]}|{board[6]} \n {board[7]}|{board[8]}|{board[9]}'
                            await ctx.send(embed=embed)

            if reaction.emoji == '💢':

                p2 = self.bot.user
                pList = [p1, p2]
                random.shuffle(pList)
                alt_player = cycle(pList)

                while working:
                    current_player = next(alt_player)
                    current_mark = next(alt_mark)

                    # Player's turn
                    if current_player == p1:
                        embed = discord.Embed(description=f'{p1.mention}({current_mark}) Make your move \n \n {board[1]}|'
                        f'{board[2]}|{board[3]} \n {board[4]}|{board[5]}|{board[6]} \n '
                        f'{board[7]}|{board[8]}|{board[9]}', color=0xff0000)
                        embed.set_author(name='Tic Tac Toe', icon_url='https://cdn.discordapp.com/attachments/4887002'
                                                                      '67060133889/695373427204292658/ezgif-7-895df30489d9.gif')
                        sent_embed = await ctx.send(embed=embed)
                        for emoji in reactions:
                            await sent_embed.add_reaction(emoji)
                        reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=check_reaction)
                        await sent_embed.delete()
                        reactions.remove(reaction.emoji)
                        for key in board:
                            if board[key] == reaction.emoji:
                                board[key] = current_mark
                                break
                        turns += 1
                        if TicTacToe.checkBoardWin(board) is None:
                            working = False
                            embed.description = f'Tie between {current_player.mention}({current_mark}) and {next(alt_player).mention}({next(alt_mark)}) \n \n {board[1]}|{board[2]}|{board[3]} \n {board[4]}|{board[5]}|{board[6]} \n {board[7]}|{board[8]}|{board[9]}'
                            await ctx.send(embed=embed)
                        elif TicTacToe.checkBoardWin(board):
                            working = False
                            embed.description = f'{current_player.mention}({current_mark}) Wins \n \n {board[1]}|{board[2]}|{board[3]} \n {board[4]}|{board[5]}|{board[6]} \n {board[7]}|{board[8]}|{board[9]}'
                            await ctx.send(embed=embed)

                    # AI's turn
                    if current_player == p2:
                        turns += 1
                        # Implement MiniMax Here
                        bot_reaction = board[self.bestMove(board=board, botMark=current_mark, pMark=next(alt_mark))]
                        print('minimax completely executed')
                        next(alt_mark)

                        # Bot inputs chosen reaction
                        reactions.remove(bot_reaction)
                        for key in board:
                            if board[key] == bot_reaction:
                                board[key] = current_mark
                                break
                        if TicTacToe.checkBoardWin(board) is None:
                            working = False
                            embed.description = f'Tie between {current_player.mention}({current_mark}) and {next(alt_player).mention}({next(alt_mark)}) \n \n {board[1]}|{board[2]}|{board[3]} \n {board[4]}|{board[5]}|{board[6]} \n {board[7]}|{board[8]}|{board[9]}'
                            await ctx.send(embed=embed)
                        elif TicTacToe.checkBoardWin(board):
                            working = False
                            embed.description = f'{current_player.mention}({current_mark}) Wins \n \n {board[1]}|{board[2]}|{board[3]} \n {board[4]}|{board[5]}|{board[6]} \n {board[7]}|{board[8]}|{board[9]}'
                            await ctx.send(embed=embed)

            if reaction.emoji == '📲':
                p2 = user
                alt_player = cycle([p1, p2])
                current_player = random.choice[p1, p2]

                while working:
                    current_player = next(alt_player)
                    current_mark = next(alt_mark)
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
                    # await checkBoardWin(current_player)


def setup(bot):
    bot.add_cog(TicTacToe(bot))


