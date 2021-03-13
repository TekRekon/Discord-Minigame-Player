from discord.ext import commands
from Cogs.Tools import DatabaseTools
from itertools import cycle
import asyncio, randfacts, random, discord


class Connect4(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.guild_only()
    @commands.bot_has_permissions(manage_messages=True)
    async def othello(self, ctx):

        def get_flanked(board, n, i):
            changeList = []

            changes = []
            indexn = n+2
            if n+1 < 8 and board[n+1][i] == other_emoji:
                changes.append((n+1, i))
                while indexn < 8:
                    if board[indexn][i] == '🟩':
                        break
                    if board[indexn][i] == current_emoji:
                        changeList.append(changes)
                        break
                    changes.append((indexn, i))
                    indexn += 1

            changes = []
            indexn = n-2
            if n-1 >= 0 and board[n-1][i] == other_emoji:
                changes.append((n-1, i))
                while indexn >= 0:
                    if board[indexn][i] == '🟩':
                        break
                    if board[indexn][i] == current_emoji:
                        changeList.append(changes)
                        break
                    changes.append((indexn, i))
                    indexn -= 1

            changes = []
            indexi = i-2
            if i-1 >= 0 and board[n][i-1] == other_emoji:
                changes.append((n, i-1))
                while indexi >= 0:
                    if board[n][indexi] == '🟩':
                        break
                    if board[n][indexi] == current_emoji:
                        changeList.append(changes)
                        break
                    changes.append((n, indexi))
                    indexi -= 1

            changes = []
            indexi = i-2
            if i-1 >= 0 and board[n][i-1] == other_emoji:
                changes.append((n, i-1))
                while indexi >= 0:
                    if board[n][indexi] == '🟩':
                        break
                    if board[n][indexi] == current_emoji:
                        changeList.append(changes)
                        break
                    changes.append((n, indexi))
                    indexi -= 1

            changes = []
            indexi = i+2
            if i+1 < 8 and board[n][i+1] == other_emoji:
                changes.append((n, i+1))
                while indexi < 8:
                    if board[n][indexi] == '🟩':
                        break
                    if board[n][indexi] == current_emoji:
                        changeList.append(changes)
                        break
                    changes.append((n, indexi))
                    indexi += 1

            changes = []
            indexi = i+2
            indexn = n+2
            if i+1 < 8 and n+1 < 8 and board[n+1][i+1] == other_emoji:
                changes.append((n+1, i+1))
                while indexi < 8 and indexn < 8:
                    if board[indexn][indexi] == '🟩':
                        break
                    if board[indexn][indexi] == current_emoji:
                        changeList.append(changes)
                        break
                    changes.append((indexn, indexi))
                    indexi += 1
                    indexn += 1

            changes = []
            indexi = i-2
            indexn = n+2
            if i-1 >= 0 and n+1 < 8 and board[n+1][i-1] == other_emoji:
                changes.append((n+1, i-1))
                while indexi >= 0 and indexn < 8:
                    if board[indexn][indexi] == '🟩':
                        break
                    if board[indexn][indexi] == current_emoji:
                        changeList.append(changes)
                        break
                    changes.append((indexn, indexi))
                    indexi -= 1
                    indexn += 1

            changes = []
            indexi = i+2
            indexn = n-2
            if i+1 < 8 and n-1 >= 0 and board[n-1][i+1] == other_emoji:
                changes.append((n-1, i+1))
                while indexi < 8 and indexn >= 0:
                    if board[indexn][indexi] == '🟩':
                        break
                    if board[indexn][indexi] == current_emoji:
                        changeList.append(changes)
                        break
                    changes.append((indexn, indexi))
                    indexi += 1
                    indexn -= 1

            changes = []
            indexi = i-2
            indexn = n-2
            if i-1 >= 0 and n-1 >= 0 and board[n-1][i-1] == other_emoji:
                changes.append((n-1, i-1))
                while indexi >= 0 and indexn >= 0:
                    if board[indexn][indexi] == '🟩':
                        break
                    if board[indexn][indexi] == current_emoji:
                        changeList.append(changes)
                        break
                    changes.append((indexn, indexi))
                    indexi -= 1
                    indexn -= 1

            return changeList

        def check_reaction(reaction, user):
            if reaction.emoji in ['🤖', '✅', '❌']:
                return reaction.message.id == sent_embed.id and user == ctx.author
            if reaction.emoji == '📲':
                return reaction.message.id == sent_embed.id and user != ctx.author and user != self.bot.user
            return False

        def check_alpha_reaction(reaction, user):
            if reaction.emoji in reactions1:
                if '🟩' in board[reactions1reversed.index(reaction.emoji)]:
                    return reaction.message.id == sent_embed.id and user == current_player
            elif reaction.emoji == '⏩':
                return reaction.message.id == sent_embed.id and user == current_player
            return False

        def check_numeric_reaction(reaction, user):
            if reaction.emoji in reactions2:
                if board[reactions1reversed.index(reaction_alpha.emoji)][reactions2.index(reaction.emoji)] == '🟩':
                    if reaction.message.id == sent_embed.id and user == current_player:
                        return True
            elif reaction.emoji == '⏩':
                return reaction.message.id == sent_embed.id and user == current_player
            return False

        # Universal Variables #
        reactions1 = ['🇦', '🇧', '🇨', '🇩', '🇪', '🇫', '🇬', '🇭']
        reactions1reversed = ['🇭', '🇬', '🇫', '🇪', '🇩', '🇨', '🇧', '🇦']
        reactions2 = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣']
        # board = [['⚪']*7 for i in range(6)]
        board = [['🟩', '🟩', '🟩', '🟩', '🟩', '🟩', '🟩', '🟩'],
                 ['🟩', '🟩', '🟩', '🟩', '🟩', '🟩', '🟩', '🟩'],
                 ['🟩', '🟩', '🟩', '🟩', '🟩', '🟩', '🟩', '🟩'],
                 ['🟩', '🟩', '🟩', '⚪', '⚫', '🟩', '🟩', '🟩'],
                 ['🟩', '🟩', '🟩', '⚫', '⚪', '🟩', '🟩', '🟩'],
                 ['🟩', '🟩', '🟩', '🟩', '🟩', '🟩', '🟩', '🟩'],
                 ['🟩', '🟩', '🟩', '🟩', '🟩', '🟩', '🟩', '🟩'],
                 ['🟩', '🟩', '🟩', '🟩', '🟩', '🟩', '🟩', '🟩']]
        p1 = ctx.author
        emoji_list = ['⚫', '⚪']
        random.shuffle(emoji_list)
        alt_emoji = cycle(emoji_list)
        working = True

        # Options Menu #
        # TODO add prompt timed out exceptions
        embed = discord.Embed(description=f'{ctx.author.mention} is waiting... \n 📲: **Join the game**', color=0x2596be)
        embed.set_author(name='Othello', icon_url='https://cdn.discordapp.com/attachments/488700267060133889/806228103323189268/a410e8bb83f1a7230d330b912d9eb895_w200.gif')
        sent_embed = await ctx.send(embed=embed)
        await sent_embed.add_reaction('📲')
        reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=check_reaction)
        await sent_embed.clear_reactions()

        # TODO Add AI option
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
            elif reaction.emoji == '✅':

                me = self.bot.get_user(285879705989677058)
                await me.send(f"othello game initiated")

                # Loading Connect4 #
                await sent_embed.clear_reactions()
                embed.description = 'Loading...'
                await sent_embed.edit(embed=embed)
                for emoji in reactions1:
                    await sent_embed.add_reaction(emoji)
                for emoji in reactions2:
                    await sent_embed.add_reaction(emoji)
                await sent_embed.add_reaction('⏩')
                sent_embed = await self.bot.get_channel(ctx.channel.id).fetch_message(sent_embed.id)


                # Player vs player exclusive variables #
                global moves
                moves = []
                p_list = [p1, p2]
                random.shuffle(p_list)
                alt_player = cycle(p_list)
                moves = 0
                othello_tips = ['Move not registering? Try double tapping.', 'A minute to learn, a lifetime to master. ', 'You have 3 minutes to make a move before receiving a loss.', randfacts.getFact(filter=True), 'Don\'t fat-finger the reactions.']
                embed.set_footer(text=random.choice(othello_tips))

                # Actual Game #
                while working:
                    current_player = next(alt_player)
                    current_emoji = next(alt_emoji)
                    other_player = next(alt_player)
                    other_emoji = next(alt_emoji)
                    next(alt_player)
                    next(alt_emoji)
                    joined_board = ["|".join(board[0]), "|".join(board[1]), "|".join(board[2]), "|".join(board[3]), "|".join(board[4]), "|".join(board[5]), "|".join(board[6]), "|".join(board[7]), '⬛' + '|' + "|".join(reactions2)]
                    for i in range(len(board)):
                        joined_board[i] = reactions1reversed[i] + '|' + joined_board[i]

                    # Player's turn
                    embed.description = f'{current_player.mention}({current_emoji}) Make your move (Choose a letter) \n \n {joined_board[0]} \n {joined_board[1]} \n {joined_board[2]} \n {joined_board[3]} \n {joined_board[4]} \n {joined_board[5]} \n {joined_board[6]} \n {joined_board[7]} \n {joined_board[8]}'
                    if moves % 5 == 0:
                        embed.set_footer(text=random.choice(othello_tips))
                    await sent_embed.edit(embed=embed)

                    try:
                        reacting = True
                        cont = True
                        while reacting:

                            reaction_alpha, user = await self.bot.wait_for('reaction_add', timeout=180.0, check=check_alpha_reaction)
                            if reaction_alpha.emoji == '⏩':
                                reacting = False
                                break

                            embed.description = f'{current_player.mention}({current_emoji}) Make your move (Choose a number) \n \n {joined_board[0]} \n {joined_board[1]} \n {joined_board[2]} \n {joined_board[3]} \n {joined_board[4]} \n {joined_board[5]} \n {joined_board[6]} \n {joined_board[7]} \n {joined_board[8]}'
                            await sent_embed.edit(embed=embed)
                            reaction_numeric, user = await self.bot.wait_for('reaction_add', timeout=180.0, check=check_numeric_reaction)
                            if reaction_numeric.emoji == '⏩':
                                reacting = False
                                break

                            n = reactions1reversed.index(reaction_alpha.emoji)
                            i = reactions2.index(reaction_numeric.emoji)
                            changeList = get_flanked(board, n, i)
                            if changeList:
                                board[n][i] = current_emoji
                                for changes in changeList:
                                    for change in changes:
                                        board[change[0]][change[1]] = current_emoji
                                reacting = False
                            else:
                                embed.description = f'{current_player.mention}({current_emoji}) Invalid move, try again (Choose a letter or forfeit your move ⏩) \n \n {joined_board[0]} \n {joined_board[1]} \n {joined_board[2]} \n {joined_board[3]} \n {joined_board[4]} \n {joined_board[5]} \n {joined_board[6]} \n {joined_board[7]} \n {joined_board[8]}'
                                await sent_embed.edit(embed=embed)
                                continue


                    except asyncio.TimeoutError:
                        embed.description = f'{other_player.mention}({other_emoji}) Wins \n {current_player.mention}({current_emoji}) Loses \n \n Player turn timed out \n \n {joined_board[0]} \n {joined_board[1]} \n {joined_board[2]} \n {joined_board[3]} \n {joined_board[4]} \n {joined_board[5]} \n {joined_board[6]} \n {joined_board[7]} \n {joined_board[8]}'
                        embed.set_footer(text='')
                        await sent_embed.edit(embed=embed)
                        await sent_embed.clear_reactions()
                        DatabaseTools.addPlayer(current_player.id, current_player.name, 'othello')
                        DatabaseTools.addPlayer(other_player.id, other_player.name, 'othello')
                        DatabaseTools.editPlayerScore(current_player.id, False, 'othello')
                        DatabaseTools.editPlayerScore(other_player.id, True, 'othello')
                        return

                    moves += 1

                    if not any(current_emoji in sublist for sublist in board):
                        working = False
                        joined_board = ["|".join(board[0]), "|".join(board[1]), "|".join(board[2]), "|".join(board[3]), "|".join(board[4]), "|".join(board[5]), "|".join(board[6]), "|".join(board[7]), '⬛' + '|' + "|".join(reactions2)]
                        for i in range(len(board)):
                            joined_board[i] = reactions1reversed[i] + '|' + joined_board[i]
                        DatabaseTools.addPlayer(current_player.id, current_player.name, 'othello')
                        DatabaseTools.addPlayer(other_player.id, other_player.name, 'othello')
                        DatabaseTools.editPlayerScore(current_player.id, False, 'othello')
                        DatabaseTools.editPlayerScore(other_player.id, True, 'othello')
                        embed.description = f'{current_player.mention}({current_emoji}) Loses \n {other_player.mention}({other_emoji}) Wins \n \n {joined_board[0]} \n {joined_board[1]} \n {joined_board[2]} \n {joined_board[3]} \n {joined_board[4]} \n {joined_board[5]} \n {joined_board[6]} \n {joined_board[7]}'
                        await sent_embed.edit(embed=embed)

                    if not any(other_emoji in sublist for sublist in board):
                        working = False
                        joined_board = ["|".join(board[0]), "|".join(board[1]), "|".join(board[2]), "|".join(board[3]), "|".join(board[4]), "|".join(board[5]), "|".join(board[6]), "|".join(board[7]), '⬛' + '|' + "|".join(reactions2)]
                        for i in range(len(board)):
                            joined_board[i] = reactions1reversed[i] + '|' + joined_board[i]
                        DatabaseTools.addPlayer(current_player.id, current_player.name, 'othello')
                        DatabaseTools.addPlayer(other_player.id, other_player.name, 'othello')
                        DatabaseTools.editPlayerScore(current_player.id, True, 'othello')
                        DatabaseTools.editPlayerScore(other_player.id, False, 'othello')
                        embed.description = f'{current_player.mention}({current_emoji}) Wins \n {other_player.mention}({other_emoji}) Loses \n \n {joined_board[0]} \n {joined_board[1]} \n {joined_board[2]} \n {joined_board[3]} \n {joined_board[4]} \n {joined_board[5]} \n {joined_board[6]} \n {joined_board[7]}'
                        await sent_embed.edit(embed=embed)


                    if not any('🟩' in sublist for sublist in board):
                        DatabaseTools.addPlayer(current_player.id, current_player.name, 'othello')
                        DatabaseTools.addPlayer(other_player.id, other_player.name, 'othello')
                        working = False
                        joined_board = ["|".join(board[0]), "|".join(board[1]), "|".join(board[2]), "|".join(board[3]), "|".join(board[4]), "|".join(board[5]), "|".join(board[6]), "|".join(board[7]), '⬛' + '|' + "|".join(reactions2)]
                        for i in range(len(board)):
                            joined_board[i] = reactions1reversed[i] + '|' + joined_board[i]
                        black = 0
                        white = 0
                        for list in board:
                            for cell in list:
                                if cell == '⚫':
                                    black += 1
                                if cell == '⚪':
                                    white += 1
                        if white > black:
                            if current_emoji == '⚫':
                                DatabaseTools.editPlayerScore(current_player.id, False, 'othello')
                                DatabaseTools.editPlayerScore(other_player.id, True, 'othello')
                                embed.description = f'{current_player.mention}({current_emoji}) Loses \n {other_player.mention}({other_emoji}) Wins \n \n {joined_board[0]} \n {joined_board[1]} \n {joined_board[2]} \n {joined_board[3]} \n {joined_board[4]} \n {joined_board[5]} \n {joined_board[6]} \n {joined_board[7]}'
                            else:
                                DatabaseTools.editPlayerScore(current_player.id, True, 'othello')
                                DatabaseTools.editPlayerScore(other_player.id, False, 'othello')
                                embed.description = f'{current_player.mention}({current_emoji}) Wins \n {other_player.mention}({other_emoji}) Loses \n \n {joined_board[0]} \n {joined_board[1]} \n {joined_board[2]} \n {joined_board[3]} \n {joined_board[4]} \n {joined_board[5]} \n {joined_board[6]} \n {joined_board[7]}'
                            embed.set_footer(text='')
                            await sent_embed.edit(embed=embed)
                            await sent_embed.clear_reactions()
                        elif black > white:
                            if current_emoji == '⚫':
                                DatabaseTools.editPlayerScore(current_player.id, True, 'othello')
                                DatabaseTools.editPlayerScore(other_player.id, False, 'othello')
                                embed.description = f'{current_player.mention}({current_emoji}) Wins \n {other_player.mention}({other_emoji}) Loses \n \n {joined_board[0]} \n {joined_board[1]} \n {joined_board[2]} \n {joined_board[3]} \n {joined_board[4]} \n {joined_board[5]} \n {joined_board[6]} \n {joined_board[7]}'
                            else:
                                DatabaseTools.editPlayerScore(current_player.id, False, 'othello')
                                DatabaseTools.editPlayerScore(other_player.id, True, 'othello')
                                embed.description = f'{current_player.mention}({current_emoji}) Loses \n {other_player.mention}({other_emoji}) Wins \n \n {joined_board[0]} \n {joined_board[1]} \n {joined_board[2]} \n {joined_board[3]} \n {joined_board[4]} \n {joined_board[5]} \n {joined_board[6]} \n {joined_board[7]}'
                            embed.set_footer(text='')
                            await sent_embed.clear_reactions()
                        else:
                            DatabaseTools.editPlayerScore(current_player.id, True, 'othello')
                            DatabaseTools.editPlayerScore(other_player.id, True, 'othello')
                            embed.description = f'Tie between {current_player.mention}({current_emoji}) amd {other_player.mention}({other_emoji}) \n \n {joined_board[0]} \n {joined_board[1]} \n {joined_board[2]} \n {joined_board[3]} \n {joined_board[4]} \n {joined_board[5]} \n {joined_board[6]} \n {joined_board[7]}'
                            embed.set_footer(text='')
                            await sent_embed.clear_reactions()
                        await sent_embed.edit(embed=embed)


def setup(bot):
    bot.add_cog(Connect4(bot))
