import discord
from discord.ext import commands
from cogs.Init import db


class Sandbox(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command(name='hello')
    async def hello_command(self, ctx, *, member: discord.Member = None):
        member = member or ctx.author
        if self._last_member is None or self._last_member.id != member.id:
            await ctx.send('Hello {0.name}~'.format(member))
        else:
            await ctx.send('Hello {0.name}... This feels familiar.'.format(member))
        self._last_member = member

    @commands.command(name='eggtest')
    async def egg_test(self, ctx, *, member: discord.Member = None):
        member = member or ctx.author

        if member == self.bot.user:
            return

        items = db["items"]

        egg = items.find_one({"_id": 2})
        id = egg.get('_id')
        name = egg.get('name')
        color = egg.get('color')
        val = egg.get('val')
        img = egg.get('img')
        rarity = egg.get('rarity')
        footer = 'Hint: This is only a test!'

        event = self.bot.get_cog('Events')
        if event is not None:
            await event.embed_item(ctx, name, color.capitalize(), str(val) + ' rings', 1, img, 'received', rarity,
                                   footer)


def setup(bot):
    bot.add_cog(Sandbox(bot))
