import discord
import os
import logging
from discord.ext import commands
from dotenv import load_dotenv
import pymongo
from pymongo import MongoClient
load_dotenv()

logger = logging.getLogger('discord')
logger.setLevel(logging.WARNING)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

# COMMAND PREFIX IS !
client = commands.Bot(command_prefix='!', help_command=None)


@client.event
async def on_ready():
    print(f'{client.user.name} online.')
    print(f'With ID: {client.user.id}')


# ATTACH COGS
client.load_extension('cogs.Admin')     # Admin commands
client.load_extension('cogs.Basic')     # Basic chao commands - hatch, play, explore, etc.
client.load_extension('cogs.Tutorial')     # New player init
client.load_extension('cogs.Events')    # Event embeds
client.load_extension('cogs.Help')      # Help commands
client.load_extension('cogs.Init')      # Bot initialization commands
client.load_extension('cogs.Sandbox')   # Experimental commands
client.load_extension('cogs.School')    # Chao school commands

client.run(os.getenv('BOT_TOKEN'))
