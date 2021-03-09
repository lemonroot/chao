import discord
from discord.ext import commands
from string import ascii_letters, digits
from cogs.Init import db
import random
from bson.objectid import ObjectId
from better_profanity import profanity


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

                else:
                    text = ("Oh? No? Well then... what would you like to name your chao?")
                    steps = "Reply with your desired name."
                    await event.embed_NPC(ctx, "Fortune Teller", text, img, footer, steps)
                    await self.name_try(ctx, event, text, img, footer, steps, chao, active, member)
                    break

            except ValueError:
                await member.send('Unknown error encountered. Please try again.')

    async def name_try(self, ctx, event, text, img, footer, steps, chao, active, member):
        while True:
            try:
                nametry = await self.bot.wait_for('message',
                                                  check=lambda message: message.author == ctx.author)
                length = len(str(nametry.content))
                proftest = profanity.contains_profanity(nametry.content)

                if length > 16:
                    await ctx.send('ERROR: Name is too long. Please try again.')

                elif proftest:
                    await ctx.send('ERROR: Name contains inappropriate language. Please try again.')

                elif set(nametry.content).difference(ascii_letters + digits):
                    await ctx.send(
                        'ERROR: Name contains invalid characters. Only letters and digits allowed. Please try again.')

                else:
                    text = ("**" + str(
                        nametry.content) + "**? A fine name... Presto! It is done. Your chao is now known as **" + str(
                        nametry.content) + "**!")
                    steps = "Null"
                    await event.embed_NPC(ctx, "Fortune Teller", text, img, footer, steps)

                    chao.update({"_id": active}, {"$set": {"name": str(nametry.content)}})
                    break

            except ValueError:
                await member.send('Unknown error encountered. Please try again.')

def setup(bot):
    bot.add_cog(School(bot))
