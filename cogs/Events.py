import discord
from discord.ext import commands


# ctx = author, name = item name, color = item color OR null,
# val = value, qua = quantity, img = image, src = received/bought/found/etc, #rarity = ★★★☆☆ etc
class Events(commands.Cog):
    async def embed_item(self, ctx, name, color, val, qua, img, src, rarity, footer):
        embed = discord.Embed(
            title='Event',
            description=(ctx.author.mention + ' ' + src + ' ' + str(qua) + ' **' + name + '**!'),
            color=ctx.author.color
        )

        embed.set_image(url=img)
        if color != 'null':
            embed.add_field(name='Color', value=color, inline='True')
        embed.add_field(name='Value', value=val, inline='True')
        embed.add_field(name='Rarity', value=rarity, inline='True')
        embed.set_footer(text=footer)

        await ctx.send(embed=embed)
        event = self.bot.get_cog('Events')
        if event is not None:
            await event.embed_item(ctx, name, color.capitalize(), str(val) + ' rings', 1, img, 'received', rarity,
                                   footer)


def setup(bot):
    bot.add_cog(Events(bot))
