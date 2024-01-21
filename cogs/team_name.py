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
        teams = self.bot.get_cog('TeamForming').teams
        for team in teams:
            if team.channel.name == self.roleNameToChannelName(teamName):
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
        teamRole = None
        
        teamForming = self.bot.get_cog('TeamForming')
        
        exists = False
        teamToChange = None
        
        # Check if user is in a team
        for team in self.teams:
            if team.team_leader == ctx.author:
                exists = True
                teamToChange = team
                teamRole = team.team_role
                break
        
        if ctx.channel != teamToChange.team_channel or exists == False:
            self.SetTeamName.reset_cooldown(ctx)
            return
        
        if teamForming.isFrozen:
            await ctx.send(constants.FROZEN_TEAM_TEXT, delete_after=8)
            return

        if not self.teamNameIsValid(newTeamName):
            await ctx.send(f"Your team name must be {constants.TEAM_NAME_MAX_LENGTH} characters or less, start with a letter, and only contain letters and numbers")
            self.SetTeamName.reset_cooldown(ctx)
            return

        if self.teamNameExists(newTeamName):
            await ctx.send("That team name is already taken. Please choose another name.")
            self.SetTeamName.reset_cooldown(ctx)
            return
        
        # Update the team list in TeamForming
        for team in teamForming.teams:
            if team.team_name == teamRole.name:
                team.team_name = newTeamName
                await teamForming.update_team_dropdown()
                break

        await teamRole.edit(name=newTeamName)
        channelName = self.roleNameToChannelName(newTeamName)
        await ctx.channel.edit(name=channelName)

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
