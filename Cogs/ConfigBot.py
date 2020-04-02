from discord.ext import commands
import json
import discord
import asyncio
import Jsontools


class ConfigBot(commands.Cog):
    reactions = ['🇦', '🇧', '🇨', '🇩', '🇪', '🇫', '🇬', '🇭', '🇮', '🇯']

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

    def generateSettings(self, ctx, num):
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
                                  icon_url='https://cdn.discordapp.com/attachments/488700267060133889'
                                           '/694687205469323284/settingjif.gif')
        settings_embed.set_footer(text='React to continue')
        return settings_embed

    async def addReactions(self, message, num):
        for n, reaction in enumerate(ConfigBot.reactions):
            if n < num:
                await message.add_reaction(reaction)

    async def sendSimpleEmbed(self, channel, text, delete):
        sent_msg = await channel.send(
            embed=discord.Embed(description=text, color=0xff0000))
        if delete:
            await sent_msg.delete(delay=10)
        return sent_msg

    @commands.command()
    async def config(self, ctx):
        try:
            await ctx.message.delete()
            if ConfigBot.correct_command_use(ctx=ctx, admin_command=True):
                def check_reaction(reaction, user):
                    return user == ctx.author and reaction.emoji in ConfigBot.reactions and reaction.message.id == sent_prompt.id

                def check_message(message):
                    return message.author == ctx.author and len(
                        message.content) > 0 and message.channel == ctx.message.channel

                use_settings = True
                while use_settings:
                    embed = ConfigBot.generateSettings(self, ctx, 2)
                    sent_prompt = await ctx.send(embed=embed)
                    await ConfigBot.addReactions(self, sent_prompt, 2)
                    reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=check_reaction)
                    await sent_prompt.delete()

                    if reaction.emoji == '🇦':
                        sent_prompt = await ctx.send(
                            embed=discord.Embed(description=f'{ctx.author.mention} Enter my new prefix',
                                                color=0xff0000))
                        command_change_response = await self.bot.wait_for('message', timeout=60.0, check=check_message)
                        if len(command_change_response.content) < 6:
                            Jsontools.changeData(ctx.guild.name, 'prefix', command_change_response.content)
                        await sent_prompt.delete()
                        await command_change_response.delete()

                    if reaction.emoji == '🇧':
                        sent_prompt = await ctx.send(embed=discord.Embed(
                            description=f'{ctx.author.mention} React to continue: \n 🇦: Add a mod \n 🇧: Delete a mod',
                            color=0xff0000))
                        await ConfigBot.addReactions(self, sent_prompt, 2)
                        reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=check_reaction)
                        await sent_prompt.delete()

                        if reaction.emoji == '🇦':
                            sent_prompt = await ctx.send(
                                embed=discord.Embed(description=f'{ctx.author.mention} Mention the mod you want to add',
                                                    color=0xff0000))
                            mod_add_response = await self.bot.wait_for('message', timeout=60.0, check=check_message)
                            await sent_prompt.delete()
                            for member in mod_add_response.mentions:
                                if member.id not in Jsontools.getData(ctx.guild.name, 'mods'):
                                    Jsontools.addListVar(ctx.guild.name, 'mods', member.id)
                            await mod_add_response.delete()
                        if reaction.emoji == '🇧':
                            sent_prompt = await ctx.send(embed=discord.Embed(
                                description=f'{ctx.author.mention} Mention the mod you want to delete', color=0xff0000))
                            mod_add_response = await self.bot.wait_for('message', timeout=60.0, check=check_message)
                            await sent_prompt.delete()
                            for member in mod_add_response.mentions:
                                if member.id in Jsontools.getData(ctx.guild.name, 'mods'):
                                    Jsontools.removeListVar(ctx.guild.name, 'mods', member.id)
                            await mod_add_response.delete()


            else:
                await ConfigBot.sendSimpleEmbed(self, channel=ctx.message.channel,
                                                text=f'{ctx.author.mention} Access denied. Mod-Only.', delete=True)

        except asyncio.TimeoutError:
            await ConfigBot.sendSimpleEmbed(self, channel=ctx.message.channel,
                                            text=f'{ctx.author.mention} Operation timed out', delete=True)
            ConfigBot.config.use_settings = False

    # @commands.command()
    # async def test(self, ctx, arg):
    #     if ConfigBot.correct_command_use(ctx=ctx, admin_command=False):
    #         Jsontools.changeData(ctx.guild.name, 'prefix', arg)
    #         await ctx.send(f'Nice {ctx.author.mention}! Ur prefix is now: {arg} \n Try using the config command now!')


def setup(bot):
    bot.add_cog(ConfigBot(bot))
