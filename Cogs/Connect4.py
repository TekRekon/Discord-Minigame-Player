from discord.ext import commands
from Cogs.Tools import ConnectFourAI, Connect4DatabaseTools
from itertools import cycle
import asyncio, randfacts, psycopg2, time, random, discord


class Connect4(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def leaderboard(self, ctx):
        p_scores = Connect4DatabaseTools.fetchRankedStats()

        embed = discord.Embed(description='\u200b', color=0xff0000)
        embed.set_author(name=f'Connect Four Leaderboard', icon_url='https://cdn.discordapp.com/attachments/488700267060133889/779444906464247828/2e4e7e76e454f56b24d6883b93afb7932.jpg')
        embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/488700267060133889/779118212850909184/ezgif-3-814c4634232b.gif')
        for k, x in enumerate(p_scores):
            if k == 0:
                embed.add_field(name=f'🥇: {x[0]} | %{x[1]}', value='\u200b', inline=False)
            elif k == 1:
                embed.add_field(name=f'🥈: {x[0]} | %{x[1]}', value='\u200b', inline=False)
            elif k == 2:
                embed.add_field(name=f'🥉: {x[0]} | %{x[1]}', value='\u200b', inline=False)
            else:
                embed.add_field(name=f'**{k+1}**: {x[0]} | %{x[1]}', value='\u200b', inline=False)

        embed.set_footer(text='Play a minimum of 10 matches to get ranked')
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def profile(self, ctx, arg: discord.Member):
        con = psycopg2.connect("postgres://tmneuvqnzogsxo:d15b738ee44cc1429e2cf014bf3c1df8448fea2b0155a4157e8e2a37dbc0d495@ec2-54-146-142-58.compute-1.amazonaws.com:5432/d3ad8vk1so3cfu")
        cur = con.cursor()

        cur.execute("SELECT user_id FROM playerConnect4Stats")
        rows = cur.fetchall()

        if arg.id not in [i[0] for i in rows]:
            embed = discord.Embed(title=f'{arg.name} does not exist in my database', color=0xff0000)
            embed.set_author(name='Null Profile', icon_url=arg.avatar_url)
            embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/488700267060133889/779526483202932777/9bec831078051d4fc5f06e964da71760.gif')
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(description='\u200b', color=0xff0000)
            embed.set_author(name=f'{arg.name}\'s Profile', icon_url=arg.avatar_url)
            embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/488700267060133889/779526483202932777/9bec831078051d4fc5f06e964da71760.gif')

            cur.execute("SELECT wins, losses FROM playerConnect4Stats WHERE user_id = %s", [arg.id])
            row = cur.fetchall()
            wins = row[0][0]
            losses = row[0][1]

            embed.add_field(name='🏆 **Wins**', value=f'{wins}', inline=True)
            embed.add_field(name='☠ **Losses**', value=f'{losses}', inline=True)

            if wins + losses == 0:
                embed.add_field(name='💠 **Win %**', value='N/A', inline=True)
            elif wins == 0:
                embed.add_field(name='💠 **Win %**', value='0', inline=True)
            elif losses == 0:
                embed.add_field(name='💠 **Win %**', value='100', inline=True)
            else:
                embed.add_field(name='💠 **Win %**', value=f'{round((wins/(losses+wins)*100), 2)}', inline=True)

            ranked_scores = Connect4DatabaseTools.fetchRankedStats()
            IDs = [tuple[2] for tuple in ranked_scores]
            winrates = [tuple[1] for tuple in ranked_scores]
            if arg.id in IDs:
                i = IDs.index(arg.id)
                embed.add_field(name='⚜ **Rank**', value=f'{i+1}', inline=False)
                if i == 0:
                    embed.add_field(name='📡 **Wins -> Next Rank**', value='0', inline=True)
                else:
                    target_winrate = winrates[i-1]
                    current_winrate = winrates[i]
                    print(target_winrate, current_winrate)
                    current_wins = Connect4DatabaseTools.getPlayerStat(arg.id, "wins")
                    current_losses = Connect4DatabaseTools.getPlayerStat(arg.id, "losses")
                    f = 0
                    while target_winrate > current_winrate:
                        f += 1
                        current_winrate = round((current_wins+f)/(current_wins+current_losses)*100, 2)
                    embed.add_field(name='📡 **Wins -> Next Rank**', value=f'{f}', inline=True)

            await ctx.send(embed=embed)

        cur.close()
        con.close()

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def connect4(self, ctx):
        Connect4DatabaseTools.addPlayer(ctx.author.id, ctx.author.name)

        def check_reaction(reaction, user):
            if reaction.emoji in ['🤖', '💢', '✅', '❌']:
                return reaction.message.id == sent_embed.id and user == ctx.author
            if reaction.emoji == '📲':
                return reaction.message.id == sent_embed.id and user != ctx.author and user != self.bot.user
            if reaction.emoji in reactions:
                for k, emoji in enumerate(reactions):
                    if emoji == reaction.emoji:
                        if board[0][k] == '⚪':
                            return reaction.message.id == sent_embed.id and user == current_player
            return False

        # Universal Variables #
        reactions = ['🇦', '🇧', '🇨', '🇩', '🇪', '🇫', '🇬']
        # board = [['⚪']*7 for i in range(6)]
        board = [['⚪', '⚪', '⚪', '⚪', '⚪', '⚪', '⚪'],  # board[0][0-6]
                 ['⚪', '⚪', '⚪', '⚪', '⚪', '⚪', '⚪'],  # board[1][0-6}
                 ['⚪', '⚪', '⚪', '⚪', '⚪', '⚪', '⚪'],
                 ['⚪', '⚪', '⚪', '⚪', '⚪', '⚪', '⚪'],
                 ['⚪', '⚪', '⚪', '⚪', '⚪', '⚪', '⚪'],
                 ['⚪', '⚪', '⚪', '⚪', '⚪', '⚪', '⚪']]
        p1 = ctx.author
        emoji_list = ['🔵', '🔴']
        random.shuffle(emoji_list)
        alt_emoji = cycle(emoji_list)
        loading_gifs = ['https://cdn.discordapp.com/attachments/488700267060133889/779516535425335307/giphy.gif',
                        'https://cdn.discordapp.com/attachments/488700267060133889/779518931085819984/gifntext-gif.gif',
                        'https://cdn.discordapp.com/attachments/488700267060133889/779518965923184641/tvnJsU7.gif',
                        'https://cdn.discordapp.com/attachments/488700267060133889/779518988194938960/giphy_1.gif',
                        'https://cdn.discordapp.com/attachments/488700267060133889/779519005941170186/custom-loading-icon.gif',
                        'https://cdn.discordapp.com/attachments/488700267060133889/779519030301294592/giphy_2.gif',
                        'https://cdn.discordapp.com/attachments/488700267060133889/779519058936070164/thA1t5G.gif',
                        'https://cdn.discordapp.com/attachments/488700267060133889/779519089998692372/giphy_3.gif',
                        'https://cdn.discordapp.com/attachments/488700267060133889/779519118672003072/giphy-downsized.gif',
                        'https://cdn.discordapp.com/attachments/488700267060133889/779519144869494804/187917b0606c80a6c295da1f19ff3e40.gif',
                        'https://cdn.discordapp.com/attachments/488700267060133889/779519172622155806/7dfd95dd9ad07e7af1eaff34a890b322.gif']
        working = True

        # Options Menu #
        embed = discord.Embed(description=f'{ctx.author.mention} is waiting... \n 📲: **Join the game**', color=0xff0000)
        embed.set_author(name='Connect Four', icon_url='https://cdn.discordapp.com/attachments/488700267060133889/699343937965654122/ezgif-7-6d4bab9dedb9.gif')
        sent_embed = await ctx.send(embed=embed)
        await sent_embed.add_reaction('📲')
        reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=check_reaction)
        await sent_embed.clear_reactions()

        if reaction.emoji == '📲':
            p2 = user
            # Ask if they accept
            embed.description = f'{ctx.author.mention}, accept a game with {user.mention}?'
            await sent_embed.edit(embed=embed)
            await sent_embed.add_reaction('✅')
            await sent_embed.add_reaction('❌')
            reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=check_reaction)
            if reaction.emoji == '❌':
                embed.description = f'{ctx.author.mention} chickened out of a game with {p2.mention}'
                await sent_embed.edit(embed=embed)
                await sent_embed.clear_reactions()
                return
        await sent_embed.clear_reactions()


        # Loading Connect4 #
        embed.set_author(name='Connect Four', icon_url='https://cdn.discordapp.com/attachments/488700267060133889/699343937965654122/ezgif-7-6d4bab9dedb9.gif')
        embed.description = 'Loading...'
        embed.set_thumbnail(url=random.choice(loading_gifs))
        await sent_embed.edit(embed=embed)
        for emoji in reactions:
            await sent_embed.add_reaction(emoji)
        sent_embed = await self.bot.get_channel(ctx.channel.id).fetch_message(sent_embed.id)

        if reaction.emoji == '✅':
            Connect4DatabaseTools.addPlayer(user.id, user.name)
            embed.set_thumbnail(url='')

            # Player vs player exclusive variables #
            p_list = [p1, p2]
            random.shuffle(p_list)
            alt_player = cycle(p_list)
            time_taken = 0
            p1_total_time = 0
            p2_total_time = 0
            p1_turns = 0
            p2_turns = 0


            # Actual Game #
            while working:
                current_player = next(alt_player)
                current_emoji = next(alt_emoji)
                other_player = next(alt_player)
                other_emoji = next(alt_emoji)
                next(alt_player)
                next(alt_emoji)
                joined_board = ["|".join(reactions), "|".join(board[0]), "|".join(board[1]), "|".join(board[2]), "|".join(board[3]), "|".join(board[4]), "|".join(board[5])]
                fact = randfacts.getFact(filter=False)
                connect4_tips = ['Move not registering? Try double tapping.', 'The middle column and row are the most valuable.', 'Try learning the Odd-Even Strategy.', 'You\'re looking mighty fine today', 'You have 5 minutes to make a move before receiving a loss.', fact, 'Don\'t fat-finger the reactions.']

                # Player's turn
                embed.description = f'{current_player.mention}({current_emoji}) Make your move \n \n {other_player.mention}({other_emoji}) took {time_taken} seconds \n \n \n {joined_board[0]} \n {joined_board[1]} \n {joined_board[2]} \n {joined_board[3]} \n {joined_board[4]} \n {joined_board[5]} \n {joined_board[6]}'
                embed.set_footer(text=random.choice(connect4_tips))
                await sent_embed.edit(embed=embed)

                try:
                    start = time.time()
                    reaction, user = await self.bot.wait_for('reaction_add', timeout=300.0, check=check_reaction)
                    end = time.time()
                    time_taken = round(end - start, 2)
                except asyncio.TimeoutError:
                    embed.description = f'{other_player.mention}({other_emoji}) Wins \n {current_player.mention}({current_emoji}) Loses \n \n {joined_board[0]} \n {joined_board[1]} \n {joined_board[2]} \n {joined_board[3]} \n {joined_board[4]} \n {joined_board[5]} \n {joined_board[6]}'
                    embed.set_footer(text='')
                    await sent_embed.edit(embed=embed)
                    await sent_embed.clear_reactions()
                    Connect4DatabaseTools.editPlayerScore(current_player.id, False)
                    Connect4DatabaseTools.editPlayerScore(other_player.id, True)
                    return

                await sent_embed.remove_reaction(reaction.emoji, user)
                for i, emoji in enumerate(reactions):
                    if emoji == reaction.emoji:
                        for list in reversed(board):
                            if list[i] == '⚪':
                                list[i] = current_emoji
                                break

                # Evaluate Board #
                joined_board = ["|".join(reactions), "|".join(board[0]), "|".join(board[1]), "|".join(board[2]), "|".join(board[3]), "|".join(board[4]), "|".join(board[5])]
                result = ConnectFourAI.checkBoardWin(board)
                if result == 'TIE':
                    working = False
                    Connect4DatabaseTools.editPlayerScore(current_player.id, True)
                    Connect4DatabaseTools.editPlayerScore(other_player.id, True)
                    embed.description = f'Tie between {current_player.mention}({current_emoji}) and {other_player.mention}({other_emoji}) \n \n {joined_board[0]} \n {joined_board[1]} \n {joined_board[2]} \n {joined_board[3]} \n {joined_board[4]} \n {joined_board[5]} \n {joined_board[6]}'
                    embed.set_footer(text='')
                    await sent_embed.edit(embed=embed)
                    await sent_embed.clear_reactions()
                elif result in ['🔴', '🔵']:
                    working = False
                    Connect4DatabaseTools.editPlayerScore(current_player.id, True)
                    Connect4DatabaseTools.editPlayerScore(other_player.id, False)
                    embed.description = f'{current_player.mention}({current_emoji}) Wins \n {other_player.mention}({other_emoji}) Loses \n \n {joined_board[0]} \n {joined_board[1]} \n {joined_board[2]} \n {joined_board[3]} \n {joined_board[4]} \n {joined_board[5]} \n {joined_board[6]}'
                    embed.set_footer(text='')
                    await sent_embed.edit(embed=embed)
                    await sent_embed.clear_reactions()

        # Unbeatable? Mode #
        if reaction.emoji == ' ':  # 💢

            # Player vs AI Exclusive Variables #
            depth = 7
            bot_time = 10
            p_time = 0
            p_list = [p1, self.bot.user]
            random.shuffle(p_list)
            alt_player = cycle(p_list)
            longest_time = 0
            prev_nodes = 0
            lowest_score = 0
            highest_score = 0
            thinking_shortened = False
            odd = False
            if next(alt_player) == self.bot.user:
                odd = True
            next(alt_player)

            # Actual Game #
            while working:
                current_player = next(alt_player)
                current_emoji = next(alt_emoji)
                other_player = next(alt_player)
                other_emoji = next(alt_emoji)
                next(alt_player)
                next(alt_emoji)
                joined_board = ["|".join(reactions), "|".join(board[0]), "|".join(board[1]), "|".join(board[2]), "|".join(board[3]), "|".join(board[4]), "|".join(board[5])]

                if current_player == self.bot.user:
                    current_heursitic = ConnectFourAI.boardHeuristic(board, current_emoji, other_emoji, odd)
                else:
                    current_heursitic = ConnectFourAI.boardHeuristic(board, other_emoji, current_emoji, odd)

                if current_heursitic < lowest_score:
                    lowest_score = current_heursitic
                elif current_heursitic > highest_score:
                    highest_score = current_heursitic
                if bot_time > longest_time:
                    longest_time = bot_time

                # Player's turn
                if current_player == p1:
                    embed.description = f'{p1.mention}({current_emoji}) Make your move \n \n Current bot score: {current_heursitic} \n \n I took **{bot_time} seconds** \n \n I explored **{prev_nodes} nodes** \n \n depth = {depth} \n \n {joined_board[0]} \n {joined_board[1]} \n {joined_board[2]} \n {joined_board[3]} \n {joined_board[4]} \n {joined_board[5]} \n {joined_board[6]}'
                    await sent_embed.edit(embed=embed)
                    start = time.time()
                    reaction, user = await self.bot.wait_for('reaction_add', timeout=300.0, check=check_reaction)
                    end = time.time()
                    p_time = round(end - start, 2)
                    await sent_embed.remove_reaction(reaction.emoji, user)
                    for i, emoji in enumerate(reactions):
                        if emoji == reaction.emoji:
                            for list in reversed(board):
                                if list[i] == '⚪':
                                    list[i] = current_emoji
                                    break
                    if bot_time < p_time and not thinking_shortened:
                        depth += 1

                # AI's Turn #
                elif current_player == self.bot.user:
                    embed.description = f'{self.bot.user.mention}({current_emoji}) is thinking... \n \n Current bot score: {current_heursitic} \n \n You took **{p_time} seconds** \n \n {joined_board[0]} \n {joined_board[1]} \n {joined_board[2]} \n {joined_board[3]} \n {joined_board[4]} \n {joined_board[5]} \n {joined_board[6]}'
                    await sent_embed.edit(embed=embed)
                    start = time.time()
                    move, shortened, nodes_explored = ConnectFourAI.bestMove(board=board, botMark=current_emoji, pMark=other_emoji, depth=depth, odd=odd)
                    prev_nodes = nodes_explored
                    board[move[0]][move[1]] = current_emoji
                    thinking_shortened = shortened
                    end = time.time()
                    bot_time = round(end - start, 2)

                # Evaluate Board #
                joined_board = ["|".join(reactions), "|".join(board[0]), "|".join(board[1]), "|".join(board[2]), "|".join(board[3]), "|".join(board[4]), "|".join(board[5])]
                result = ConnectFourAI.checkBoardWin(board)
                if result == 'TIE':
                    working = False
                    embed.description = f'Tie between {current_player.mention}({current_emoji}) and {other_player.mention}({other_emoji}) \n \n My **highest score** was **{highest_score}** \n My **lowest score** was **{lowest_score}** \n My **longest move** took **{longest_time} seconds** \n \n {joined_board[0]} \n {joined_board[1]} \n {joined_board[2]} \n {joined_board[3]} \n {joined_board[4]} \n {joined_board[5]} \n {joined_board[6]}'
                    embed.set_footer(text='')
                    await sent_embed.edit(embed=embed)
                    await sent_embed.clear_reactions()
                elif result in ['🔴', '🔵']:
                    working = False
                    embed.description = f'{current_player.mention}({current_emoji}) Wins \n {other_player.mention}({other_emoji}) Loses \n \n My **highest score** was **{highest_score}** \n My **lowest score** was **{lowest_score}** \n My **longest move** took **{longest_time} seconds** \n \n {joined_board[0]} \n {joined_board[1]} \n {joined_board[2]} \n {joined_board[3]} \n {joined_board[4]} \n {joined_board[5]} \n {joined_board[6]}'
                    embed.set_footer(text='')
                    await sent_embed.edit(embed=embed)
                    await sent_embed.clear_reactions()


def setup(bot):
    bot.add_cog(Connect4(bot))
