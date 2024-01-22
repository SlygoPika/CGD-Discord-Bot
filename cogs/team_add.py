import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
import cogs.utils.constants as constants

class TeamAdd(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    def roleNameToChannelName(self, roleName):
        return roleName.replace(" ", "-").lower()

    @commands.command(help=f"Admin command: Adds an already existing team channel/role to the team forming channel. Usage:\n *$AddTeam <TeamName>*")
    @has_permissions(administrator=True)
    async def AddTeam(self, ctx, teamName):
        # Add an already existing team to the team forming channel
        teamName = str(teamName.strip())
        teamForming = self.bot.get_cog('TeamForming')
        
        all_roles = ctx.guild.roles
        all_role_names = [role.name for role in all_roles]
        if teamName not in all_role_names:
            await ctx.send(f'{teamName} does not exist. Select an existing team please')
            return
        else:
            # Make a new team object
            team_role = discord.utils.get(ctx.guild.roles, name=teamName)
            team_channel = discord.utils.get(ctx.guild.channels, name=f"{constants.DEFAULT_TEAM_EMOJI}{constants.EMOJI_SEPARATOR}{self.roleNameToChannelName(teamName)}")
            team_leader = None
            team_members = []
            team = teamForming.Team(teamName, team_leader, team_members, team_channel, team_role)
            
            teamForming.teams.append(team)
            await teamForming.update_team_dropdown()
            await ctx.send(f'{teamName} has been added to the teams channel')

async def setup(bot):
    await bot.add_cog(TeamAdd(bot))
