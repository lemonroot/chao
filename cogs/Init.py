import discord
from discord.ext import commands, tasks
from pymongo import MongoClient
from numpy.random import choice
import datetime

mongo_url = "mongodb+srv://lemonroot:LFijfLSGFtxylftV0uUX@cluster0.5jfol.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
cluster = MongoClient(mongo_url)
db = cluster["ChaoBot"]


class Init(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
        self.update_shop.start()

    @commands.Cog.listener()
    async def on_ready(self):
        game = discord.Game('with chao!')
        await self.bot.change_presence(status=discord.Status.online, activity=game)

    @commands.Cog.listener()
    async def on_message(self, ctx):
        if not ctx.author.bot:
            users = db["users"]
            myquery = {"_id": ctx.author.id}
            search = users.count_documents(myquery)
            if search != 0:
                users.update_one({"_id": ctx.author.id}, {"$inc": {"rings": 1}})
            else:
                return

    @tasks.loop(hours=12)
    async def update_shop(self):
        items = db["items"]
        shop = db["shop"]

        utc_timestamp = datetime.datetime.utcnow()

        # Egg calcs
        probs = ["A,A,A", "A,A,B", "A,B,B"]
        eggdist = choice(probs, 1, p=[.8, .15, .05])

        if eggdist == "A,A,A":
            itemlist = list(items.aggregate([
                {"$match": {"type": "egg", "src": "shop1"}},
                {"$sample": {"size": 3}}
            ]))
        elif eggdist == "A,A,B":
            itemlist = list(items.aggregate([
                {"$match": {"type": "egg", "src": "shop1"}},
                {"$sample": {"size": 2}}
            ]))
            itemlist.append(list(items.aggregate([
                {"$match": {"type": "egg", "src": "shop2"}},
                {"$sample": {"size": 1}}
            ])))
        elif eggdist == "A,B,B":
            itemlist = list(items.aggregate([
                {"$match": {"type": "egg", "src": "shop1"}},
                {"$sample": {"size": 1}}
            ]))
            itemlist.append(list(items.aggregate([
                {"$match": {"type": "egg", "src": "shop2"}},
                {"$sample": {"size": 2}}
            ])))

        # Fruit calcs
        probs = ["A,A,B", "A,A,B,B"]
        fruitdist = choice(probs, 1, p=[.6, .4])

        if fruitdist == "A,A,B":
            itemlist.append(list(items.aggregate([
                {"$match": {"type": "fruit", "src": "shop1"}},
                {"$sample": {"size": 2}}
            ])))
            itemlist.append(list(items.aggregate([
                {"$match": {"type": "fruit", "src": "shop2"}},
                {"$sample": {"size": 1}}
            ])))
        elif fruitdist == "A,A,B,B":
            itemlist.append(list(items.aggregate([
                {"$match": {"type": "fruit", "src": "shop1"}},
                {"$sample": {"size": 2}}
            ])))
            itemlist.append(list(items.aggregate([
                {"$match": {"type": "fruit", "src": "shop2"}},
                {"$sample": {"size": 2}}
            ])))

        # Accessory calcs
        itemlist.append(list(items.aggregate([
            {"$match": {"type": "hat"}},
            {"$sample": {"size": 2}}
        ])))
        print(itemlist)

        # Remove all fields from Black Market collection
        shop.remove({})

        # Insert black market items into shop collection
        for s in range(len(itemlist)):
            shop.insert(itemlist[s])

        return itemlist


def setup(bot):
    bot.add_cog(Init(bot))
