import discord
from Cogs.Tools import JsonTools


async def sendSimpleEmbed(channel, text, delete):
    """
    Given a channel, sends default red-colored embed given an embed description with optional deletion
    """
    sent_msg = await channel.send(embed=discord.Embed(description=text, color=0xff0000))
    if delete:
        await sent_msg.delete(delay=10)
    return sent_msg


def correct_command_use(ctx, mod_command):
    """
    Given context and boolean for mod-only, check if command is used correctly
    """
    # TODO implement permission_required instead of this method
    data = JsonTools.getDataParsable()
    guildID = str(ctx.guild.id)
    if ctx.message.channel.id not in data[guildID]['noCommandChannels']:
        if ctx.message.content.startswith(data[guildID]['prefix']):
            if mod_command and ctx.author.id in data[guildID]['mods']:
                    return True
            elif not mod_command:
                return True
    else:
        return False


async def addReactions(message, num):
    """
    Add reactions given a message and number of reactions
    """
    reactions = ['🇦', '🇧', '🇨', '🇩', '🇪', '🇫', '🇬', '🇭', '🇮', '🇯']
    for n, reaction in enumerate(reactions):
        if n < num:
            await message.add_reaction(reaction)
