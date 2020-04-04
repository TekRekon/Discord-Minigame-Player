from discord.ext import commands
import discord
import asyncio


class OnDemandEmbed(commands.Cog):
    oneWordStoryChannel = None
    userTekRekon = None
    guild = None
    title = ''
    description = ''
    color = 0xff0000
    thumbnail = 'https://cdn.discordapp.com/attachments/549334435737239566/693915786665787583/Annotation_2020-03-29_' \
                '153201.png'
    user_embed = discord.Embed(color=color)
    example_embed = discord.Embed(color=color)
    footer = 'Enter 4 to change the Footer'
    stage = ""

    def __init__(self, bot):
        self.bot = bot
        OnDemandEmbed.guild = self.bot.get_guild(477829362771689484)
        OnDemandEmbed.userTekRekon = OnDemandEmbed.guild.get_member(285879705989677058)
        OnDemandEmbed.oneWordStoryChannel = self.bot.get_channel(552130564031774760)

    @commands.command()
    async def embed(self, ctx):
        if ctx.author != self.bot.user and ctx.message.channel != OnDemandEmbed.oneWordStoryChannel:
            OnDemandEmbed.thumbnail = 'https://cdn.discordapp.com/attachments/549334435737239566/693915786665787583/' \
                                      'Annotation_2020-03-29_153201.png'
            OnDemandEmbed.user_embed = discord.Embed(color=OnDemandEmbed.color)
            OnDemandEmbed.example_embed = discord.Embed(color=OnDemandEmbed.color)
            OnDemandEmbed.footer = 'Enter 4 to change the Footer'
            try:
                def check(message):
                    return message.author == ctx.author and len(message.content) > 0 \
                           and message.channel == ctx.message.channel

                def generate_example_embed():
                    if OnDemandEmbed.title == 'None' and OnDemandEmbed.description == 'None':
                        OnDemandEmbed.example_embed = discord.Embed(color=OnDemandEmbed.color)
                        OnDemandEmbed.user_embed = discord.Embed(color=OnDemandEmbed.color)
                    elif OnDemandEmbed.title is not None and OnDemandEmbed.description is not None:
                        OnDemandEmbed.example_embed = discord.Embed(title=OnDemandEmbed.title,
                                                                    description=OnDemandEmbed.description,
                                                                    color=OnDemandEmbed.color)
                        OnDemandEmbed.user_embed = discord.Embed(title=OnDemandEmbed.title,
                                                                 description=OnDemandEmbed.description,
                                                                 color=OnDemandEmbed.color)
                    elif OnDemandEmbed.title == 'None':
                        OnDemandEmbed.example_embed = discord.Embed(description=OnDemandEmbed.description,
                                                                    color=OnDemandEmbed.color)
                        OnDemandEmbed.user_embed = discord.Embed(description=OnDemandEmbed.description,
                                                                 color=OnDemandEmbed.color)
                    elif OnDemandEmbed.description == 'None':
                        OnDemandEmbed.example_embed = discord.Embed(title=OnDemandEmbed.title,
                                                                    color=OnDemandEmbed.color)
                        OnDemandEmbed.user_embed = discord.Embed(title=OnDemandEmbed.title, color=OnDemandEmbed.color)

                    OnDemandEmbed.example_embed.set_author(name='Type Done to finish or Cancel to exit',
                                                           icon_url=ctx.author.avatar_url)
                    OnDemandEmbed.example_embed.set_thumbnail(url=OnDemandEmbed.thumbnail)
                    OnDemandEmbed.example_embed.set_footer(text=OnDemandEmbed.footer)

                OnDemandEmbed.stage = 'init'
                await ctx.message.delete()
                prompt = await ctx.send(embed=discord.Embed(description=ctx.author.mention + 'Enter a Title or None',
                                                            color=OnDemandEmbed.color))
                title = await self.bot.wait_for('message', timeout=60.0, check=check)
                OnDemandEmbed.title = title.content
                await  title.delete()
                await prompt.delete()

                prompt = await ctx.send(embed=discord.Embed(description=ctx.author.mention + ' Enter a Description or '
                                                                                             'None',
                                                            color=OnDemandEmbed.color))
                description = await self.bot.wait_for('message', timeout=60.0, check=check)
                OnDemandEmbed.description = description.content
                await  description.delete()
                await prompt.delete()

                generate_example_embed()

                working = True
                OnDemandEmbed.stage = 'working'
                while working:
                    sent_example_embed = await ctx.send(embed=OnDemandEmbed.example_embed)
                    input_num = await self.bot.wait_for('message', timeout=60.0, check=check)
                    if input_num.content == '4':
                        await sent_example_embed.delete()
                        await input_num.delete()
                        prompt = await ctx.send(embed=discord.Embed(description=ctx.author.mention + ' Enter a Footer',
                                                                    color=OnDemandEmbed.color))
                        input_footer = await self.bot.wait_for('message', timeout=60.0, check=check)
                        OnDemandEmbed.footer = input_footer.content
                        if OnDemandEmbed.footer != 'None':
                            OnDemandEmbed.user_embed.set_footer(text=input_footer.content)
                        await input_footer.delete()
                        await prompt.delete()
                        if OnDemandEmbed.footer != 'None':
                            OnDemandEmbed.example_embed.set_footer(text=OnDemandEmbed.footer)
                    elif input_num.content == '3':
                        await sent_example_embed.delete()
                        await input_num.delete()
                        prompt = await ctx.send(embed=discord.Embed(description=ctx.author.mention
                                                                    + ' Enter a valid Thumbnail URL',
                                                                    color=OnDemandEmbed.color))
                        input_url = await self.bot.wait_for('message', timeout=60.0, check=check)
                        OnDemandEmbed.thumbnail = input_url.content
                        if OnDemandEmbed.thumbnail != 'None':
                            OnDemandEmbed.user_embed.set_thumbnail(url=input_url.content)
                        await input_url.delete()
                        await prompt.delete()
                        if OnDemandEmbed.thumbnail != 'None':
                            OnDemandEmbed.example_embed.set_thumbnail(url=input_url.content)
                    elif input_num.content == 'Done' or input_num.content == 'done':
                        await sent_example_embed.delete()
                        await input_num.delete()
                        OnDemandEmbed.user_embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
                        await ctx.send(embed=OnDemandEmbed.user_embed)
                        working = False
                    elif input_num.content.lower() == 'cancel':
                        await sent_example_embed.delete()
                        await input_num.delete()
                        cancel_msg = await ctx.send(embed=discord.Embed(description=ctx.author.mention
                                                                        + ' Operation cancelled',
                                                                        color=OnDemandEmbed.color))
                        await cancel_msg.delete(delay=10)
                        working = False
                    else:
                        await input_num.delete()
                        cancel_msg = ctx.send(embed=discord.Embed(description=ctx.author.mention + ' Valid input '
                                                                                                   'please',
                                                                  color=OnDemandEmbed.color))
                        await cancel_msg.delete(delay=3)

            except asyncio.TimeoutError:
                embed_warn = discord.Embed(description=ctx.author.mention + ' Operation timed out', color=0xff0000)
                if OnDemandEmbed.stage == 'init':
                    await prompt.delete()
                elif OnDemandEmbed.stage == 'working':
                    await sent_example_embed.delete()
                warn_cache = await ctx.send(embed=embed_warn)
                await warn_cache.delete(delay=20)


def setup(bot):
    bot.add_cog(OnDemandEmbed(bot))
