from discord.ext import commands
import discord
import asyncio
from Cogs.Tools import JsonTools, MessageTools


class ConfigBot(commands.Cog):
    reactions = ['🇦', '🇧', '🇨', '🇩', '🇪', '🇫', '🇬', '🇭', '🇮', '🇯']

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):

        # Check for an original exception, if present
        error = getattr(error, 'original', error)

        # TODO Handle insufficient permissions error

        if isinstance(error, discord.errors.Forbidden):
            # Raises another Forbidden error if error message sent in channel without access
            print('error')
            pass
        # elif isinstance(error, discord.ext.commands.errors.BadArgument) or isinstance(error, ValueError):
        #     await MessageTools.sendSimpleEmbed(ctx, f'{ctx.author.name}: Not valid input. Use .help for assistance',
        #                                        delete=True)
        elif isinstance(error, commands.DisabledCommand):
            await MessageTools.sendSimpleEmbed(ctx, f'{ctx.author.name}: {ctx.command} has been disabled',
                                               delete=True)
        elif isinstance(error, asyncio.TimeoutError):
            await MessageTools.sendSimpleEmbed(ctx.message.channel, f'{ctx.author.name}: Operation timed out',
                                               delete=False)

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        JsonTools.addGuild(guild)

    def generateSettings(self, ctx):
        data = JsonTools.getDataParsable()
        settings_embed = discord.Embed(title=f'Hey {ctx.author.name}, what needs editing?', color=0xff0000)
        settings_embed.add_field(name='\u200b',
                                 value='🇦**:** Edit my command prefix: `' + data[str(ctx.guild.id)]['prefix'] + '`',
                                 inline=False)
        user_mods = [self.bot.get_user(x) for x in data[str(ctx.guild.id)]['mods']]
        settings_embed.add_field(name='\u200b',
                                 value='🇧**:** Edit your mods: `' + str([x.name for x in user_mods]) + '`',
                                 inline=False)
        settings_embed.set_author(name='Settings',
                                  icon_url='https://cdn.discordapp.com/attachments/488700267060133889'
                                           '/694687205469323284/settingjif.gif')
        settings_embed.set_footer(text='React to continue')
        return settings_embed

    # TODO Add a quit option
    @commands.command()
    async def config(self, ctx):
        try:
            if MessageTools.correct_command_use(ctx=ctx, mod_command=True):
                await ctx.message.delete()
                def check_reaction(reaction, user):
                    return user == ctx.author and reaction.emoji in ConfigBot.reactions and reaction.message.id == \
                           sent_prompt.id

                def check_message(message):
                    return message.author == ctx.author and len(
                        message.content) > 0 and message.channel == ctx.message.channel

                use_settings = True
                while use_settings:
                    # Create settings page and retrieve reaction
                    embed = ConfigBot.generateSettings(self, ctx)
                    sent_prompt = await ctx.send(embed=embed)
                    await MessageTools.addReactions(sent_prompt, 2)
                    reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=check_reaction)
                    await sent_prompt.delete()

                    if reaction.emoji == '🇦':
                        sent_prompt = await ctx.send(
                            embed=discord.Embed(description=f'{ctx.author.mention} Enter my new prefix',
                                                color=0xff0000))
                        command_change_response = await self.bot.wait_for('message', timeout=60.0, check=check_message)
                        if len(command_change_response.content) < 6:
                            JsonTools.changeData(str(ctx.guild.id), 'prefix', command_change_response.content)
                        await sent_prompt.delete()
                        await command_change_response.delete()

                    if reaction.emoji == '🇧':
                        sent_prompt = await ctx.send(embed=discord.Embed(
                            description=f'{ctx.author.mention} React to continue: \n 🇦: Add mods \n 🇧: Delete mods',
                            color=0xff0000))
                        await MessageTools.addReactions(sent_prompt, 2)
                        reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=check_reaction)
                        await sent_prompt.delete()

                        if reaction.emoji == '🇦':
                            sent_prompt = await ctx.send(
                                embed=discord.Embed(description=f'{ctx.author.mention} Mention the mods you want to '
                                                    f'add', color=0xff0000))
                            mod_add_response = await self.bot.wait_for('message', timeout=60.0, check=check_message)
                            await sent_prompt.delete()
                            for member in mod_add_response.mentions:
                                if member.id not in JsonTools.getData(str(ctx.guild.id), 'mods'):
                                    JsonTools.addListVar(str(ctx.guild.id), 'mods', member.id)
                            await mod_add_response.delete()
                        if reaction.emoji == '🇧':
                            sent_prompt = await ctx.send(embed=discord.Embed(description=f'{ctx.author.mention} '
                                                         f'Mention the mods you want to delete', color=0xff0000))
                            mod_add_response = await self.bot.wait_for('message', timeout=60.0, check=check_message)
                            await sent_prompt.delete()
                            for member in mod_add_response.mentions:
                                if member.id in JsonTools.getData(str(ctx.guild.id), 'mods'):
                                    JsonTools.removeListVar(str(ctx.guild.id), 'mods', member.id)
                            await mod_add_response.delete()
            else:
                await MessageTools.sendSimpleEmbed(channel=ctx.message.channel, text=f'{ctx.author.name}: Command used incorrectly', delete=True)

        except asyncio.TimeoutError:
            await MessageTools.sendSimpleEmbed(channel=ctx.message.channel, text=f'{ctx.author.mention} Operation '
                                               f'timed out', delete=True)
            ConfigBot.config.use_settings = False



    # @commands.command()
    # async def test(self, ctx, arg):
    #     if ConfigBot.correct_command_use(ctx=ctx, admin_command=False):
    #         Jsontools.changeData(ctx.guild.name, 'prefix', arg)
    #         await ctx.send(f'Nice {ctx.author.mention}! Ur prefix is now: {arg} \n Try using the config command now!')


def setup(bot):
    bot.add_cog(ConfigBot(bot))