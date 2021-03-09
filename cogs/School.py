import discord
from discord.ext import commands
from cogs.Init import db
import random
from bson.objectid import ObjectId


class School(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command(name="name")
    async def name_chao(self, ctx, *, member: discord.member = None):
        member = member or ctx.author
        users = db["users"]
        chao = db["chao"]

        user = users.find_one({"_id": ctx.author.id})
        active = user.get("active")

        chaoinst = chao.find_one({"_id": ObjectId(active)})
        name = chaoinst.get("name")

        with open('data/names.txt', 'r') as f:
            read = f.read()
            array = read.split('\n')
            suggestion = random.choice(array)
        if name == "Chao":
            text = ("Welcome to the fortune-telling house. Oh dear! Your chao doesn't have a name. How about... "
                    "**" + suggestion + "**?")
        else:
            text = ("Hmm... I see. Your chao's name is **" + name + "**? It's a fine name, but I could change"
                                                                           " it if you'd like. How about... **" +
                    suggestion + "**?")
        steps = "Reply yes or no."
        img = "https://chao-island.com/w/images/1/1b/Fortune_teller_chaoicon.png"
        footer = "Hint: The !name command changes the name of your active chao."

        event = self.bot.get_cog('Events')
        if event is not None:
            await event.embed_NPC(ctx, "Fortune Teller", text, img, footer, steps)

        while True:
            try:
                # Await user confirmation
                answer = await self.bot.wait_for('message', check=lambda message: message.author == ctx.author)

                if answer.content.lower() not in ('y', 'yes', 'n', 'no'):
                    await ctx.send("You must reply with yes or no!")

                elif answer.content.lower() in ('yes', 'y'):
                    text = ("I see. Then it is done! Your chao will now be known as... **" + suggestion + "**!")
                    steps = "Null"
                    await event.embed_NPC(ctx, "Fortune Teller", text, img, footer, steps)
                    chao.update({"_id": active}, {"$set": {"name": str(suggestion)}})

                    break
                elif answer.content.lower() in ('no' or 'n'):
                    text = ("Oh? No? Well then... what would you like to name your chao?")
                    steps = "Reply with your desired name."
                    await event.embed_NPC(ctx, "Fortune Teller", text, img, footer, steps)

                    answer = await self.bot.wait_for('message', check=lambda message: message.author == ctx.author)

                    text = ("**" + str(answer.content) + "**? A fine name... Presto! It is done. Your chao is now known as **" + str(answer.content) + "**!")
                    steps = "Null"
                    await event.embed_NPC(ctx, "Fortune Teller", text, img, footer, steps)

                    chao.update({"_id": active}, {"$set": {"name": str(answer.content)}})

                    break
            except ValueError:
                await member.send('Unknown error encountered. Please try again.')


def setup(bot):
    bot.add_cog(School(bot))
