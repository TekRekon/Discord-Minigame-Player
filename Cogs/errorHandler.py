from discord.ext import commands
import discord
import asyncio
from Cogs.Tools import MessageTools


class errorHandler(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error1):

        # Check for an original exception, if present
        error = getattr(error1, 'original', error1)

        if isinstance(error, discord.errors.Forbidden):
            # Raises another Forbidden error if error message sent in channel without access
            pass
        elif isinstance(error, discord.ext.commands.errors.MissingPermissions):
            # Actual channel is not giving access, but has the permissions in its user
            pass
        elif isinstance(error, discord.ext.commands.errors.BadArgument):
            await MessageTools.sendSimpleEmbed(ctx, f'{ctx.author.name}, Command was given bad input. For more info, use command `+help`', delete=False)
        elif isinstance(error, asyncio.TimeoutError):
            pass
        elif isinstance(error, commands.errors.CommandOnCooldown):
            await MessageTools.sendSimpleEmbed(ctx.message.channel, f'{ctx.author.name}, You are on cooldown for this command.', delete=False)
        elif isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
            await MessageTools.sendSimpleEmbed(ctx.message.channel, f'{ctx.author.name}, This command is missing required arguments. For more info, use `+help`', delete=False)
        elif isinstance(error, discord.ext.commands.errors.CommandNotFound):
            pass
        elif isinstance(error, discord.ext.commands.errors.BotMissingPermissions):
            if 'send_messages' in error.missing_perms or 'read_messages' in error.missing_perms or 'view_channel' in error.missing_perms:
                pass
            else:
                try:
                    await MessageTools.sendSimpleEmbed(ctx.message.channel, f'{ctx.author.name}, I am missing the following permission to run this command: {error.missing_perms}', delete=False)
                except discord.errors.Forbidden:
                    pass

        elif isinstance(error, discord.ext.commands.NoPrivateMessage):
            pass
        else:
            try:
                me = await self.bot.fetch_user(285879705989677058)
                await me.send(f"Unhandled error: {error} \n Message: {ctx.message} \n More: {error1}")
            except Exception:
                print(Exception)

    @commands.command()
    @commands.cooldown(1, 180, commands.BucketType.user)
    async def bug(self, ctx, *, message):
        try:
            me = await self.bot.fetch_user(285879705989677058)
            await me.send(f"> {ctx.author.name}#{ctx.author.discriminator}({ctx.author.id}): {message}")
            await MessageTools.sendSimpleEmbed(ctx, f'{ctx.author.mention}: ✅ Report sent successfully: \n `{message}`', delete=False)
        except Exception:
            await MessageTools.sendSimpleEmbed(ctx, f'{ctx.author.mention}: ❌ Report failed to send`', delete=False)


def setup(bot):
    bot.add_cog(errorHandler(bot))
