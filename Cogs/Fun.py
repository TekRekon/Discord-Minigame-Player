from discord.ext import commands
from Cogs.Tools import MessageTools
import discord


class Fun(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def roast(self, ctx, arg: discord.Member):
        if MessageTools.correct_command_use(ctx, False):
            # Find the custom emoji needed uploaded in my server
            for m in self.bot.get_guild(477829362771689484).emojis:
                if m.name == 'BoiGif':
                    if arg == self.bot.user:
                        await ctx.message.add_reaction('🇧')
                        await ctx.message.add_reaction('🇴')
                        await ctx.message.add_reaction('🇮')
                        await ctx.message.add_reaction(m)
                        await MessageTools.sendSimpleEmbed(ctx, f'{ctx.author.mention}, You roast me I roast you', delete=False)
                    elif arg == ctx.author:
                        await ctx.message.add_reaction('🇧')
                        await ctx.message.add_reaction('🇴')
                        await ctx.message.add_reaction('🇮')
                        await ctx.message.add_reaction(m)
                    else:
                        async for message in ctx.channel.history(limit=50):
                            if message.author == arg:
                                await message.add_reaction('🇧')
                                await message.add_reaction('🇴')
                                await message.add_reaction('🇮')
                                await message.add_reaction(m)
                                break

    @commands.command()
    async def purge(self, ctx, num: int):
        if MessageTools.correct_command_use(ctx, mod_command=True):
            if ctx.message.author != self.bot.user:
                await ctx.message.delete()
                await ctx.channel.purge(limit=num)


def setup(bot):
    bot.add_cog(Fun(bot))
