from discord.ext import commands
import discord
from Cogs.Tools import MessageTools, ConnectFourAI
from itertools import cycle
import random
import time
import psycopg2


class Connect4(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def profile(self, ctx, arg: discord.Member):
        con = psycopg2.connect("postgres://tmneuvqnzogsxo:d15b738ee44cc1429e2cf014bf3c1df8448fea2b0155a4157e8e2a37dbc0d495@ec2-54-146-142-58.compute-1.amazonaws.com:5432/d3ad8vk1so3cfu")
        cur = con.cursor()

        cur.execute("SELECT user_id FROM playerConnect4Stats")
        rows = cur.fetchall()

        if arg.id not in [i[0] for i in rows]:
            embed = discord.Embed(title=f'{arg.name} does not exist in my database', color=0xff0000)
            embed.set_author(name='Null Profile', icon_url='https://cdn.discordapp.com/attachments/488700267060133889/777402434447474698/ef6d69dfe7a08c26207dfde9117c8217.gif')
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(description='\u200b', color=0xff0000)
            embed.set_author(name=f'{arg.name}\'s Profile', icon_url='https://cdn.discordapp.com/attachments/488700267060133889/777402434447474698/ef6d69dfe7a08c26207dfde9117c8217.gif')

            cur.execute("SELECT wins, losses FROM playerConnect4Stats WHERE user_id = %s", [arg.id])
            row = cur.fetchall()
            wins = row[0][0]
            losses = row[0][1]

            embed.add_field(name='🏆 **Wins**', value=f'{wins}', inline=True)
            embed.add_field(name='☠ **Losses**', value=f'{losses}', inline=True)

            win_percent = 100
            if wins + losses == 0:
                embed.add_field(name='💠 **Win %**', value='N/A', inline=True)
            elif wins == 0:
                embed.add_field(name='💠 **Win %**', value='0', inline=True)
            elif losses == 0:
                embed.add_field(name='💠 **Win %**', value='100', inline=True)
            else:
                embed.add_field(name='💠 **Win %**', value=f'{round((wins/(losses+wins)*100), 2)}', inline=True)

            await ctx.send(embed=embed)


        cur.execute("SELECT user_id, username, wins, losses FROM playerConnect4Stats")

        rows = cur.fetchall()
        for r in rows:
            print(f"ID: {r[0]}, NAME: {r[1]}, WINS: {r[2]}, LOSS: {r[3]}")

        cur.close()
        con.close()


    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def connect4(self, ctx):
        ConnectFourAI.addPlayer(ctx.author.id, ctx.author.name)


        if MessageTools.correct_command_use(ctx, mod_command=False):

            # Universal Constants #
            reactions = ['🇦', '🇧', '🇨', '🇩', '🇪', '🇫', '🇬']
            # board = [[' ']*7 for i in range(6)]
            board = [[' ', ' ', ' ', ' ', ' ', ' ', ' '],  # board[0][0-6]
                     [' ', ' ', ' ', ' ', ' ', ' ', ' '],  # board[1][0-6}
                     [' ', ' ', ' ', ' ', ' ', ' ', ' '],
                     [' ', ' ', ' ', ' ', ' ', ' ', ' '],
                     [' ', ' ', ' ', ' ', ' ', ' ', ' '],
                     [' ', ' ', ' ', ' ', ' ', ' ', ' ']]
            alt_mark = cycle(['X', 'O'])
            p1 = ctx.author
            working = True

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

            # Options Menu #
            embed = discord.Embed(description=f'{ctx.author.mention} is waiting... \n 📲: **Join the game** \n 💢: **(DISABLED) Add a smart AI**', color=0xff0000)
            embed.set_author(name='Connect Four', icon_url='https://cdn.discordapp.com/attachments/488700267060133889/699343937965654122/ezgif-7-6d4bab9dedb9.gif')
            sent_embed = await ctx.send(embed=embed)
            await sent_embed.add_reaction('📲')
            await sent_embed.add_reaction('💢')
            reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=check_reaction)
            await sent_embed.clear_reactions()

            if reaction.emoji == '📲':
                ConnectFourAI.addPlayer(user.id, user.name)
                # Player vs player Variables #
                pList = [ctx.author, user]
                random.shuffle(pList)
                alt_player = cycle(pList)
                eList = ['🔵', '🔴']
                random.shuffle(eList)
                alt_emoji = cycle(eList)


                # Loading Connect4 #
                embed.set_author(name='Connect Four (1v1 Mode)', icon_url='https://cdn.discordapp.com/attachments/488700267060133889/699343937965654122/ezgif-7-6d4bab9dedb9.gif')
                embed.description = 'Loading...'
                await sent_embed.edit(embed=embed)
                for emoji in reactions:
                    await sent_embed.add_reaction(emoji)
                sent_embed = await self.bot.get_channel(ctx.channel.id).fetch_message(sent_embed.id)

                # Actual Game #
                while working:
                    current_player = next(alt_player)
                    current_emoji = next(alt_emoji)

                    ConnectFourAI.convertBoard(board, simple=False)
                    joinedBoard = ["|".join(reactions), "|".join(board[0]), "|".join(board[1]), "|".join(board[2]), "|".join(board[3]), "|".join(board[4]), "|".join(board[5])]

                    # Player's turn
                    embed.description = f'{current_player.mention}({current_emoji}) Make your move \n \n {joinedBoard[0]} \n {joinedBoard[1]} \n {joinedBoard[2]} \n {joinedBoard[3]} \n {joinedBoard[4]} \n {joinedBoard[5]} \n {joinedBoard[6]}'
                    embed.set_footer(text='Move not registering? Try double tapping')
                    await sent_embed.edit(embed=embed)
                    reaction, user = await self.bot.wait_for('reaction_add', timeout=300.0, check=check_reaction)
                    await sent_embed.remove_reaction(reaction.emoji, user)
                    for i, emoji in enumerate(reactions):
                        if emoji == reaction.emoji:
                            for list in reversed(board):
                                if list[i] == '⚪':
                                    list[i] = current_emoji
                                    break

                    # Evaluate Board #
                    joinedBoard = ["|".join(reactions), "|".join(board[0]), "|".join(board[1]), "|".join(board[2]), "|".join(board[3]), "|".join(board[4]), "|".join(board[5])]
                    ConnectFourAI.convertBoard(board, simple=True)
                    result = ConnectFourAI.checkBoardWin(board)
                    ConnectFourAI.convertBoard(board, simple=False)
                    if result == 'TIE':
                        working = False
                        ConnectFourAI.editPlayerScore(ctx.author.id, True)
                        ConnectFourAI.editPlayerScore(user.id, True)
                        embed.description = f'Tie between {current_player.mention}({current_emoji}) and {next(alt_player).mention}({next(alt_emoji)}) \n \n {joinedBoard[0]} \n {joinedBoard[1]} \n {joinedBoard[2]} \n {joinedBoard[3]} \n {joinedBoard[4]} \n {joinedBoard[5]} \n {joinedBoard[6]}'
                        embed.set_footer(text='')
                        await sent_embed.edit(embed=embed)
                        await sent_embed.clear_reactions()
                    elif result in ['X', 'O']:
                        working = False
                        ConnectFourAI.editPlayerScore(current_player.id, True)
                        ConnectFourAI.editPlayerScore(next(alt_player).id, False)
                        next(alt_player)
                        embed.description = f'{current_player.mention}({current_emoji}) Wins \n {next(alt_player).mention}({next(alt_emoji)}) Loses \n \n {joinedBoard[0]} \n {joinedBoard[1]} \n {joinedBoard[2]} \n {joinedBoard[3]} \n {joinedBoard[4]} \n {joinedBoard[5]} \n {joinedBoard[6]}'
                        embed.set_footer(text='')
                        await sent_embed.edit(embed=embed)
                        await sent_embed.clear_reactions()

            # Unbeatable? Mode #
            if reaction.emoji == ' ':   # 💢

                # Player vs AI Variables #
                depth = 7
                botTime = 10
                pTime = 0
                p2 = self.bot.user
                pList = [p1, p2]
                random.shuffle(pList)
                alt_player = cycle(pList)
                longestTime = 0
                prevNodes = 0
                lowestScore = 0
                highestScore = 0
                thinking_shortened = False
                odd = False
                if (next(alt_player) != self.bot.user):
                    odd = True
                ConnectFourAI.firstPlayer = next(alt_player)


                # Loading Connect4 #
                embed.set_author(name='Connect Four (Smart Mode)', icon_url='https://cdn.discordapp.com/attachments/488700267060133889/699343937965654122/ezgif-7-6d4bab9dedb9.gif')
                embed.description = 'Loading...'
                await sent_embed.edit(embed=embed)
                for emoji in reactions:
                    await sent_embed.add_reaction(emoji)
                sent_embed = await self.bot.get_channel(ctx.channel.id).fetch_message(sent_embed.id)

                # Actual Game #
                while working:
                    current_player = next(alt_player)
                    current_mark = next(alt_mark)
                    current_emoji = ConnectFourAI.convert(current_mark)
                    other_player = next(alt_player)
                    other_mark = next(alt_mark)
                    other_emoji = ConnectFourAI.convert(other_mark)
                    next(alt_player)
                    next(alt_mark)

                    ConnectFourAI.convertBoard(board, simple=False)
                    joinedBoard = ["|".join(reactions), "|".join(board[0]), "|".join(board[1]), "|".join(board[2]), "|".join(board[3]), "|".join(board[4]), "|".join(board[5])]
                    ConnectFourAI.convertBoard(board, simple=True)

                    if current_player == self.bot.user:
                        currentHeursitic = ConnectFourAI.boardHeuristic(board, current_mark, other_mark, odd)
                    else:
                        currentHeursitic = ConnectFourAI.boardHeuristic(board, other_mark, current_mark, odd)

                    if currentHeursitic < lowestScore:
                        lowestScore = currentHeursitic
                    elif currentHeursitic > highestScore:
                        highestScore = currentHeursitic
                    if botTime > longestTime:
                        longestTime = botTime

                    # Player's turn
                    if current_player == p1:
                        ConnectFourAI.convertBoard(board, simple=False)
                        embed.description = f'{p1.mention}({current_emoji}) Make your move \n \n Current bot score: {currentHeursitic} \n \n I took **{botTime} seconds** \n \n I explored **{prevNodes} nodes** \n \n depth = {depth} \n \n {joinedBoard[0]} \n {joinedBoard[1]} \n {joinedBoard[2]} \n {joinedBoard[3]} \n {joinedBoard[4]} \n {joinedBoard[5]} \n {joinedBoard[6]}'
                        embed.set_footer(text='Move not registering? Try double tapping')
                        await sent_embed.edit(embed=embed)
                        start = time.time()
                        reaction, user = await self.bot.wait_for('reaction_add', timeout=300.0, check=check_reaction)
                        end = time.time()
                        pTime = round(end - start, 2)
                        await sent_embed.remove_reaction(reaction.emoji, user)
                        for i, emoji in enumerate(reactions):
                            if emoji == reaction.emoji:
                                for list in reversed(board):
                                    if list[i] == '⚪':
                                        list[i] = ConnectFourAI.convert(current_mark)
                                        break
                        if botTime < 6 and not thinking_shortened:
                            depth += 1


                    # AI's turn
                    elif current_player == p2:
                        ConnectFourAI.convertBoard(board, simple=True)
                        embed.description = f'{p2.mention}({current_emoji}) is thinking... \n \n Current bot score: {currentHeursitic} \n \n You took **{pTime} seconds** \n \n {joinedBoard[0]} \n {joinedBoard[1]} \n {joinedBoard[2]} \n {joinedBoard[3]} \n {joinedBoard[4]} \n {joinedBoard[5]} \n {joinedBoard[6]}'
                        await sent_embed.edit(embed=embed)
                        start = time.time()
                        move, shortened, nodesExplored = ConnectFourAI.bestMove(board=board, botMark=current_mark, pMark=other_mark, depth=depth, odd = odd)
                        prevNodes = nodesExplored
                        board[move[0]][move[1]] = current_mark
                        thinking_shortened = shortened
                        end = time.time()
                        botTime = round(end - start, 2)

                    # Evaluate Board #
                    ConnectFourAI.convertBoard(board, simple=False)
                    joinedBoard = ["|".join(reactions), "|".join(board[0]), "|".join(board[1]), "|".join(board[2]), "|".join(board[3]), "|".join(board[4]), "|".join(board[5])]
                    ConnectFourAI.convertBoard(board, simple=True)
                    result = ConnectFourAI.checkBoardWin(board)
                    if result == 'TIE':
                        working = False
                        embed.description = f'Tie between {current_player.mention}({current_emoji}) and {other_player.mention}({other_emoji}) \n \n My **highest score** was **{highestScore}** \n My **lowest score** was **{lowestScore}** \n My **longest move** took **{longestTime} seconds** \n \n {joinedBoard[0]} \n {joinedBoard[1]} \n {joinedBoard[2]} \n {joinedBoard[3]} \n {joinedBoard[4]} \n {joinedBoard[5]} \n {joinedBoard[6]}'
                        embed.set_footer(text='')
                        await sent_embed.edit(embed=embed)
                        await sent_embed.clear_reactions()
                    elif result in ['X', 'O']:
                        working = False
                        embed.description = f'{current_player.mention}({current_emoji}) Wins \n {other_player.mention}({other_emoji}) Loses \n \n My **highest score** was **{highestScore}** \n My **lowest score** was **{lowestScore}** \n My **longest move** took **{longestTime} seconds** \n \n {joinedBoard[0]} \n {joinedBoard[1]} \n {joinedBoard[2]} \n {joinedBoard[3]} \n {joinedBoard[4]} \n {joinedBoard[5]} \n {joinedBoard[6]}'
                        embed.set_footer(text='')
                        await sent_embed.edit(embed=embed)
                        await sent_embed.clear_reactions()


def setup(bot):
    bot.add_cog(Connect4(bot))

