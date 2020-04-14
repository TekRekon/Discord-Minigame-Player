from discord.ext import commands
from Cogs.Tools import JsonTools, MessageTools
import discord
import asyncio
import random
from itertools import cycle


class Fun(commands.Cog):

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

    @commands.command()
    async def roast(self, ctx, arg: discord.Member):
        print('was good')
        if MessageTools.correct_command_use(ctx, False):
            # Find the custom emoji needed uploaded in my server
            for m in self.bot.get_guild(JsonTools.getData('477829362771689484', 'guildID')).emojis:
                if m.name == 'BoiGif':
                    if arg == self.bot.user:
                        await ctx.message.add_reaction(m)
                        await MessageTools.sendSimpleEmbed(ctx, f'{ctx.author.mention}, You roast me I roast you',
                                                           delete=False)
                    elif arg == ctx.author:
                        await ctx.message.add_reaction(m)
                    else:
                        async for message in ctx.channel.history(limit=50):
                            if message.author == arg:
                                await message.add_reaction(m)

    @commands.command()
    async def purge(self, ctx, num: int):
        if MessageTools.correct_command_use(ctx, mod_command=True):
            await ctx.message.delete()
            await ctx.channel.purge(limit=num)


def setup(bot):
    bot.add_cog(Fun(bot))
