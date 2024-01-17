import discord
from discord.ext import commands
import cogs.utils.user_utils as user


class TeamName(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    def nameIsValid(self, name):
        return len(name) <= 16 and name.isalnum() and name[0].isalpha() and not name.contains("-")
    
    def roleNameToChannelName(self, roleName):
        return roleName.replace(" ", "-").lower()

    @commands.command()
    async def SetTeamName(self, ctx, newTeamName):
        print("SetTeamName has run")
        
        roles = user.get_user_roles(ctx)
        currentChannel = ctx.channel
        hasPermissions = False
        teamRole = None
        
        for role in roles:
            if self.roleNameToChannelName(role.name) == currentChannel.name:
                #await ctx.send('You have the permissions to change the channel!')
                hasPermissions = True
                teamRole = role
                break
        
        if ctx.author.guild_permissions.administrator:
            #await ctx.send('You have the permissions to change the channel!')
            hasPermissions = True
        
        if not hasPermissions:
            await ctx.send("You are not in your team's channel")
            return
    
        await teamRole.edit(name=newTeamName)
        await currentChannel.edit(name=self.roleNameToChannelName(newTeamName))
        
        await ctx.send(f'Your team name has successfully been set to "{newTeamName}"')

async def setup(bot):
    await bot.add_cog(TeamName(bot))