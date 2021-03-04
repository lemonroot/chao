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

        myquery = {"_id": ctx.author.id }
        search = users.count_documents(myquery)
        if search == 0:
            post = {"_id": ctx.author.id, "rings": 50}
            users.insert_one(post)

            event = self.bot.get_cog('Events')
            if event is not None:
                await event.embed_chao(ctx, 'Normal', '0 rings', 'https://i.imgur.com/AQmDl2s.png')
        else:
            await ctx.send('ERROR: You already have a chao! Please use the **!hatch normal** command instead, '
                           'or use **!help hatch** for more info. '
                           + ctx.author.mention)


def setup(bot):
    bot.add_cog(Begin(bot))
