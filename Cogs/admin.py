from discord.ext import commands
import psycopg2
import config


class admin(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def fetchguilds(self, ctx, numGuilds):
        if ctx.message.author.id == config.personal_id:
            for guild in self.bot.guilds:
                if numGuilds != 0:
                    numGuilds -= 1
                    await ctx.send(f"{guild.name}")
                else:
                    return

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def test(self, ctx, prefix):
        con = psycopg2.connect(dbname=config.dbname, user=config.user, password=config.password)
        cur = con.cursor()
        cur.execute("SELECT EXISTS(SELECT 1 FROM guildsettings WHERE guild_id = %s)", [ctx.guild.id])
        guild_exist = cur.fetchall()

        if guild_exist[0][0]:
            cur.execute("UPDATE guildsettings SET prefix = %s WHERE guild_id = %s", [prefix, ctx.guild.id])

        else:
            new_guild = (
                "INSERT INTO guildsettings (guild_id, username, prefix) "
                "VALUES (%s, %s, %s)"
            )

            data = (ctx.guild.id, ctx.guild.name, '.')

            cur.execute(new_guild, data)

        con.commit()
        cur.close()
        con.close()


def setup(bot):
    bot.add_cog(admin(bot))