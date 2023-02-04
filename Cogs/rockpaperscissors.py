from discord.ext import commands
import discord
import config
from Cogs.Tools import DatabaseTools
import random


class rockpaperscissors(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command()
    @commands.guild_only()
    @commands.bot_has_permissions(manage_messages=True)
    async def rps(self, ctx):

        availableReactions = ['🪨', '📰', '✂']

        def check_reaction(reaction, user):
            if reaction.emoji in ['🤖']:
                return reaction.message.id == sent_embed.id and user == ctx.author
            if reaction.emoji == '📲':
                return reaction.message.id == sent_embed.id and user != ctx.author
            return False

        def check_message(m):
            if m.channel.type == discord.ChannelType.private:
                if m.author in [p1, p2]:
                    if m.content in ['rock', 'paper', 'scissors']:
                        return True
            return False


        # TODO add game confirmation
        # TODO add prompt timed out exceptions
        embed = discord.Embed(description=f'{ctx.author.mention} is waiting... \n 📲: Join the game \n 🤖: Add a bot',
                              color=0x2596be)
        embed.set_author(name='Rock Paper Scissors', icon_url='https://cdn.discordapp.com/attachments/'
                                                              '488700267060133889/808744030618779658/b680a062246147.'
                                                              '5a8a773c6932d.gif')
        embed.set_footer(text='React to continue.')
        sent_embed = await ctx.send(embed=embed)
        await sent_embed.add_reaction('📲')
        await sent_embed.add_reaction('🤖')
        reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=check_reaction)
        await sent_embed.clear_reactions()
        embed.set_footer(text='')

        p1 = ctx.author
        working = True

        if reaction.emoji == '📲':
            p2 = user
            embed.set_author(name=f'Rock Paper Scissors (2 player)', icon_url='https://cdn.discordapp.com/'
                                                                              'attachments/488700267060133889/'
                                                                              '808744030618779658/b680a062246147.'
                                                                              '5a8a773c6932d.gif')
            embed.description = f'{p1.mention} and {p2.mention}: DM me `rock`, `paper`, or `scissors`'
            await sent_embed.edit(embed=embed)

            while working:
                # Player's turn
                message1 = await self.bot.wait_for('message', timeout=60.0, check=check_message)
                await message1.channel.send(f'✅ {message1.content} received')
                embed.description = f'{message1.author.mention} object received, waiting on your opponent: DM me ' \
                                    f'`rock`, `paper`, or `scissors`'
                await sent_embed.edit(embed=embed)
                message2 = await self.bot.wait_for('message', timeout=60.0, check=check_message)
                await message2.channel.send(f'✅ {message2.content} received')

                if message1.content == message2.content:
                    embed.description = f'{p1.mention} and {p2.mention} tied using {message1.content}. DM me ' \
                                        f'`rock`, `paper`, or `scissors`'
                    await sent_embed.edit(embed=embed)
                else:
                    try:
                        DatabaseTools.addPlayer(message1.author.id, message1.author.name, 'rps')
                        DatabaseTools.addPlayer(message1.author.id, message2.author.name, 'rps')
                        embed.set_footer(text='')
                        x = [message1.content, message2.content]
                        if 'rock' in x and 'paper' in x:
                            if message1.content == 'paper':
                                embed.description = f'{message1.author.mention} won against ' \
                                                    f'{message2.author.mention} using {message1.content}'
                                DatabaseTools.editPlayerScore(message1.author.id, True, 'rps')
                                DatabaseTools.editPlayerScore(message2.author.id, False, 'rps')
                                await sent_embed.edit(embed=embed)
                            else:
                                embed.description = f'{message2.author.mention} won against ' \
                                                    f'{message1.author.mention} using {message2.content}'
                                DatabaseTools.editPlayerScore(message1.author.id, False, 'rps')
                                DatabaseTools.editPlayerScore(message2.author.id, True, 'rps')
                                await sent_embed.edit(embed=embed)

                        elif 'paper' in x and 'scissors' in x:
                            if message1.content == 'scissors':
                                embed.description = f'{message1.author.mention} won against ' \
                                                    f'{message2.author.mention} using {message1.content}'
                                DatabaseTools.editPlayerScore(message1.author.id, True, 'rps')
                                DatabaseTools.editPlayerScore(message2.author.id, False, 'rps')
                                await sent_embed.edit(embed=embed)
                            else:
                                embed.description = f'{message2.author.mention} won against ' \
                                                    f'{message1.author.mention} using {message2.content}'
                                DatabaseTools.editPlayerScore(message1.author.id, False, 'rps')
                                DatabaseTools.editPlayerScore(message2.author.id, True, 'rps')
                                await sent_embed.edit(embed=embed)

                        elif 'scissors' in x and 'rock' in x:
                            if message1.content == 'rock':
                                embed.description = f'{message1.author.mention} won against ' \
                                                    f'{message2.author.mention} using {message1.content}'
                                DatabaseTools.editPlayerScore(message1.author.id, True, 'rps')
                                DatabaseTools.editPlayerScore(message2.author.id, False, 'rps')
                                await sent_embed.edit(embed=embed)
                            else:
                                embed.description = f'{message2.author.mention} won against ' \
                                                    f'{message1.author.mention} using {message2.content}'
                                DatabaseTools.editPlayerScore(message1.author.id, False, 'rps')
                                DatabaseTools.editPlayerScore(message2.author.id, True, 'rps')
                                await sent_embed.edit(embed=embed)
                        working = False
                    except Exception as e:
                        me = await self.bot.fetch_user(config.personal_id)
                        await me.send(f"Failed to update scores in rps: {e}")
                        embed.description = f'Profile scores failed to update. If this problem persists, report' \
                                            f' it using command +bug <message>'
                        await ctx.send(embed=embed)


        if reaction.emoji == '🤖':
            p2 = self.bot.user

            embed.set_author(name=f'Rock Paper Scissors (AI)', icon_url='https://cdn.discordapp.com/attachments/'
                                                                        '488700267060133889/808744030618779658/'
                                                                        'b680a062246147.5a8a773c6932d.gif')
            embed.description = f'{p1.mention}: DM me `rock`, `paper`, or `scissors`'
            await sent_embed.edit(embed=embed)


            while working:

                message1 = await self.bot.wait_for('message', timeout=60.0, check=check_message)
                await message1.channel.send(f'✅ {message1.content} received')

                message2 = random.choice(['rock', 'paper', 'scissors'])


                if message1.content == message2:
                    embed.description = f'{p1.mention} and {p2.mention} tied using {message2}. DM me `rock`, ' \
                                        f'`paper`, or `scissors`'
                    await sent_embed.edit(embed=embed)
                else:
                    try:
                        DatabaseTools.addPlayer(message1.author.id, message1.author.name, 'rps')
                        DatabaseTools.addPlayer(p2.id, p2.name, 'rps')
                        embed.set_footer(text='')
                        x = [message1.content, message2]
                        if 'rock' in x and 'paper' in x:
                            if message1.content == 'paper':
                                embed.description = f'{message1.author.mention} won against {p2.mention} using ' \
                                                    f'`{message1.content}`'
                                DatabaseTools.editPlayerScore(message1.author.id, True, 'rps')
                                DatabaseTools.editPlayerScore(p2.id, False, 'rps')
                                await sent_embed.edit(embed=embed)
                            else:
                                embed.description = f'{p2.mention} won against {message1.author.mention} using ' \
                                                    f'`{message2}`'
                                DatabaseTools.editPlayerScore(message1.author.id, False, 'rps')
                                DatabaseTools.editPlayerScore(p2.id, True, 'rps')
                                await sent_embed.edit(embed=embed)

                        elif 'paper' in x and 'scissors' in x:
                            if message1.content == 'scissors':
                                embed.description = f'{message1.author.mention} won against {p2.mention} using' \
                                                    f' `{message1.content}`'
                                DatabaseTools.editPlayerScore(message1.author.id, True, 'rps')
                                DatabaseTools.editPlayerScore(p2.id, False, 'rps')
                                await sent_embed.edit(embed=embed)
                            else:
                                embed.description = f'{p2.mention} won against {message1.author.mention} using ' \
                                                    f'`{message2}`'
                                DatabaseTools.editPlayerScore(message1.author.id, False, 'rps')
                                DatabaseTools.editPlayerScore(p2.id, True, 'rps')
                                await sent_embed.edit(embed=embed)

                        elif 'scissors' in x and 'rock' in x:
                            if message1.content == 'rock':
                                embed.description = f'{message1.author.mention} won against {p2.mention} using ' \
                                                    f'`{message1.content}`'
                                DatabaseTools.editPlayerScore(message1.author.id, True, 'rps')
                                DatabaseTools.editPlayerScore(p2.id, False, 'rps')
                                await sent_embed.edit(embed=embed)
                            else:
                                embed.description = f'{p2.mention} won against {message1.author.mention} using ' \
                                                    f'`{message2}`'
                                DatabaseTools.editPlayerScore(message1.author.id, False, 'rps')
                                DatabaseTools.editPlayerScore(p2.id, True, 'rps')
                                await sent_embed.edit(embed=embed)
                        working = False
                    except Exception as e:
                        me = await self.bot.fetch_user(285879705989677058)
                        await me.send(f"Error in rps: {e}-----{type(e)}-----{e.args}-----{ctx.guild}")
                        embed.description = f'Profile scores failed to update. If this problem persists, report it ' \
                                            f'using command +bug <message>'
                        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(rockpaperscissors(bot))
