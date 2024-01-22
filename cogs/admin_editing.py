import discord
from discord.ext import commands
import cogs.utils.constants as constants
from discord.ext.commands import has_permissions

class AdminEditing(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(help=f"Admin Command: Renames an already existing team channel/role. Usage:\n *$RenameTeam <TeamName> <NewTeamName>*")
    @has_permissions(administrator=True)
    async def RenameTeam(self, ctx, teamRole, newTeamName):
        teamForming = self.bot.get_cog('TeamForming')
        newTeamName = str(newTeamName.strip())
        newTeamChannelName = newTeamName.replace(" ", "-").lower()
        
        for team in teamForming.teams:
            if team.team_role.name == teamRole:
                await team.team_role.edit(name=newTeamName)
                newTeamChannelName = f"{team.team_emoji}{constants.EMOJI_SEPARATOR}{newTeamChannelName}"
                await team.team_channel.edit(name=newTeamChannelName)
                await ctx.send(f'Your team name has successfully been set to "{newTeamName}"')
                teamForming.update_team_dropdown()
                return
        await ctx.send("That team name does not exist. Please choose another name.")
    
    @commands.command(help=f"Admin Command: Moves a user to a different team. Usage:\n *$MoveUserToTeam <@User> <Team>*")
    @has_permissions(administrator=True)
    async def MoveUserToTeam(self, ctx, user: discord.Member, teamRole):
        teamForming = self.bot.get_cog('TeamForming')
        exists = False
        newTeam = None
        oldTeam = None
        
        print(user)
        print(teamRole)
        
        # Check if the user is already in a team
        for team in teamForming.teams:
            if user in team.team_members:
                if team.team_leader == user:
                    await ctx.send("You cannot move the team leader to another team.")
                    return
                oldTeam = team
        
        if teamRole == constants.NO_TEAM_OPTION:
            if oldTeam == None:
                await ctx.send("That user is not in a team.")
                return
            else:
                oldTeam.team_members.remove(user)
                await user.remove_roles(oldTeam.team_role)
                await ctx.send(f"{user.mention} has successfully been removed from {oldTeam.team_name}.")
                return
            
        # Check if new team exists
        for team in teamForming.teams:
            if team.team_name == teamRole:
                # Check if user is already in the team
                if user in team.team_members:
                    await ctx.send("That user is already in the team.")
                    return
                exists = True
                newTeam = team
        
        if not exists:
            await ctx.send("That team does not exist. Please choose another team.")
            return
        
        # Remove the user from the old team
        if oldTeam != None:
            oldTeam.team_members.remove(user)
            await user.remove_roles(team.team_role)
        
        # Add the user to the new team
        newTeam.team_members.append(user)
        await user.add_roles(newTeam.team_role)
        await ctx.send(f"{user.mention} has successfully been moved to {teamRole}.")
    
    @commands.command(help=f"Admin Command: Deletes a team. Usage:\n *$DeleteTeam <Team>*")
    @has_permissions(administrator=True)
    async def DeleteTeam(self, ctx, teamRole):
        teamForming = self.bot.get_cog('TeamForming')
        exists = False
        teamToDelete = None
        
        # Check if team exists
        for team in teamForming.teams:
            if team.team_name == teamRole:
                exists = True
                teamToDelete = team
                break
        
        if not exists:
            await ctx.send("That team does not exist. Please choose another team.")
            return
        
        # Delete the team
        await teamToDelete.team_role.delete()
        await teamToDelete.team_channel.delete()
        await teamToDelete.team_leader.remove_roles(teamForming.team_leader_role)
        for team in teamForming.teams:
            if team.team_name == teamToDelete.team_name:
                teamForming.teams.remove(team)
                break
        await ctx.send(f"{teamRole} has successfully been deleted.")
        teamForming.update_team_dropdown()
    
    @commands.command(help=f"Admin Command: Switches the team leader of a team. Usage:\n *$SwitchTeamLeader <@User> <Team>*")
    @has_permissions(administrator=True)
    async def SwitchTeamLeader(self, ctx, user: discord.Member, teamRole):
        teamForming = self.bot.get_cog('TeamForming')
        exists = False
        teamToSwitch = None
        
        # Check if team exists
        for team in teamForming.teams:
            if team.team_name == teamRole:
                exists = True
                teamToSwitch = team
                break
        
        if not exists:
            await ctx.send("That team does not exist. Please choose another team.")
            return
        
        # Check if user is in the team
        if user not in teamToSwitch.team_members:
            await ctx.send("That user is not in the team.")
            return
        
        # Check if user is already the team leader
        if user == teamToSwitch.team_leader:
            await ctx.send("That user is already the team leader.")
            return
        
        # Switch the team leader
        teamToSwitch.team_leader.remove_roles(teamForming.team_leader_role)
        teamToSwitch.team_leader = user
        await user.add_roles(teamForming.team_leader_role)
        await teamForming.update_team_dropdown()
        await ctx.send(f"{user.mention} has successfully been switched to the team leader of {teamRole}.")
    
    @commands.command(help=f"Admin Command: Removes all existing teams. Usage:\n *$ResetTeams*")
    @has_permissions(administrator=True)
    async def ResetTeams(self, ctx):
        print("resetting teams")
        
        teamForming = self.bot.get_cog('TeamForming')
        
        for team in teamForming.teams:
            #remove team leader role from team leader
            await team.team_leader.remove_roles(teamForming.team_leader_role)
            await team.team_role.delete()
            await team.team_channel.delete()
            
        teamForming.teams = []
        await teamForming.update_team_dropdown()
        
        await ctx.send("All teams have successfully been deleted.")
    
    @commands.command(help=f"Admin Command: Prints all existing teams. Usage:\n *$PrintTeams*")
    @has_permissions(administrator=True)
    async def PrintTeams(self, ctx):
        teamForming = self.bot.get_cog('TeamForming')
        for team in teamForming.teams:
            print(team.team_name)
            print(team.team_leader)
            print(team.team_members)
            print()
        
        await ctx.send("Check the console for the teams.")
    
                

async def setup(bot):
    await bot.add_cog(AdminEditing(bot))