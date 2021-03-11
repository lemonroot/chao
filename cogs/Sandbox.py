import discord
from discord.ext import commands
from cogs.Init import db
from numpy.random import choice


class Sandbox(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command(name='hello')
    async def hello_command(self, ctx, *, member: discord.Member = None):
        member = member or ctx.author
        if self._last_member is None or self._last_member.id != member.id:
            await ctx.send('Hello {0.name}~'.format(member))
        else:
            await ctx.send('Hello {0.name}... This feels familiar.'.format(member))
        self._last_member = member

    @commands.command(name='stats')
    async def stattest(self, ctx):
        stats = ["S", "A", "B", "C", "D", "E"]
        statdist = choice(stats, 5, p=[0.01, 0.05, 0.14, 0.3, 0.3, 0.2])
        await ctx.send(statdist)

def setup(bot):
    bot.add_cog(Sandbox(bot))
