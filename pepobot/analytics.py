print("IMPORT: %s" % __name__)

from . import config
from . import functions
from . import discord
from . import entropy

import time

lastMessageChannels = {}

@discord.bot.event
async def on_message(message):
	#this controls the entropy pool size, to make sure its at least x of the start
	entropy.monitorPool()

	if config.cfg['bot']['debug'] == 1:
		print("Server: {0.server} #{0.channel} User: {0.author} (ID:{0.author.id}) Message: {0.content}".format(message))

	if message.author.id == discord.bot.user.id:
		rateLimitNewMessage(message.channel.id)
		return

	if rateLimitAllowProcessing(message) is True:
		await discord.bot.process_commands(message)

def getEventTime():
	return time.time()

#create a dict of all channels and the last time the bot spoke in the channel
def rateLimitNewMessage(channel):
	lastMessageChannels[channel] = int(getEventTime()) #cast the float to an int, add it to a dictionary for all channels

#find the last time the bot spoke in channel, if the bot has never spoken since boot return the ratelimit in config.json
def rateLimitSinceLastMessage(channel):
	try:
		return int(getEventTime()) - lastMessageChannels[channel]
	except KeyError:
		return config.cfg['bot']['rate']

#controls if we should process commands or not
def rateLimitAllowProcessing(msg):
	last = rateLimitSinceLastMessage(msg.channel.id)
	if msg.author.id == config.cfg['administration']['owner']:	
		return True
	elif last >= config.cfg['bot']['rate']:
		return True
	else:
		return False