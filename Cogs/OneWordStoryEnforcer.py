from discord.ext import commands
import discord


class OneWordStoryEnforcer(commands.Cog):
    oneWordStoryChannel = None
    prevAuthor = None

    def __init__(self, bot):
        self.bot = bot
        OneWordStoryEnforcer.oneWordStoryChannel = self.bot.get_channel(552130564031774760)

    @commands.Cog.listener()
    async def on_message(self, message):
        author = message.author
        channel = message.channel
        content = message.content
        try:
            if channel == OneWordStoryEnforcer.oneWordStoryChannel:
                if ' ' in content or author == OneWordStoryEnforcer.prevAuthor:
                    if author != self.bot.user:
                        await message.delete()
                        warn_message = await channel.send("You may only type ONE word after another person has gone"
                                                          + author.mention)
                        await warn_message.delete(delay=2)
                else:
                    OneWordStoryEnforcer.prevAuthor = author

        # Catch + Handle Error If User Blocked Bot based off of ability to mention
        except discord.errors.Forbidden:
            await message.delete()
            warn_message = await OneWordStoryEnforcer.oneWordStoryChannel.send("Please unblock " + self.bot.user.mention
                                                                               + " to participate in this channel "
                                                                               + author.mention)
            await warn_message.delete(delay=5)


def setup(bot):
    bot.add_cog(OneWordStoryEnforcer(bot))
