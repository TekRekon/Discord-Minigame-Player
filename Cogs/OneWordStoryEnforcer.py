from discord.ext import commands
import discord
from Cogs.Tools import JsonTools, MessageTools


class OneWordStoryEnforcer(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.type != discord.ChannelType.private:
            guildID = str(message.guild.id)
            author = message.author
            channel = message.channel
            content = message.content
            oneWordChannel = self.bot.get_channel(JsonTools.getData(guildID, 'oneWordChannel'))
            prevAuthor = JsonTools.getData(guildID, 'oneWordPrevAuthor')

            if channel == oneWordChannel and author != self.bot.user:
                await message.delete()
                if ' ' in content or author.id == prevAuthor:
                    await MessageTools.sendSimpleEmbed(channel=oneWordChannel, text='You may only type ONE word '
                                                       'after another person has gone', delete=True)
                elif content.startswith(JsonTools.getData(guildID, 'prefix')) and len(content) > 1:
                    await MessageTools.sendSimpleEmbed(channel=oneWordChannel, text='You may only type ONE word '
                                                       'after another person has gone', delete=True)
                else:
                    JsonTools.changeData(guildID, 'oneWordPrevAuthor', author.id)
                    await channel.send(embed=discord.Embed(description=author.name.mention + ' ' + message.content, color=0xff0000))


def setup(bot):
    bot.add_cog(OneWordStoryEnforcer(bot))
