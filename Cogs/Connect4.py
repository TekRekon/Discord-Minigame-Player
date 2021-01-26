from discord.ext import commands
from Cogs.Tools import DatabaseTools
from itertools import cycle
import asyncio, randfacts, random, discord


class Connect4(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    def checkBoardWin(board):
        for n, list in enumerate(board):
            for i, cell in enumerate(list):
                if cell in ['🔴', '🔵']:
                    if i < 4 and n > 2 and (board[n][i] == board[n - 1][i + 1] == board[n - 2][i + 2] == board[n - 3][i + 3]):
                        return cell
                    if i > 2 and n > 2 and (
                            board[n][i] == board[n - 1][i - 1] == board[n - 2][i - 2] == board[n - 3][i - 3]):
                        return cell
                    if n < 3 and (board[n][i] == board[n + 1][i] == board[n + 2][i] == board[n + 3][i]):
                        return cell
                    if i < 4 and (board[n][i] == board[n][i + 1] == board[n][i + 2] == board[n][i + 3]):
                        return cell
                    if n == 0 and '⚪' not in board[n]:
                        return 'TIE'
        return 'NO_END'

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.guild_only()
    async def connect4(self, ctx):

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
        working = True

        # Options Menu #
        # TODO add prompt timed out exceptions
        embed = discord.Embed(description=f'{ctx.author.mention} is waiting... \n 📲: **Join the game**', color=0xff0000)
        embed.set_author(name='Connect Four', icon_url='https://cdn.discordapp.com/attachments/488700267060133889/699343937965654122/ezgif-7-6d4bab9dedb9.gif')
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
                await me.send(f"connect4 game initiated")

                # Loading Connect4 #
                await sent_embed.clear_reactions()
                embed.set_author(name='Connect Four', icon_url='https://cdn.discordapp.com/attachments/488700267060133889/699343937965654122/ezgif-7-6d4bab9dedb9.gif')
                embed.description = 'Loading...'
                await sent_embed.edit(embed=embed)
                for emoji in reactions:
                    await sent_embed.add_reaction(emoji)
                sent_embed = await self.bot.get_channel(ctx.channel.id).fetch_message(sent_embed.id)


                # Player vs player exclusive variables #
                p_list = [p1, p2]
                random.shuffle(p_list)
                alt_player = cycle(p_list)
                moves = 0
                connect4_tips = ['Move not registering? Try double tapping.', 'The middle column and row are the most valuable.', 'Try learning the Odd-Even Strategy.', 'You\'re looking mighty fine today', 'You have 3 minutes to make a move before receiving a loss.', randfacts.getFact(filter=True), 'Don\'t fat-finger the reactions.']
                embed.set_footer(text=random.choice(connect4_tips))

            # Actual Game #
                while working:
                    current_player = next(alt_player)
                    current_emoji = next(alt_emoji)
                    other_player = next(alt_player)
                    other_emoji = next(alt_emoji)
                    next(alt_player)
                    next(alt_emoji)
                    joined_board = ["|".join(reactions), "|".join(board[0]), "|".join(board[1]), "|".join(board[2]), "|".join(board[3]), "|".join(board[4]), "|".join(board[5])]

                    # Player's turn
                    embed.description = f'{current_player.mention}({current_emoji}) Make your move \n \n {joined_board[0]} \n {joined_board[1]} \n {joined_board[2]} \n {joined_board[3]} \n {joined_board[4]} \n {joined_board[5]} \n {joined_board[6]}'
                    if moves % 5 == 0:
                        embed.set_footer(text=random.choice(connect4_tips))
                    await sent_embed.edit(embed=embed)

                    try:
                        reaction, user = await self.bot.wait_for('reaction_add', timeout=180.0, check=check_reaction)
                    except asyncio.TimeoutError:
                        embed.description = f'{other_player.mention}({other_emoji}) Wins \n {current_player.mention}({current_emoji}) Loses \n \n "Player turn timed out \n \n {joined_board[0]} \n {joined_board[1]} \n {joined_board[2]} \n {joined_board[3]} \n {joined_board[4]} \n {joined_board[5]} \n {joined_board[6]}'
                        embed.set_footer(text='')
                        await sent_embed.edit(embed=embed)
                        await sent_embed.clear_reactions()
                        DatabaseTools.addPlayer(current_player.id, current_player.name, 'connect4')
                        DatabaseTools.addPlayer(other_player.id, other_player.name, 'connect4')
                        DatabaseTools.editPlayerScore(current_player.id, False, 'connect4')
                        DatabaseTools.editPlayerScore(other_player.id, True, 'connect4')
                        return

                    await sent_embed.remove_reaction(reaction.emoji, user)
                    for i, emoji in enumerate(reactions):
                        if emoji == reaction.emoji:
                            for list in reversed(board):
                                if list[i] == '⚪':
                                    list[i] = current_emoji
                                    break

                    moves += 1

                    # Evaluate Board #
                    joined_board = ["|".join(reactions), "|".join(board[0]), "|".join(board[1]), "|".join(board[2]), "|".join(board[3]), "|".join(board[4]), "|".join(board[5])]
                    result = Connect4.checkBoardWin(board)
                    if result == 'TIE':
                        working = False
                        DatabaseTools.addPlayer(current_player.id, current_player.name, 'connect4')
                        DatabaseTools.addPlayer(other_player.id, other_player.name, 'connect4')
                        DatabaseTools.editPlayerScore(current_player.id, True, 'connect4')
                        DatabaseTools.editPlayerScore(other_player.id, True, 'connect4')
                        embed.description = f'Tie between {current_player.mention}({current_emoji}) and {other_player.mention}({other_emoji}) \n \n {joined_board[0]} \n {joined_board[1]} \n {joined_board[2]} \n {joined_board[3]} \n {joined_board[4]} \n {joined_board[5]} \n {joined_board[6]}'
                        embed.set_footer(text='')
                        await sent_embed.edit(embed=embed)
                        await sent_embed.clear_reactions()
                    elif result in ['🔴', '🔵']:
                        working = False
                        DatabaseTools.addPlayer(current_player.id, current_player.name, 'connect4')
                        DatabaseTools.addPlayer(other_player.id, other_player.name, 'connect4')
                        DatabaseTools.editPlayerScore(current_player.id, True, 'connect4')
                        DatabaseTools.editPlayerScore(other_player.id, False, 'connect4')
                        embed.description = f'{current_player.mention}({current_emoji}) Wins \n {other_player.mention}({other_emoji}) Loses \n \n {joined_board[0]} \n {joined_board[1]} \n {joined_board[2]} \n {joined_board[3]} \n {joined_board[4]} \n {joined_board[5]} \n {joined_board[6]}'
                        embed.set_footer(text='')
                        await sent_embed.edit(embed=embed)
                        await sent_embed.clear_reactions()


def setup(bot):
    bot.add_cog(Connect4(bot))
