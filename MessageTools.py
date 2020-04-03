import discord
import JsonTools


async def sendSimpleEmbed(channel, text, delete):
    sent_msg = await channel.send(
        embed=discord.Embed(description=text, color=0xff0000))
    if delete:
        await sent_msg.delete(delay=10)
    return sent_msg


def correct_command_use(ctx, admin_command):
    data = JsonTools.getDataParsable()
    if ctx.message.channel.id not in data[ctx.guild.name]['noCommandChannels']:
        if admin_command and ctx.author.id in data[ctx.guild.name]['mods']:
            if ctx.message.content.startswith(data[ctx.guild.name]['prefix']):
                return True
        elif not admin_command:
            return True
    else:
        return False


async def addReactions(message, num):
    reactions = ['🇦', '🇧', '🇨', '🇩', '🇪', '🇫', '🇬', '🇭', '🇮', '🇯']
    for n, reaction in enumerate(reactions):
        if n < num:
            await message.add_reaction(reaction)
