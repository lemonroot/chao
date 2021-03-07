import discord
from discord.ext import commands
from cogs.Init import db
from datetime import datetime

personality = ["gentle", "naughty", "energetic", "quiet", "big eater", "chatty", "easily bored", "curious", "carefree",
               "smart", "cry baby", "lonely", "naive", "mysterious", "wacky", "rowdy", "tough", "bossy", "curious",
               "nervous", "sweet", "rebellious"]


class Basic(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command(name='hatch')
    async def hatch(self, ctx, arg=None):
        if not arg:
            await ctx.send("Please provide the color of the egg! " + ctx.author.mention)
        else:
            # Get item and inventory collections
            items = db["items"]
            inv = db["inventory"]

            # Find ID for egg of given color
            egg = items.find_one({"color": arg})
            eggid = egg.get("_id")

            # Search player inventory for egg
            myquery = {"userid": ctx.author.id, "itemid": eggid}
            search = inv.count_documents(myquery)
            if search == 0:
                await ctx.send("ERROR: You do not possess any " + arg + " eggs!")
            else:
                invinst = inv.find_one(myquery)
                hatchtime = invinst.get("hatch")
                if datetime.now() > hatchtime:
                    qua = invinst.get("quantity")
                    src = invinst.get("src")
                    await ctx.send("Hatched! This message will be a bit more descriptive in the future...")
                    if qua == 1:
                        # remove item from inventory
                        inv.delete_one(invinst)
                    else:
                        # lower quantity by 1
                        await ctx.send("should lower quantity here " + str(invinst))

                    if src == "tutorial":
                        event = self.bot.get_cog('Events')
                        if event is not None:
                            await ctx.send("Tutorial egg detected")
                            await event.tut2_embed(ctx)
                else:
                    await ctx.send("ERROR: This egg isn't ready to hatch! It needs a bit longer...")


def setup(bot):
    bot.add_cog(Basic(bot))
