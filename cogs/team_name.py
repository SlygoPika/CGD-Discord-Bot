import discord
from discord.ext import commands

class TeamName(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def SetTeamName(self, ctx, teamName):
        print("SetTeamName has run")
        """Says hello"""
        await ctx.send(f'Team name set to {teamName}~')

async def setup(bot):
    await bot.add_cog(TeamName(bot))