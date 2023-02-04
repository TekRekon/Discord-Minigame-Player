from discord.ext import commands
from Cogs.Tools import DatabaseTools
from itertools import cycle
import asyncio, randfacts, psycopg2, time, random, discord, config


class DataCommands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.guild_only()
    async def leaderboard(self, ctx, mode: str, start: int = 1):
        con = psycopg2.connect(config.dbname, config.user, config.password)
        cur = con.cursor()

        if mode == "tictactoe":
            p_scores = DatabaseTools.fetchRankedStats("tictactoe")
        elif mode == "connect4":
            p_scores = DatabaseTools.fetchRankedStats("connect4")
        elif mode == "othello":
            p_scores = DatabaseTools.fetchRankedStats("othello")
        elif mode == "rps":
            p_scores = DatabaseTools.fetchRankedStats("rps")
        else:
            raise discord.ext.commands.errors.BadArgument()

        if len(p_scores) == 0:
            embed = discord.Embed(title=f'No ranked players yet. To get ranked, play 10 games of {mode}',
                                  color=0x2596be)
            await ctx.send(embed=embed)
            return

        elif start < 1 or start > len(p_scores):
            raise discord.ext.commands.errors.BadArgument()


        cur.close()
        con.close()

        embed = discord.Embed(description='\u200b', color=0x2596be)
        embed.set_author(name=f'{mode} Leaderboard', icon_url='https://cdn.discordapp.com/attachments/'
                          '488700267060133889/779444906464247828/2e4e7e76e454f56b24d6883b93afb7932.jpg')
        embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/488700267060133889/779118212850909184/'
                                'ezgif-3-814c4634232b.gif')
        for k, x in enumerate(p_scores):
            if start <= k+1 < start+10:
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
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.guild_only()
    async def profile(self, ctx, arg: discord.Member, mode: str):
        me = self.bot.get_user(285879705989677058)
        await me.send(f"profile initiated")
        if mode not in ['connect4', 'tictactoe', 'othello', 'rps']:
            raise discord.ext.commands.errors.BadArgument()
        con = psycopg2.connect(config.dbname, config.user, config.password)
        cur = con.cursor()

        if mode == 'connect4':
            cur.execute("SELECT user_id FROM playerConnect4Stats")
        elif mode == 'tictactoe':
            cur.execute("SELECT user_id FROM playertictactoestats")
        elif mode == 'othello':
            cur.execute("SELECT user_id FROM playerothellostats")
        elif mode == 'rps':
            cur.execute("SELECT user_id FROM playerrpsstats")
        rows = cur.fetchall()

        if arg.id not in [i[0] for i in rows]:
            embed = discord.Embed(title=f'{arg.name} has not played a game of {mode} yet', color=0x2596be)
            embed.set_author(name=f'{arg.name}\'s {mode} Profile', icon_url=arg.avatar_url)
            embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/488700267060133889/779526483202932777/'
                                    '9bec831078051d4fc5f06e964da71760.gif')
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(description='\u200b', color=0x2596be)
            embed.set_author(name=f'{arg.name}\'s {mode} Profile', icon_url=arg.avatar_url)
            embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/488700267060133889/779526483202932777/'
                                    '9bec831078051d4fc5f06e964da71760.gif')

            p_data = DatabaseTools.getPlayerStat(arg.id, 'all', mode)

            embed.add_field(name='🏆 **Wins**', value=f'{p_data[1]}', inline=True)
            embed.add_field(name='☠ **Losses**', value=f'{p_data[2]}', inline=True)
            embed.add_field(name='💠 **Win %**', value=f'{p_data[3]}', inline=True)

            # TODO cleanup this area
            ranked_scores = DatabaseTools.fetchRankedStats(mode)
            IDs = [r[4] for r in ranked_scores]
            winrates = [r[1] for r in ranked_scores]
            if arg.id in IDs:
                i = IDs.index(arg.id)
                embed.add_field(name='⚜ **Global Rank**', value=f'#{i+1}/{len(IDs)}', inline=True)
                if i == 0:
                    embed.add_field(name='📡 **Wins -> Next Rank**', value='0', inline=True)
                else:
                    target_winrate = winrates[i-1]
                    current_winrate = winrates[i]
                    current_wins = DatabaseTools.getPlayerStat(arg.id, "wins", f'{mode}')
                    current_losses = DatabaseTools.getPlayerStat(arg.id, "losses", f'{mode}')
                    f = 0
                    while target_winrate > current_winrate:
                        f += 1
                        current_winrate = round((current_wins+f)/(current_wins+current_losses)*100, 2)
                    embed.add_field(name='📡 **Wins -> Next Rank**', value=f'{f}', inline=True)
            else:
                embed.set_footer(text='Play 10 games to get ranked.')

            await ctx.send(embed=embed)

        cur.close()
        con.close()


def setup(bot):
    bot.add_cog(DataCommands(bot))
