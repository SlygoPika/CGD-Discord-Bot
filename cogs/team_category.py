import discord
from discord.ext import commands

class TeamCategory(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.teamCategory = None

    @commands.command()
    async def SetTeamCategory(self, ctx, TeamCategory):
        await ctx.send(f'The category for team channels has successfully been set to "{TeamCategory}"')

async def setup(bot):
    await bot.add_cog(TeamCategory(bot))