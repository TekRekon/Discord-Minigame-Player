from discord.ext import commands
import discord

# YOU CAN MENTION PEOPLE IN THE VALUE OF A FIELD!!!

class AutoFormatNewGit(commands.Cog):
    botUpdatesChannel = None
    botNotifsRole = None
    guild = None

    def __init__(self, bot):
        self.bot = bot
        AutoFormatNewGit.guild = self.bot.get_guild(477829362771689484)
        AutoFormatNewGit.botUpdatesChannel = self.bot.get_channel(554807470288011264)
        AutoFormatNewGit.botNotifsRole = AutoFormatNewGit.guild.get_role(556277198361722900)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel == AutoFormatNewGit.botUpdatesChannel:
            if message.author != self.bot.user:
                old_embed = message.embeds[0]
                if old_embed.title is not None:
                    git_embed = discord.Embed(title=old_embed.title, color=0xff0000)
                else:
                    git_embed = discord.Embed(color=0xff0000)
                for x in old_embed.fields:
                    git_embed.add_field(name=x.name, value=x.value, inline=x.inline)
                if old_embed.author.name is not None and old_embed.author.icon_url is not None:
                    git_embed.set_author(name=old_embed.author.name, icon_url=old_embed.author.icon_url)
                await message.channel.send(AutoFormatNewGit.botNotifsRole.mention)
                await message.channel.send(embed=git_embed)
                await message.delete()


def setup(bot):
    bot.add_cog(AutoFormatNewGit(bot))
