from discord.ext import commands

# Note: to get the emoji id, use \:emoji_name: in discord #


class AutoStar(commands.Cog):
    dailyPollChannel = None
    countChannel = None
    botUpdatesChannel = None
    starboardChannel = None

    def __init__(self, bot):
        self.bot = bot
        AutoStar.dailyPollChannel = self.bot.get_channel(553760889778733073)
        AutoStar.countChannel = self.bot.get_channel(489513733652086785)
        AutoStar.botUpdatesChannel = self.bot.get_channel(554807470288011264)
        AutoStar.starboardChannel = self.bot.get_channel(549276628866564106)

    @commands.Cog.listener()
    async def on_message(self, message):
        channel = message.channel
        if channel != AutoStar.dailyPollChannel and channel != AutoStar.botUpdatesChannel \
                and channel != AutoStar.countChannel and channel != AutoStar.starboardChannel:
            if message.author != self.bot.user:
                await message.add_reaction(emoji="⭐")


def setup(bot):
    bot.add_cog(AutoStar(bot))
