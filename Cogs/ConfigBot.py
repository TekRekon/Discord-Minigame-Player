from discord.ext import commands
import json
import discord
import asyncio
import Jsontools


class ConfigBot(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # with open('data.json', 'r') as f:
    #     data = json.load(f)
    #     for majorkey, subdict in data.items():
    #         for subkey, value in subdict.items():
    #             print (subkey)

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        Jsontools.addGuild(guild)

    @staticmethod
    def correct_command_use(ctx, admin_command):
        data = Jsontools.getDataParsable()
        if ctx.message.channel.id not in data[ctx.guild.name]['noCommandChannels']:
            if admin_command and ctx.author.id in data[ctx.guild.name]['mods']:
                if ctx.message.content.startswith(data[ctx.guild.name]['prefix']):
                    return True
            elif not admin_command:
                return True
        else:
            return False

    def generateSettings(self, ctx):
        data = Jsontools.getDataParsable()
        settings_embed = discord.Embed(title=f'Hey {ctx.author.name}, what needs editing?', color=0xff0000)
        settings_embed.add_field(name='\u200b',
                                 value='🇦**:** Edit my command prefix: `' + data[ctx.guild.name]['prefix'] + '`',
                                 inline=False)
        userMods = [self.bot.get_user(x) for x in data[ctx.guild.name]['mods']]
        settings_embed.add_field(name='\u200b',
                                 value='🇧**:** Edit your mods: `' + str([x.name for x in userMods]) + '`',
                                 inline=False)
        settings_embed.set_author(name='Settings',
                                  icon_url='https://cdn.discordapp.com/attachments/488700267060133889/694687205469323284/settingjif.gif')
        settings_embed.set_footer(text='React to continue')
        return settings_embed

    @commands.command()
    async def config(self, ctx):
        await ctx.message.delete()
        if ConfigBot.correct_command_use(ctx=ctx, admin_command=True):
            sent_setting = await ctx.send(embed=ConfigBot.generateSettings(self, ctx))
            await sent_setting.add_reaction('🇦')

            def check(reaction, user):
                return user == ctx.author and reaction.emoji in ['🇦', '🇧', '🇨', '🇩', '🇪', '🇫', '🇬', '🇭', '🇮',
                                                                 '🇯'] and reaction.message.id == sent_setting.id

            try:
                reaction, user = await self.bot.wait_for('reaction_add', check=check, timeout=60.0)
                await sent_setting.delete()
                if reaction.emoji == '🇦':
                    await ctx.send("Worked!")
            except asyncio.TimeoutError:
                warn = await ctx.send(
                    embed=discord.Embed(description=ctx.author.mention + ' Operation timed out', color=0xff0000))
                await warn.delete(delay=20)

        else:
            msg = await ctx.send(
                embed=discord.Embed(title='\u200b', description=f'{ctx.author.mention} Access denied. Mod-Only.',
                                    color=0xff0000))
            await msg.delete(delay=10)

    # @commands.command()
    # async def test(self, ctx, arg):
    #     if ConfigBot.correct_command_use(ctx=ctx, admin_command=False):
    #         Jsontools.changeData(ctx.guild.name, 'prefix', arg)
    #         await ctx.send(f'Nice {ctx.author.mention}! Ur prefix is now: {arg} \n Try using the config command now!')


def setup(bot):
    bot.add_cog(ConfigBot(bot))
