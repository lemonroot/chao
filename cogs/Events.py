import discord
from discord.ext import commands
from discord.utils import get
import os
import time
import json


class Events(commands.Cog):
    async def embed_chao(self, ctx):
        embed = discord.Embed(
            title='Event',
            description=(ctx.author.mention + ' found a chao egg!'),
            colour=discord.Colour.blue()
        )

        embed.set_image(url='https://i.imgur.com/AQmDl2s.png')
        embed.add_field(name='Color', value='Normal', inline='True')
        embed.add_field(name='Value', value='0 rings', inline='True')
        embed.set_footer(text='Hint: Use !hatch to hatch the egg!')

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Events(bot))
