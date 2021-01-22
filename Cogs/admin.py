from discord.ext import commands
import discord
import asyncio
from Cogs.Tools import MessageTools
import psycopg2


class admin(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def fetchguilds(self, ctx, numGuilds):
        if ctx.message.author.id == 285879705989677058:
            for guild in self.bot.guilds:
                if numGuilds != 0:
                    numGuilds -= 1
                    await ctx.send(f"{guild.name}")
                else:
                    return

    # @commands.command()
    # @commands.cooldown(1, 5, commands.BucketType.user)
    # async def test(self, ctx, prefix):
    #     print("testing")
    #     con = psycopg2.connect("postgres://tmneuvqnzogsxo:d15b738ee44cc1429e2cf014bf3c1df8448fea2b0155a4157e8e2a37dbc0d495@ec2-54-146-142-58.compute-1.amazonaws.com:5432/d3ad8vk1so3cfu")
    #     cur = con.cursor()
    #     print('connected')
    #     cur.execute("SELECT EXISTS(SELECT 1 FROM guildsettings WHERE guild_id = %s)", [ctx.guild.id])
    #     print('selected')
    #     guild_exist = cur.fetchall()
    #     print(guild_exist)
    #
    #     if guild_exist[0][0]:
    #         print('not empty data')
    #         cur.execute("UPDATE guildsettings SET prefix = %s WHERE guild_id = %s", [prefix, ctx.guild.id])
    #
    #     else:
    #         print("creating new guild")
    #         new_guild = (
    #             "INSERT INTO guildsettings (guild_id, username, prefix) "
    #             "VALUES (%s, %s, %s)"
    #         )
    #
    #         data = (ctx.guild.id, ctx.guild.name, '.')
    #
    #         cur.execute(new_guild, data)
    #
    #     con.commit()
    #     cur.close()
    #     con.close()

    @commands.command()
    async def who(self, ctx, word):
        if word == 'asked' and ctx.guild.id == 715634233590415441:
            await MessageTools.sendSimpleEmbed(channel=ctx, text="**No one.**", delete=False)

def setup(bot):
    bot.add_cog(admin(bot))