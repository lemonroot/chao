import discord
from discord.ext import commands
from cogs.Init import db


class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command(name='eggtest')
    async def egg_test(self, ctx, arg):
        if ctx.message.author.guild_permissions.administrator:
            items = db["items"]

            egg = items.find_one({"color": arg})
            name = egg.get('name')
            color = egg.get('color')
            val = egg.get('val')
            img = egg.get('img')
            thumb = egg.get('icon')
            rarity = egg.get('rarity')
            footer = str(egg.get('footer')) + ' \nHint: This is only a test!'

            event = self.bot.get_cog('Events')
            if event is not None:
                await event.embed_item(ctx, name, color.capitalize(), str(val) + ' rings', 1, img, thumb, 'received', rarity,
                                       footer)
        else:
            print('no')
            return

    @commands.command(name='setrings')
    async def setrings(self, ctx, arg):
        if ctx.message.author.guild_permissions.administrator:
            users = db["users"]
            users.update_one({"_id": ctx.author.id}, {"$set": {"rings": int(arg)}})


def setup(bot):
    bot.add_cog(Admin(bot))
