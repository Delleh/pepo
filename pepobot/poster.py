import logging

from . import config
from . import discord
from . import functions
from . import entropy

logger = logging.getLogger(__name__)
logger.info("loading...")

@discord.bot.command(pass_context=True, description="Posts images", aliases=config.cfg['bot']['commands']['postimage'])
async def postimage(ctx):
    chosenFrog = entropy.frogFromPool()
    with open(chosenFrog, "rb") as f:
        await discord.bot.send_file(ctx.message.channel, f)

@discord.bot.command(pass_context=True, description="Get the URL to join", aliases=config.cfg['bot']['commands']['joinlink'])
async def joinlink(ctx):
    await discord.bot.say('Add me to your own discord! <https://discordapp.com/oauth2/authorize?client_id={0.user.id}&scope=bot&permissions=0>'.format(discord.bot))

@discord.bot.command(pass_context=True, no_pm=True, description="Allows users to request images to add to the bot.", aliases=config.cfg['bot']['commands']['requestimage'])
async def requestimage(ctx):
    filename = await functions.queueFrogFromMessage(ctx.message)

    if filename is False:
        await discord.bot.add_reaction(ctx.message, config.cfg['reaction']['failure'])
        return
    
    #check to make sure filetype is valid based on hex data not ext
    filenameCheck = functions.getFileType(filename)
    if filenameCheck is False:
        await discord.bot.add_reaction(ctx.message, config.cfg['reaction']['failure'])
        return

    #if we made it this far put it in the pepo-request channel
    await discord.bot.send_message(discord.objectFactory(config.cfg['administration']['requests']),"New suggestion from: **" + ctx.message.author.name + "** from server: **" + ctx.message.server.name + "**")
    with open(filename, "rb") as f:
        await discord.bot.send_file(discord.objectFactory(config.cfg['administration']['requests']), f)
    functions.deleteFrog(filename)