import discord
from discord.ext import commands
import cogs.utils.constants as constants
from discord.ext.commands import has_permissions

class TeamEmoji(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.team_create_emoji = constants.DEFAULT_TEAM_CREATE_EMOJI

    @commands.command()
    @has_permissions(administrator=True)
    async def SetTeamFormingEmoji(self, ctx, TeamEmoji):
        self.team_create_emoji = TeamEmoji
        await ctx.send(f'The default emoji reaction for creating a team has successfully been set to "{TeamEmoji}"')
    ...

async def setup(bot):
    await bot.add_cog(TeamEmoji(bot))