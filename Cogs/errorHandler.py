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

        if isinstance(error, discord.errors.Forbidden):
            # Raises another Forbidden error if error message sent in channel without access
            pass
        if isinstance(error, discord.ext.commands.errors.BadArgument):
            await MessageTools.sendSimpleEmbed(ctx, f'{ctx.author.name}: Command was given bad input. For more info, use command `+help`', delete=False)
        elif isinstance(error, asyncio.TimeoutError):
            pass
        elif isinstance(error, commands.errors.CommandOnCooldown):
            await MessageTools.sendSimpleEmbed(ctx.message.channel, f'{ctx.author.name}: You are on cooldown for this command.', delete=False)
        elif isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
            await MessageTools.sendSimpleEmbed(ctx.message.channel, f'{ctx.author.name}: This command is missing required arguments. For more info, use `+help`', delete=False)
        elif isinstance(error, discord.ext.commands.errors.CommandNotFound):
            pass
        elif isinstance(error, discord.ext.commands.errors.MissingPermissions):
            pass
        elif isinstance(error, discord.ext.commands.NoPrivateMessage):
            pass
        else:
            me = self.bot.get_user(285879705989677058)
            await me.send(f"Unhandled error: {error} \n Message: {ctx.message}")

    @commands.command()
    @commands.cooldown(1, 180, commands.BucketType.user)
    async def bug(self, ctx, *, message):
        await ctx.message.delete()
        me = self.bot.get_user(285879705989677058)
        await me.send(f"> {ctx.author.name}#{ctx.author.discriminator}({ctx.author.id}): {message}")
        await MessageTools.sendSimpleEmbed(ctx, f'{ctx.author.mention}: ✅ Report sent successfully: \n {message}', delete=False)


def setup(bot):
    bot.add_cog(errorHandler(bot))
