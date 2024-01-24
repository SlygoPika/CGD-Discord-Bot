import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
import cogs.utils.constants as constants
import emoji

class TeamAdd(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    def roleNameToChannelName(self, roleName):
        return roleName.replace(" ", "-").lower()

    @commands.command(help=f"Admin command: Adds an already existing team channel/role to the team forming channel. Use in case the bot needs to be rebooted. Usage:\n *$AddTeam <TeamName>*")
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
            team_channel = None
            team_voice_channel = None
            for channel in ctx.guild.channels:
                if f"{teamName} {constants.TEAM_VC_SUFFIX}" in channel.name:
                    team_voice_channel = channel
                elif self.roleNameToChannelName(teamName) in channel.name:
                    team_channel = channel
            team_leader = None
            
            if team_channel == None or team_voice_channel == None:
                ctx.send(f'Team text channel or voice channel could not be found.')
                return

            #Get emoji from team_channel.name
            team_emoji = emoji.distinct_emoji_list(team_channel.name)[0]
            
            team_members = []
            #find all members with teamRole
            for member in ctx.guild.members:
                if team_role in member.roles:
                    if teamForming.team_leader_role in member.roles:
                        team_leader = member
                    team_members.append(member)
                    
            team = teamForming.Team(teamName, team_leader, team_members, team_channel, team_voice_channel, team_role)
            team.team_emoji = team_emoji
            teamForming.teams.append(team)
            await teamForming.update_team_dropdown()
            await ctx.send(f'{teamName} has been added to the teams channel')

async def setup(bot):
    await bot.add_cog(TeamAdd(bot))
