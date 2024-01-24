import discord
from discord.ext import commands
import cogs.utils.constants as constants
from discord.ext.commands import has_permissions
import emoji

class TeamEmoji(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.team_create_emoji = constants.DEFAULT_TEAM_CREATE_EMOJI

    @commands.command(help=f"Admin command: Sets the default emoji reaction for creating a team. Default is {constants.DEFAULT_TEAM_CREATE_EMOJI}. Usage:\n *$SetTeamFormingEmoji <TeamEmoji>*")
    @has_permissions(administrator=True)
    async def SetTeamFormingEmoji(self, ctx, TeamEmoji):
        self.team_create_emoji = TeamEmoji
        teamForming = self.bot.get_cog("TeamForming")
        if teamForming is not None:
            if teamForming.isSetup:
                await teamForming.update_team_create_button()
        await ctx.send(f'The default emoji reaction for creating a team has successfully been set to "{TeamEmoji}"')
    
    @commands.command(aliases=['TeamEmoji', 'setTeamEmoji', 'setteamemoji', 'set_team_emoji'], help="Sets your team's emoji. Only available in your channel. 5 minute cooldown. Usage:\n *$SetTeamEmoji \"newTeamEmoji\"*")
    @commands.cooldown(1, 300, commands.BucketType.channel)
    async def SetTeamEmoji(self, ctx, TeamEmoji):
        print("SetTeamEmoji called")
        teamForming = self.bot.get_cog("TeamForming")
        
        for team in teamForming.teams:
            if ctx.author in team.team_members:
                if ctx.channel == team.team_channel:
                    print(TeamEmoji)
                    TeamEmoji = emoji.distinct_emoji_list(TeamEmoji)[0]
                    print(TeamEmoji)
                    if emoji.emoji_count(TeamEmoji) == 1:
                        #Set new channel name
                        new_channel_name = f"{TeamEmoji}{constants.EMOJI_SEPARATOR}{team.team_name.replace(' ', '-').lower()}"
                        await team.team_channel.edit(name=new_channel_name)
                        new_vc_name = f"{TeamEmoji}{constants.EMOJI_SEPARATOR}{team.team_name} {constants.TEAM_VC_SUFFIX}"
                        await team.team_voice_channel.edit(name=new_vc_name)
                        team.team_emoji = TeamEmoji
                        await teamForming.update_team_dropdown()
                        await ctx.send(f'The team emoji for {team.team_name} has successfully been set to "{TeamEmoji}"')
                        return
                    else:
                        await ctx.send("Error: Please input one emoji. The emoji must be a default discord emoji.")
                        self.SetTeamEmoji.reset_cooldown(ctx)
                        return
    
    @SetTeamEmoji.error
    async def SetTeamEmoji_error(self, ctx, error):
        print ("on_command_error has run")
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f"SetTeamEmoji is on cooldown. Try again in {error.retry_after:.2f}s.", delete_after=8)
        else:
            await ctx.send("Error: The emoji must be a default discord emoji.")
            self.SetTeamEmoji.reset_cooldown(ctx)

async def setup(bot):
    await bot.add_cog(TeamEmoji(bot))