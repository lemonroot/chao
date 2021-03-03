import discord
from discord.ext import commands
from discord.utils import get
import os
import time
import json


class Events(commands.Cog):
    async def embed_chao(self, ctx, egg, val, img):
        embed = discord.Embed(
            title='Event',
            description=(ctx.author.mention + ' found a chao egg!'),
            color=ctx.author.color
        )

        embed.set_image(url=img)
        embed.add_field(name='Color', value=egg, inline='True')
        embed.add_field(name='Value', value=val, inline='True')
        embed.set_footer(text='Hint: Use !hatch to hatch the egg!')

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Events(bot))