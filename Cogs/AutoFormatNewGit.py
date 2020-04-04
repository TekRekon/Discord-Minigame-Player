from discord.ext import commands
import discord


class AutoFormatNewGit(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.guild == 477829362771689484 and message.author != self.bot.user:
            old_embed = message.embeds[0]
            git_embed = discord.Embed(title=old_embed.title, description=old_embed.description, color=0xff0000)
            for x in old_embed.fields:
                git_embed.add_field(name=x.name, value=x.value, inline=x.inline)
            git_embed.set_author(name=old_embed.author.name, icon_url=old_embed.author.icon_url)
            git_embed.set_footer(text=old_embed.footer)
            await message.channel.send(self.bot.get_guild(477829362771689484).get_role(556277198361722900).mention)
            await message.channel.send(embed=git_embed)
            await message.delete()


def setup(bot):
    bot.add_cog(AutoFormatNewGit(bot))
