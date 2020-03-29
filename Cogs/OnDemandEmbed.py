from discord.ext import commands
import discord


class OnDemandEmbed(commands.Cog):
    userTekRekon = None
    guild = None

    def __init__(self, bot):
        self.bot = bot
        OnDemandEmbed.guild = self.bot.get_guild(477829362771689484)
        OnDemandEmbed.userTekRekon = OnDemandEmbed.guild.get_member(285879705989677058)

    @commands.command()
    async def create_embed(self, ctx, *args):
        if ctx.author != self.bot.user:
            # await ctx.send('{} arguments: {}'.format(len(args), ', '.join(args)))
            if len(args) > 0:
                embed = discord.Embed(color=0xff0000)
                for n, x in enumerate(args):
                    if x.startswith('T') and len(x) > 1 and n == 0:
                        embed = discord.Embed(title=x[1:], color=0xff0000)
                    elif x.startswith('f') and len(x) > 1:
                        embed.set_footer(text=x[1:])
                    elif x.startswith('F') and len(x.split('|')[0]) > 1 and len(x.split('|')[1]) > 0:
                        embed.add_field(name=x.split('|')[0][1:], value=x.split('|')[1])
                    else:
                        embed = discord.Embed(title='\'TExample\' argument creates a title named Example (always '
                                                    'declare first)', color=0xff0000)
                        embed.add_field(name='\'FExample|Value\' argument creates a field with the word Example',
                                        value='and a field value name Value')
                        embed.set_footer(text='\'fExample\' argument creates a footer with the word Example')
                        await ctx.send(ctx.author.mention + 'Your arguments were either null or unconventional. I made '
                                                            'you an informational embed on how to use '
                                                            '\'.create_embed\' correctly:')
                        break
                embed.set_author(name=ctx.author.mention, icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)
                await ctx.message.delete()
            else:
                ctx.message.delete()
                warn_message = await ctx.send(ctx.author.mention + 'Please enter an argument first')
                await warn_message.delete(delay=5)


def setup(bot):
    bot.add_cog(OnDemandEmbed(bot))
