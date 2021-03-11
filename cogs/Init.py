import discord
from discord.ext import commands, tasks
from pymongo import MongoClient
from numpy.random import choice

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
        shop = db["shop"]
        items = db["items"]

        # Egg calcs
        probs = ["A,A,A", "A,A,B", "A,B,B"]
        statdist = choice(probs, 1, p=[.8, .15, .05])

        if statdist == "A,A,A":
            cursor = items.aggregate([
                {"$match": {"type": "egg", "src": "shop1"}},
                {"$sample": {"size": 3}}
            ])
            print(list(cursor))
        elif statdist == "A,A,B":
            cursor = items.aggregate([
                {"$match": {"type": "egg", "src": "shop1"}},
                {"$sample": {"size": 2}}
            ])
            print(list(cursor))
            cursor = items.aggregate([
                {"$match": {"type": "egg", "src": "shop2"}},
                {"$sample": {"size": 1}}
            ])
            print(list(cursor))
        elif statdist == "A,B,B":
            cursor = items.aggregate([
                {"$match": {"type": "egg", "src": "shop1"}},
                {"$sample": {"size": 1}}
            ])
            print(list(cursor))
            cursor = items.aggregate([
                {"$match": {"type": "egg", "src": "shop2"}},
                {"$sample": {"size": 2}}
            ])
            print(list(cursor))

        # Fruit calcs

        # Accessory calcs

def setup(bot):
    bot.add_cog(Init(bot))
