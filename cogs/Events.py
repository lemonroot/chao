import discord
from discord.ext import commands


# ctx = author, name = item name, color = item color OR null,
# val = value, qua = quantity, img = image, src = received/bought/found/etc, #rarity = ★★★☆☆ etc
class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    async def embed_item(self, ctx, name, color, val, qua, img, src, rarity, footer):
        embed = discord.Embed(
            title='Event',
            description=(ctx.author.mention + ' ' + src + ' ' + str(qua) + ' **' + name + '**!'),
            color=ctx.author.color,
        )
        embed.set_image(url=img)
        if color != 'null':
            embed.add_field(name='Color', value=color, inline='True')
        embed.add_field(name='Value', value=val, inline='True')
        embed.add_field(name='Rarity', value=rarity, inline='True')
        embed.set_footer(text=footer)

        await ctx.send(embed=embed)

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
        embed.add_field(name="Examples", value="!chao\n!chao 1\n!chao ChaoBot", inline="False")
        embed.add_field(name="Examples", value="!name\n!name ChaoBot", inline="False")

        await ctx.send(embed=embed)

    async def embed_NPC(self, ctx, npc, text, img, footer, steps, member: discord.Member = None):
        member = member or ctx.author
        bot = self.bot.user
        embed = discord.Embed(
            title=npc,
            description=text,
            color=ctx.author.color,
        )
        embed.set_image(url=img)
        embed.add_field(name='Instructions', value=steps, inline='True')
        embed.set_footer(text=footer)

        await ctx.send(embed=embed)



def setup(bot):
    bot.add_cog(Events(bot))
