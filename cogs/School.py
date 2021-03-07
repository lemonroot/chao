import discord
from discord.ext import commands
from cogs.Init import db
import random


class School(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command(name="name")
    async def name_chao(self, ctx):
        with open('data/names.txt', 'r') as f:
            read = f.read()
            array = read.split('\n')
            name = random.choice(array)
        text = ("Welcome to the fortune-telling house. Oh dear! Your chao doesn't have a name. How about... **" + name + "**?")
        steps = "Reply yes or no."
        img = "https://chao-island.com/w/images/1/1b/Fortune_teller_chaoicon.png"
        footer = "Hint: You don't have to be nice! Say no!"
        event = self.bot.get_cog('Events')
        if event is not None:
            await event.embed_NPC(ctx, "Fortune Teller", text, img, footer, steps)


def setup(bot):
    bot.add_cog(School(bot))
