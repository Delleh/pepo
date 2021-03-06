from . import config
from . import functions
from . import discord
from . import entropy
from . import database

import logging
import time

logger = logging.getLogger(__name__)
logger.info("loading...")

lastMessageChannels = {}

@discord.bot.event
async def on_message(message):
	#this controls the entropy pool size, to make sure its at least x of the start
	entropy.monitorPool()

	#check if the user is blacklisted globally
	database.cursor.execute('SELECT * FROM ignore_user WHERE user=?', (message.author.id,))
	result = database.cursor.fetchone()
	if result is not None:
		return

	if config.cfg['bot']['debug'] == 1:
		logging.info("MSG Server: {0.server} #{0.channel} User: {0.author} (ID:{0.author.id}) Message: {0.content}".format(message))

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