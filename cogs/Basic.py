import discord
from discord.ext import commands
from cogs.Init import db
from datetime import datetime, timedelta
import random
from numpy.random import choice


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
                        invinst.update({"quantity": -1})
                        await ctx.send("should lower quantity here " + str(invinst))

                    await self._create_chao(ctx, arg, src)
                    if src == "tutorial":
                        event = self.bot.get_cog('Tutorial')
                        if event is not None:
                            await event.tut2_embed(ctx)
                else:
                    await ctx.send("ERROR: This egg isn't ready to hatch!")

    async def _create_chao(self, ctx, color, src):
        with open('data/personalities.txt', 'r') as f:
            read = f.read()
            array = read.split('\n')
            person = random.choice(array)
        chao = db["chao"]
        statlist = await self._calc_stats(ctx, src)
        post = {"userid": ctx.author.id, "name": "Chao", "looks": [color, False, True], "data": [0, 0, 0.0, 5, 0],
                "grades": statlist, "stats": [0, 0, 0, 0, 0, 0, 0],
                "personality": person, "birthday": datetime.now()}
        chao.insert_one(post)

    async def _calc_stats(self, ctx, src):
        stats = ["S", "A", "B", "C", "D", "E"]
        if src == 'tutorial':
            statdist = choice(stats, 5, p=[0.01, 0.05, 0.14, 0.3, 0.3, 0.2])
        elif src == 'shop':
            statdist = choice(stats, 5, p=[0.01, 0.05, 0.24, 0.3, 0.2, 0.2])
        return list(statdist)

    @commands.command(name='setactive', aliases=['active', 'setchao'])
    async def set_active(self, ctx, arg=None):
        if not arg:
            await ctx.send("ERROR: Please specify a chao to set as active, or use **!chaolist** to see all of your chao.")
        else:
            chao = db["chao"]
            users = db["users"]

            user = users.find_one({"_id": ctx.author.id})
            chaolist = chao.find_one({"userid": ctx.author.id, "name": arg})
            active = user.get("active")
            if not chaolist:
                await ctx.send("ERROR: You have no chao with this name!")
            else:
                # Get chao's ID to test it against the active field
                chaoid = chaolist.get("_id")
                if chaoid == active:
                    await ctx.send("ERROR: This chao is already active!")
                else:
                    users.update({"_id": ctx.author.id}, {"$set": {"active": chaoid}})
                    await ctx.send("Your active chao has been set to **" + arg + "**!")

    @commands.command(name='rings', aliases=['coins', 'money'])
    async def rings(self, ctx):
        users = db["users"]
        user = users.find_one({"_id": ctx.author.id})
        rings = user.get("rings")
        await ctx.send(ctx.author.mention + ", you currently have " + str(rings) + " rings.")

    @commands.command(name="buy")
    async def buy(self, ctx, arg=None):
        shop = db["shop"]
        inv = db["inventory"]
        users = db["users"]

        # Find current user
        user = users.find_one({"_id": ctx.author.id})
        rings = user.get("rings")

        if not arg:
            await ctx.send(ctx.author.mention + ", please specify the name of what you wish to buy!")
        else:
            inst = shop.find_one({"_id": int(arg)})
            cost = inst.get("val")
            if cost > rings:
                await ctx.send("ERROR: " + ctx.author.mention + ", you cannot afford this!")
            else:
                await ctx.send(ctx.author.mention + ", how many would you like to buy?")

                qua = await self.bot.wait_for('message',
                                                  check=lambda message: message.author == ctx.author)

                total = int(qua.content) * int(cost)
                if total > rings:
                    await ctx.send("ERROR: " + ctx.author.mention + ", you cannot afford this!")
                else:
                    name = inst.get("name")
                    color = inst.get("color")
                    val = cost
                    img = inst.get("img")
                    thumb = inst.get("icon")
                    src = inst.get("src")
                    rarity = inst.get("rarity")
                    footer = inst.get("footer")

                    if not color:
                        event = self.bot.get_cog('Events')
                        if event is not None:
                            await event.embed_item(ctx, name, "null", val, qua.content, img, thumb, "purchased", rarity, footer)
                    else:
                        event = self.bot.get_cog('Events')
                        if event is not None:
                            await event.embed_item(ctx, name, color.capitalize(), val, qua.content, img, thumb, "purchased", rarity, footer)

                    newrings = rings - total
                    users.update_one({"_id": ctx.author.id}, {"$set": {"rings": newrings}})

                    post = {"userid": ctx.author.id, "itemid": int(arg), "name": name, "quantity": int(qua.content), "src": src,
                            "time": datetime.now(), "hatch": (datetime.now() + timedelta(hours=1))}
                    inv.insert_one(post)

    @commands.command(name="profile", aliases=["chao"])
    async def profile(self, ctx, arg=None):
        users = db["users"]
        inv = db["inventory"]
        chao = db["chao"]

        if not arg:
            # Find user's active chao
            user = users.find_one({"_id": ctx.author.id})
            active = user.get("active")

            chaoinst = chao.find_one({"_id": active})

            name = chaoinst.get("name")
            event = self.bot.get_cog('Events')
            if event is not None:
                await event.embed_profile(ctx, name, chaoinst)
        else:
            chaoinst = chao.find_one({"userid": ctx.author.id, "name": str(arg)})
            if not chaoinst:
                await ctx.send(ctx.author.mention + ", you have no chao by that name!")
            else:
                name = chaoinst.get("name")
                event = self.bot.get_cog('Events')
                if event is not None:
                    await event.embed_profile(ctx, name, chaoinst)



def setup(bot):
    bot.add_cog(Basic(bot))
