import discord
from discord.ext import commands
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

        else:
            await ctx.send('ERROR: You already have a chao!')


def setup(bot):
    bot.add_cog(Begin(bot))
