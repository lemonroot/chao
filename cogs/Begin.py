import discord
from discord.ext import commands
from cogs.Init import db


class Begin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command(name='begin', aliases=['start'])
    async def _begin(self, ctx, *, member: discord.member = None):
        member = member or ctx.author

        if member == self.bot.user:
            return

        users = db["users"]
        inv = db["inventory"]
        items = db["items"]

        myquery = {"_id": ctx.author.id }
        search = users.count_documents(myquery)
        if search == 0:
            # INSERT USER IF DOESN'T EXIST
            post = {"_id": ctx.author.id, "rings": 50}
            users.insert_one(post)

            egg = items.find_one({"_id": 1})
            name = egg.get('name')
            color = egg.get('color')
            val = egg.get('val')
            img = egg.get('img')

            event = self.bot.get_cog('Events')
            if event is not None:
                await event.embed_chao(ctx, name, color.upper(), str(val) + ' rings', img)
        else:
            await ctx.send('ERROR: You already received an egg! Please use the **!hatch normal** command instead, '
                           'or use **!help hatch** for more info. '
                           + ctx.author.mention)


def setup(bot):
    bot.add_cog(Begin(bot))
