from discord.ext import commands
import discord


class AutoFormatNewGit(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.id == 554807470288011264 and message.author != self.bot.user:
            channel = message.channel
            try:
                embed = message.embeds[0]
                await channel.send(self.bot.get_guild(477829362771689484).get_role(556277198361722900).mention)
                await channel.send(embed=embed)
            except IndexError:
                embed = discord.Embed(description=message.content, color=0xff0000)
                embed.set_author(name=message.author.name, icon_url=message.author.avatar_url)
                await channel.send(embed=embed)
            await message.delete()


def setup(bot):
    bot.add_cog(AutoFormatNewGit(bot))
