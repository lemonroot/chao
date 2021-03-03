import discord
from discord.ext import commands
from cogs import Events
from discord.utils import get
import os
import time
import json


class Begin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command(name='begin', aliases=['start'])
    async def _begin(self, ctx, *, member: discord.member = None):
        member = member or ctx.author

        if member == self.bot.user:
            return

        if not os.path.exists('profiles/{}'.format(ctx.author.id)):
            os.makedirs('profiles/{}'.format(ctx.author.id) + '/chao1')
            directory = ('profiles/' + str(ctx.author.id) + '/chao1/info.json')

            with open('data/dummyacc.json', 'r') as f:
                new_account = json.load(f)
            with open(directory, 'w') as f:
                json.dump(new_account, f)
            event = self.bot.get_cog('Events')
            if event is not None:
                await event.embed_chao(ctx)
        else:
            await ctx.send('ERROR: You already have a chao! Please use the **!hatch** command instead. '
                           + ctx.author.mention)




def setup(bot):
    bot.add_cog(Begin(bot))
