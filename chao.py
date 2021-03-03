import discord
import os
import logging
from discord.ext import commands
from dotenv import load_dotenv
from string import ascii_letters, digits
import time
import json
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
client.load_extension('cogs.Init')      # Bot initialization commands
client.load_extension('cogs.Admin')
client.load_extension('cogs.Begin')     # New player command
client.load_extension('cogs.Sandbox')

client.run(os.getenv('BOT_TOKEN'))
