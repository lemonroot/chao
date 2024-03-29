import discord
from discord.ext import commands
from cogs.Init import db
import math


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
            embed.add_field(name='Color', value=color.capitalize(), inline=True)
        embed.add_field(name='Value', value=val, inline=True)
        embed.add_field(name='Rarity', value=rarity, inline=True)
        embed.set_footer(text=footer)

        await ctx.send(embed=embed)

    async def embed_NPC(self, ctx, npc, text, img, footer, steps):
        embed = discord.Embed(
            title=npc,
            description=text,
            color=ctx.author.color,
        )
        embed.set_image(url=img),
        if steps != "Null":
            embed.add_field(name='Instructions', value=steps, inline=True)
        embed.set_footer(text=footer)

        await ctx.send(embed=embed)

    async def embed_chao_list(self, ctx, user, active, chao):
        await ctx.send("test")

        embed = discord.Embed(
            title=(""),
            description="",
            color=ctx.author.color,
        )
        embed.set_thumbnail(url="https://static.wikia.nocookie.net/sonic/images/4/41/Omochao_SR.png")
        embed.set_author(name=(ctx.author.name + "'s Chao"), icon_url=ctx.author.avatar_url)

        cursor = chao.find({"userid": ctx.author.id})
        num = 0
        for s in cursor:
            id = s.get("_id")
            name = s.get("name")
            looks = s.get("looks")
            color = looks[0]
            shiny = looks[1]
            ttone = looks[2]
            data = s.get("data")
            grades = s.get("grades")
            stats = s.get("stats")
            personality = s.get("personality")
            num += 1
            embed.add_field(name="#" + str(num) + ': ' + name, value="**Stats:** " + str(stats[0]) + " Swi / " + str(stats[1]) + " Fly / " + str(stats[2]) + " Pow / " + str(stats[3]) + " Run / " + str(stats[4]) + " Sta"
                                                                     "\n**Personality:** " + personality + "\n**Color:** " + color.capitalize(), inline=True)
        await ctx.send(embed=embed)

    async def embed_shop(self, ctx):
        shop = db["shop"]

        embed = discord.Embed(
            title="Black Market",
            description="Welcome to the Black Market!",
            hint="Hint: You can use !buy to purchase an item.",
            color=ctx.author.color,
        )
        embed.set_image(url="https://chao-island.com/w/images/b/b8/Blackmarketchao.png")

        cursor = shop.find({})
        num = 0
        for s in cursor:
            id = s.get("_id")
            name = s.get("name")
            color = s.get("color")
            type = s.get("type")
            value = s.get("val")
            rarity = s.get("rarity")
            if type == "fruit":
                embed.add_field(name=(str(id) + ': 🍎' + name.capitalize()), value=("Cost: " + str(value) + ' rings\nRarity:' + rarity), inline=False)
            elif type == "hat":
                embed.add_field(name=(str(id) + ': 🎩' + name.capitalize()), value=("Cost: " + str(value) + ' rings\nRarity:' + rarity), inline=False)
            else:
                embed.add_field(name=(str(id) + ': 🥚' + color.capitalize()) + ' egg', value=("Cost: " + str(value) + ' rings\nRarity:' + rarity), inline=False)
        embed.set_footer(text="Hint: Buy an item with the !buy command and the corresponding ID #. Example: !buy 8")
        await ctx.send(embed=embed)

    async def embed_profile(self, ctx, name, chaoinst):
        birth = chaoinst.get("birthday")
        data = chaoinst.get("data")
        age = data[0]
        stats = chaoinst.get("stats")
        grades = chaoinst.get("grades")
        person = chaoinst.get("personality")
        agestr = ['Newborn', 'Child', 'Adult', 'Senior', 'Cocoon']
        intstat = stats[5]
        intlist = ['Infant', 'Average', 'Learned', 'Scholarly', 'Genius']

        intstr = intlist[math.ceil(intstat/25)]

        hunger = data[3]

        month = birth.strftime("%b")

        embed = discord.Embed(
            title=(""),
            description="No description set",
            color=ctx.author.color,
        )

        embed.set_author(name=(name + "'s Profile"), icon_url=ctx.author.avatar_url)
        embed.set_thumbnail(url="https://static.wikia.nocookie.net/sonic/images/d/d1/Sonic_Runners_Normal_Chao.png")
        embed.add_field(name="Birthday", value=(month + ' ' + str(birth.date().day)))
        embed.add_field(name="Age", value=agestr[age])
        embed.add_field(name="Personality", value=person)
        embed.add_field(name="Stats", value=(grades[0] + " **Swim:** Lvl " + str(stats[0]) + "\n" + grades[1] +
                                             " **Fly:** Lvl " + str(stats[1]) + "\n" + grades[1] + " **Power:** Lvl " +
                                             str(stats[2]) + "\n" + grades[2] + " **Run:** Lvl " + str(stats[3]) +
                                             "\n" + grades[3] + " **Stamina:** Lvl " + str(stats[4])), inline=True)
        embed.add_field(name="Intelligence", value=intstr)
        embed.add_field(name="Hunger Meter", value=(int(hunger) * ":blue_square:" + (5-int(hunger)) *
                                                    ":white_large_square:"), inline=False)
        await ctx.send(embed=embed)

    async def embed_inv(self, ctx, inv, rings):
        items = db["items"]
        cursor = inv.find({"userid": ctx.author.id})
        embed = discord.Embed(
            title="",
            description="",
            color=ctx.author.color,
        )
        embed.set_author(name=(ctx.author.name + "'s Inventory"), icon_url=ctx.author.avatar_url)
        embed.add_field(name="Rings", value=rings, inline=False)
        for s in cursor:
            id = s.get("itemid")
            name = s.get("name")
            qua = s.get("quantity")
            src = s.get("src")

            inst = items.find_one({"_id": int(id)})
            type = inst.get("type")
            rarity = inst.get("rarity")
            color = inst.get("color")
            value = inst.get("val")

            if src == "shop1" or "shop2":
                src = "shop"

            if type == "fruit":
                name = name = ('🍎' + name.capitalize())
            elif type == "hat":
                name = name = ('🎩' + name.capitalize())
            else:
                name = ('🥚' + color.capitalize()) + ' egg'
            embed.add_field(name=name, value=("Quantity: " + str(qua) + '\nValue: ' + str(value) + '\nRarity: ' + rarity + '\nSource: ' + src.capitalize()), inline=True)

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Events(bot))
