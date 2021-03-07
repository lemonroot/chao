import discord
from discord.ext import commands
import random

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command(name="hint")
    async def hint(self, ctx, *, member: discord.Member = None):
        member = member or ctx.author
        with open('data/hints.txt', 'r') as f:
            read = f.read()
            array = read.split('\n')
            quote = random.choice(array)
        em = discord.Embed(title="Hint", description=quote, color=ctx.author.color)

        await member.send(embed=em)

    @commands.group(invoke_without_command=True)
    async def help(self, ctx):
        em = discord.Embed(title="Help", description = "Use !help for extended information.", color=ctx.author.color)

        await ctx.send(embed=em)

    @help.command()
    async def begin(self, ctx):
        em = discord.Embed(title="!begin", description="Use the !begin command to collect your first chao egg and create"
                                                     " your profile. This will only work once. After that, you can use "
                                                     "the **!hatch** command to hatch the egg.", color=ctx.author.color)
        em.add_field(name="**Syntax**", value="!begin")

        await ctx.send(embed=em)

    @help.command()
    async def hatch(self, ctx):
        em = discord.Embed(title="!hatch", description="Use the !hatch command to hatch any eggs you may have. You will"
                                                       " need to specify the color of the egg. Please "
                                                       "note that you can only hatch an egg if it is **ready** to be"
                                                       " hatched.")
        em.add_field(name="**Syntax**", value="!hatch *color*")
        em.add_field(name="**Examples**", value="!hatch red\n!hatch normal\n!hatch shinywhite")

        await ctx.send(embed=em)

    @help.command()
    async def eggtest(self, ctx):
        em = discord.Embed(title="!eggtest", description="Use the !eggtest command to look at various egg events. "
                                                         "The eggs currently available to test are: normal, red, blue, "
                                                         "green, lime, cyan, purple, pink, orange, brown, yellow, black, "
                                                         "gray, white, onyx, ruby, sapphire, garnet, aquamarine, emerald, "
                                                         "amethyst, peridot, topaz, silver, gold, indigo, "
                                                         "crimson, mint, diamond, and pearl.")
        em.add_field(name="**Syntax**", value="!eggtest *color*")
        em.add_field(name="**Examples**", value="!eggtest red\n!eggtest sapphire\n!eggtest brown")

        await ctx.send(embed=em)


def setup(bot):
    bot.add_cog(Help(bot))
