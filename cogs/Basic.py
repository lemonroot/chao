import discord
from discord.ext import commands
from cogs.Init import db

personality = ["gentle", "naughty", "energetic", "quiet", "big eater", "chatty", "easily bored", "curious", "carefree",
               "smart", "cry baby", "lonely", "naive", "mysterious", "wacky", "rowdy", "tough", "bossy", "curious",
               "nervous", "sweet", "rebellious"]


class Basic(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command(name='hatch')
    async def hatch(self, ctx, *args):
        if not args:
            await ctx.send("Please provide the color of the egg! " + ctx.author.mention)
        else:
            await ctx.send(args)


def setup(bot):
    bot.add_cog(Basic(bot))
