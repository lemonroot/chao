import discord
from discord.ext import commands


# ctx = author, name = item name, color = item color OR null,
# val = value, qua = quantity, img = image, src = received/bought/found/etc, #rarity = ★★★☆☆ etc
class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    async def embed_item(self, ctx, name, color, val, qua, img, thumb, src, rarity, footer):
        embed = discord.Embed(
            title='Event',
            description=(ctx.author.mention + ' ' + src + ' ' + str(qua) + ' **' + name + '**!'),
            color=ctx.author.color,
        )
        embed.set_image(url=img)
        embed.set_thumbnail(url=thumb)
        if color != 'null':
            embed.add_field(name='Color', value=color, inline='True')
        embed.add_field(name='Value', value=val, inline='True')
        embed.add_field(name='Rarity', value=rarity, inline='True')
        embed.set_footer(text=footer)

        await ctx.send(embed=embed)

    async def embed_NPC(self, ctx, npc, text, img, footer, steps, member: discord.Member = None):
        member = member or ctx.author
        bot = self.bot.user
        embed = discord.Embed(
            title=npc,
            description=text,
            color=ctx.author.color,
        )
        embed.set_image(url=img),
        if steps != "Null":
            embed.add_field(name='Instructions', value=steps, inline='True')
        embed.set_footer(text=footer)

        await ctx.send(embed=embed)

    async def embed_shop(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        bot = self.bot.user
        init = self.bot.get_cog('Init')

        embed = discord.Embed(
            title="Black Market",
            description="Welcome to the Black Market! You can use **!buy** to purchase an item.",
            color=ctx.author.color,
        )
        embed.set_image(url="https://chao-island.com/w/images/b/b8/Blackmarketchao.png")

        embed.add_field(name="List", value=init.update_shop)

        await ctx.send(embed=embed)



def setup(bot):
    bot.add_cog(Events(bot))
