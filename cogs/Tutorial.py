import discord
from discord.ext import commands
from cogs.Init import db
from datetime import datetime, timedelta


class Tutorial(commands.Cog):
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
            # Insert user into users table
            post = {"_id": ctx.author.id, "rings": 50}
            users.insert_one(post)

            # Find item in items table
            egg = items.find_one({"_id": 1})
            id = egg.get('_id')
            name = egg.get('name')
            color = egg.get('color')
            val = egg.get('val')
            img = egg.get('img')
            rarity = egg.get('rarity')
            footer = 'Hint: Use !hatch to hatch the egg!'

            # Insert egg into inventory
            # hourtest = datetime.now() + timedelta(hours=1)
            post = {"userid": ctx.author.id, "itemid": id, "name": name, "quantity": 1, "src": "tutorial",
                    "time": datetime.now(), "hatch": datetime.now()}
            inv.insert_one(post)

            event = self.bot.get_cog('Events')
            if event is not None:
                await event.embed_item(ctx, name, color.capitalize(), str(val) + ' rings', 1, img, 'received',
                                       rarity, footer)
                await self.tut1_embed(ctx)
        else:
            await ctx.send('ERROR: You already received an egg! Please use the **!hatch normal** command instead, '
                           'or use **!help hatch** for more info. '
                           + ctx.author.mention)

    async def tut1_embed(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        bot = self.bot.user
        embed = discord.Embed(
            title='Tutorial',
            author=bot,
            description="Now that you've claimed your first egg, it's time to hatch it! Ordinarily, you'd need "
                              "to wait a while until your egg was ready to hatch. However, this egg is good to go! "
                              "\n\nGo ahead and give the **!hatch normal** command a try!",
            color=ctx.author.color,
        )
        embed.add_field(name='Command', value='!hatch normal', inline='True')

        await ctx.send(embed=embed)

    async def tut2_embed(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        bot = self.bot.user

        users = db["users"]
        chao = db["chao"]
        chaoinst = chao.find_one({"userid": ctx.author.id})
        active = chaoinst.get("_id")
        users.update({"_id": ctx.author.id}, {"$set": {"active": active}})

        embed = discord.Embed(
            title='Tutorial',
            author=bot,
            description="**Congratulations**, you did it! \n\nYou can view your chao with the **!chao** command. You might "
                              "notice that your chao's name is just Chao... but don't you think they deserve something"
                              " a bit more creative? \n\nUse the **!name** command to visit the fortune teller and name your "
                              "chao!",
            color=ctx.author.color,
        )
        embed.add_field(name='Command', value='!chao', inline='True')
        embed.add_field(name='Command', value='!name', inline='True')
        embed.add_field(name="Examples", value="!chao\n!chao 1\n!chao Chaobert", inline="False")
        embed.add_field(name="Examples", value="!name\n!name Chaobert", inline="False")

        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Tutorial(bot))
