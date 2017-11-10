print("IMPORT: %s" % __name__)

from . import config
from . import discord
from . import functions
from . import entropy

@discord.bot.command(pass_context=True, no_pm=True, hidden=True)
async def fetch(ctx):
    if ctx.message.author.id == config.cfg['administration']['owner']:
        resp = await functions.fetchFrogFromMessage(ctx.message)
        if resp is False:
            await discord.bot.add_reaction(ctx.message, config.cfg['reaction']['failure'])
        else:
            await discord.bot.add_reaction(ctx.message, config.cfg['reaction']['success'])

@discord.bot.command(pass_context=True, no_pm=True, hidden=True)
async def recall(ctx, id: str):
    if ctx.message.author.id == config.cfg['administration']['owner']:
        recalled = await discord.bot.get_message(ctx.message.channel, id)
        getFroggo = await functions.fetchFrogFromMessage(recalled)
        if getFroggo is False:
            await discord.bot.add_reaction(ctx.message, config.cfg['reaction']['failure'])
        else:
            await discord.bot.add_reaction(ctx.message, config.cfg['reaction']['success'])

@discord.bot.group(pass_context=True, no_pm=True, hidden=True)
async def admin(ctx):
    if ctx.message.author.id == config.cfg['administration']['owner']:
        if ctx.invoked_subcommand is None:
            await discord.bot.say('Unknown request')

@admin.command(pass_context=True, no_pm=True, hidden=True)
async def resetpool(ctx):
    if ctx.message.author.id == config.cfg['administration']['owner']:
        health = entropy.findPoolHealth() * 100
        if entropy.resetPool() is True:
            await discord.bot.say('Reset the image entropy pool, {0} in randomized pool. Pool was {1}% before reset.'.format(len(entropy.frogPool), health))