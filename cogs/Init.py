import discord
from discord.ext import commands, tasks
from pymongo import MongoClient
from datetime import datetime

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
        print("The shop would update automatically right now.")


def setup(bot):
    bot.add_cog(Init(bot))
