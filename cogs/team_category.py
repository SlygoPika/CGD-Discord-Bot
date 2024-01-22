import discord
from discord.ext import commands
from discord.ext.commands import has_permissions

class TeamCategory(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.teamCategory = None
        
    def findCategory(self, ctx, categoryName):
        for category in ctx.guild.categories:
            if category.name.lower() == categoryName.lower():
                return category
        return None

    @commands.command(help=f"Admin command: Sets the category for team channels. Usage:\n *$SetTeamCategory <TeamCategory>*")
    @has_permissions(administrator=True)
    async def SetTeamCategory(self, ctx, TeamCategory):
        self.teamCategory = self.findCategory(ctx, TeamCategory)
        if self.teamCategory == None:
            await ctx.send(f'{TeamCategory} does not exist. Select an existing category please')
        else:
            await ctx.send(f'The category for team channels has successfully been set to "{TeamCategory}"')

async def setup(bot):
    await bot.add_cog(TeamCategory(bot))