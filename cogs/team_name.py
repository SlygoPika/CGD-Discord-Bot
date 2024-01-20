import discord
from discord.ext import commands
import cogs.utils.user_utils as user
import cogs.utils.constants as constants


class TeamName(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # Returns true if the team name is shorter than 24 characters, starts with a letter, and only contains letters and numbers
    def teamNameIsValid(self, teamName) -> bool:
        return len(teamName) <= constants.TEAM_NAME_MAX_LENGTH and teamName[0].isalpha() and teamName.replace(' ', '').isalnum()

    def teamNameExists(self, teamName):
        teamCategory = self.bot.get_cog('TeamCategory').teamCategory
        for channel in teamCategory.channels:
            if channel.name == self.roleNameToChannelName(teamName):
                return True
        return False

    def roleNameToChannelName(self, roleName):
        return roleName.replace(" ", "-").lower()

    def channelIsInTeamCategory(self, ctx):
        try:
            teamCategory = self.bot.get_cog('TeamCategory').teamCategory
            print(teamCategory.name)
            return ctx.channel.category.name == teamCategory.name
        except:
            return False

    @commands.command()
    @commands.cooldown(1, 300, commands.BucketType.channel)
    async def SetTeamName(self, ctx, newTeamName):
        print("SetTeamName has run with " + newTeamName)
        newTeamName = str(newTeamName.strip())
        currentChannel = ctx.channel
        hasPermissions = False
        teamRole = None
        
        teamForming = self.bot.get_cog('TeamForming')

        # Checking if the user has a role that matches the current channel
        for team in teamForming.teams:
            if team.team_channel.name == currentChannel.name:
                teamRole = team.team_role
                hasPermissions = True
                break

        if not hasPermissions or not self.channelIsInTeamCategory(ctx):
            await ctx.send("You are not in your team's channel")
            return
        print("pass")
        if not self.teamNameIsValid(newTeamName):
            await ctx.send(f"Your team name must be {constants.TEAM_NAME_MAX_LENGTH} characters or less, start with a letter, and only contain letters and numbers")
            return
        print("pass")

        if self.teamNameExists(newTeamName):
            await ctx.send("That team name is already taken. Please choose another name.")
            return
        print("pass")
        
        # Update the team list in TeamForming
        for team in teamForming.teams:
            if team.team_name == teamRole.name:
                team.team_name = newTeamName
                await teamForming.update_team_dropdown()
                break

        await teamRole.edit(name=newTeamName)
        channelName = self.roleNameToChannelName(newTeamName)
        print(channelName)
        await currentChannel.edit(name=channelName)

        await ctx.send(f'Your team name has successfully been set to "{newTeamName}"')
    
    #function called when SetTeamName is on cooldown
    @SetTeamName.error
    async def SetTeamName_error(self, ctx, error):
        print ("on_command_error has run")
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f"SetTeamName is on cooldown. Try again in {error.retry_after:.2f}s.", delete_after=5)
        else:
            print(error)


async def setup(bot):
    await bot.add_cog(TeamName(bot))
