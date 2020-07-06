from discord.ext import commands
import discord


class errorHandler(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # @commands.Cog.listener()
    # async def on_command_error(self, ctx, error):
    #
    #     # Check for an original exception, if present
    #     error = getattr(error, 'original', error)
    #
    #     if isinstance(error, discord.errors.Forbidden):
    #         # Raises another Forbidden error if error message sent in channel without access
    #         pass
    #     # elif isinstance(error, discord.ext.commands.errors.BadArgument) or isinstance(error, ValueError):
    #     #     await MessageTools.sendSimpleEmbed(ctx, f'{ctx.author.name}: Not valid input. Use .help for assistance',
    #     #                                        delete=True)
    #     elif isinstance(error, commands.DisabledCommand):
    #         await MessageTools.sendSimpleEmbed(ctx, f'{ctx.author.name}: {ctx.command} has been disabled',
    #                                            delete=True)
    #     elif isinstance(error, asyncio.TimeoutError):
    #         await MessageTools.sendSimpleEmbed(ctx.message.channel, f'{ctx.author.name}: Operation timed out',
    #                                            delete=False)
    #     # else:
    #     #     await ctx.send('YES! YOU FOUND AN ERROR:')
    #     #     await ctx.send(error)

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        embed = discord.Embed(description=str(error), color=0xff0000)
        embed.set_author(name=f'{ctx.author.name},', icon_url='https://cdn.discordapp.com/attachments/488700267060133889/729781442069921882/ezgif.com-crop.gif')
        await ctx.channel.send(embed=embed)


def setup(bot):
    bot.add_cog(errorHandler(bot))
