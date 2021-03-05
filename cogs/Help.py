import discord
from discord.ext import commands


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

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
        em.add_field(name="**Examples**", value="!hatch red\n!hatch normal\n!hatch shiny white")

        await ctx.send(embed=em)


def setup(bot):
    bot.add_cog(Help(bot))
