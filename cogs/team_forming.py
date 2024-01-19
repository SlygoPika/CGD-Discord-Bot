import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
import cogs.utils.constants as constants
import cogs.utils.channel_utils as channels
from cogs.UI.team_dropdown import TeamDropdownView


class TeamForming(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.create_message_id = None
        self.message_url = None

    @commands.command()
    @has_permissions(administrator=True)
    async def SetTeamFormingChannel(self, ctx, targetChannel):
        '''
        Creates message where people can react to to join a team
        '''
        if self.create_message_id != None:
            await ctx.send(f'Create team message already exists here {self.message_url}')
            return

        all_channels = ctx.guild.channels  # get all channels

        all_text_channel_dict = {channel.name: channel.id for channel in all_channels if isinstance(
            channel, discord.TextChannel)}

        if targetChannel not in all_text_channel_dict.keys():
            await ctx.send(f'{targetChannel} does not exist. Select an existing channel please')
        else:
            channel_id = all_text_channel_dict[targetChannel]
            target_channel = self.bot.get_channel(channel_id)
            create_message = await target_channel.send(constants.CREATE_TEAM_MESSAGE)
            self.create_message_id = create_message.id
            self.message_url = create_message.jump_url
            
            #add emoji reaction to message
            await create_message.add_reaction(self.bot.get_cog('TeamEmoji').team_create_emoji)
            
            join_message = await target_channel.send(constants.JOIN_TEAM_MESSAGE, view=TeamDropdownView())
            self.join_message_id = join_message.id
            #self.message_url = join_message.jump_url
            
            await ctx.send(f'{self.message_url} has been set up as the team forming channel.')

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        '''
        Creates new team channel on react of specific message
        '''
        
        #check if the reaction is not from the bot
        if payload.member.bot:
            return

        guild_id = payload.guild_id
        member = payload.member
        message_id = payload.message_id
        channel_id = payload.channel_id

        if message_id != self.create_message_id:
            return

        guild = await self.bot.fetch_guild(guild_id)
        # so that new text channels goes into the specific category for teams
        teamCategory = self.bot.get_cog('TeamCategory').teamCategory

        if teamCategory is None:
            return

        # Get the existing teams and count the number of teams
        existing_teams = [role.name for role in guild.roles]

        title = channels.auto_team_channel_naming(existing_teams)

        team_count = 0
        title = f"{constants.NEW_TEAM_NAME_PREFIX}{str(team_count).zfill(4)}"

        while title in existing_teams:
            temp_title = f"{constants.NEW_TEAM_NAME_PREFIX}{str(team_count).zfill(4)}"
            if temp_title not in existing_teams:
                title = temp_title
                break
            team_count += 1

        new_role = await guild.create_role(name=title)

        await member.add_roles(new_role, atomic=True)

        # permissions for team
        overwrites = {
            new_role: discord.PermissionOverwrite(read_messages=True),
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            member: discord.PermissionOverwrite(read_messages=False)
        }

        channel = await guild.create_text_channel(title, category=teamCategory, overwrites=overwrites)

        await channel.send(f"You have joined {title}")


async def setup(bot):
    await bot.add_cog(TeamForming(bot))
