from discord.ext import commands
import discord
import asyncio
from Cogs.Tools import MessageTools


class errorHandler(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):

        # Check for an original exception, if present
        error = getattr(error, 'original', error)

        # if isinstance(error, discord.errors.Forbidden):
        #     # Raises another Forbidden error if error message sent in channel without access
        #     pass
        if isinstance(error, discord.ext.commands.errors.BadArgument) or isinstance(error, ValueError):
            await MessageTools.sendSimpleEmbed(ctx, f'{ctx.author.name}: Command was used incorrectly. Use .help for assistance', delete=False)
        # elif isinstance(error, commands.DisabledCommand):
        #     await MessageTools.sendSimpleEmbed(ctx, f'{ctx.author.name}: {ctx.command} has been disabled', delete=False)
        elif isinstance(error, asyncio.TimeoutError):
            await MessageTools.sendSimpleEmbed(ctx.message.channel, f'{ctx.author.name}: Operation timed out', delete=False)
        # elif isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
        #     await MessageTools.sendSimpleEmbed(ctx.message.channel, f'{ctx.author.name}: This command is missing required arguments', delete=False)
        # elif isinstance(error, discord.ext.commands.errors.CommandNotFound):
        #     s = ctx.message.content
        #     if not s == len(s) * '.':
        #         await MessageTools.sendSimpleEmbed(ctx.message.channel, f'{ctx.author.name}: Unknown command. Use .help for assistance', delete=False)
        # else:
        #     await MessageTools.sendSimpleEmbed(ctx.message.channel, f'{ctx.author.name}: Unhandled error: {error}', delete=False)


def setup(bot):
    bot.add_cog(errorHandler(bot))
