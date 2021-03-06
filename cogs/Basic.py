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
    async def hatch(self, ctx, arg):
        if not arg:
            await ctx.send("Please provide the color of the egg! " + ctx.author.mention)
        else:
            items = db["items"]
            inv = db["inventory"]

            egg = items.find_one({"color": arg})
            eggid = egg.get("_id")

            myquery = {"userid": ctx.author.id, "itemid": eggid}
            search = inv.count_documents(myquery)
            if search == 0:
                await ctx.send("False")
            else:
                await ctx.send("True")


def setup(bot):
    bot.add_cog(Basic(bot))
