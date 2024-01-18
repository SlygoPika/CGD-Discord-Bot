import discord
from discord.ext import commands
import cogs.utils.user_utils as user


class TeamName(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # Returns true if the team name is shorter than 16 characters, starts with a letter, and only contains letters and numbers
    def teamNameIsValid(self, teamName) -> bool:
        return len(teamName) <= 16 and teamName[0].isalpha() and teamName.replace(' ','').isalnum()
    
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
        roles = user.get_user_roles(ctx)
        currentChannel = ctx.channel
        hasPermissions = False
        teamRole = None
        
        #Checking if the user has a role that matches the current channel
        for role in roles:
            if self.roleNameToChannelName(role.name) == currentChannel.name:
                #await ctx.send('You have the permissions to change the channel!')
                hasPermissions = True
                teamRole = role
                break
    
        if not hasPermissions or not self.channelIsInTeamCategory(ctx):
            await ctx.send("You are not in your team's channel")
            return
        print("pass")
        if not self.teamNameIsValid(newTeamName):
            await ctx.send("Your team name must be 16 characters or less, start with a letter, and only contain letters and numbers")
            return
        print("pass")
        
        if self.teamNameExists(newTeamName):
            await ctx.send("That team name is already taken. Please choose another name.")
            return
        print("pass")
        
        await teamRole.edit(name=newTeamName)
        channelName = self.roleNameToChannelName(newTeamName)
        print(channelName)
        await currentChannel.edit(name=channelName)
        
        await ctx.send(f'Your team name has successfully been set to "{newTeamName}"')

async def setup(bot):
    await bot.add_cog(TeamName(bot))