import discord
from discord.ext import commands
import pymongo
from pymongo import MongoClient

mongo_url = "mongodb+srv://lemonroot:LFijfLSGFtxylftV0uUX@cluster0.5jfol.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
cluster = MongoClient(mongo_url)
db = cluster["ChaoBot"]


class Init(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.Cog.listener()
    async def on_ready(self):
        game = discord.Game('with chao!')
        await self.bot.change_presence(status=discord.Status.online, activity=game)


def setup(bot):
    bot.add_cog(Init(bot))
