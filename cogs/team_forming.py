import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
import cogs.utils.constants as constants
import cogs.utils.channel_utils as channels
from cogs.UI.team_dropdown import TeamDropdownView
from cogs.UI.team_create_button import TeamCreateButtonView
from cogs.UI.yes_no_buttons import YesNoButtonView


class TeamForming(commands.Cog):
    
    class Team:
        def __init__(self, team_name, team_leader, team_members, team_channel, team_role):
            self.team_name = team_name
            self.team_leader = team_leader
            self.team_members = team_members
            self.team_channel = team_channel
            self.team_role = team_role
        
        def add_member(self, member):
            self.team_members.append(member)
        
        def remove_member(self, member):
            for i in range(len(self.team_members)):
                if self.team_members[i].name == member.name:
                    self.team_members.pop(i)
                    break
    
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.create_message_id = None
        self.message_url = None
        self.team_leader_role = None
        self.team_forming_channel = None
        self.join_message = None
        self.switch_team_message = None
        self.teams = []
        self.isFrozen = False
    

    @commands.command()
    @has_permissions(administrator=True)
    async def SetTeamFormingChannel(self, ctx, targetChannel):
        '''
        Creates message where people can react to to join a team
        '''
        if self.create_message_id != None:
            await ctx.send(f'The team-forming channel has already been setup here {self.message_url}')
            return

        all_channels = ctx.guild.channels  # get all channels

        all_text_channel_dict = {channel.name: channel.id for channel in all_channels if isinstance(
            channel, discord.TextChannel)}

        if targetChannel not in all_text_channel_dict.keys():
            await ctx.send(f'{targetChannel} does not exist. Select an existing channel please')
        else:
            channel_id = all_text_channel_dict[targetChannel]
            target_channel = self.bot.get_channel(channel_id)
            self.team_forming_channel = target_channel
            create_message = await target_channel.send(constants.CREATE_TEAM_MESSAGE, view=TeamCreateButtonView(on_team_create=self.on_create_team, emoji=self.bot.get_cog('TeamEmoji').team_create_emoji))
            self.create_message_id = create_message.id
            self.message_url = create_message.jump_url
            
            #add emoji reaction to message
            #await create_message.add_reaction(self.bot.get_cog('TeamEmoji').team_create_emoji)
            
            self.join_message = await target_channel.send(constants.JOIN_TEAM_MESSAGE, view=TeamDropdownView(on_team_select=self.on_team_join))
            self.join_message_id = self.join_message.id
            #self.message_url = join_message.jump_url
            
            # Setting up team leader role
            if constants.TEAM_LEADER_ROLE_NAME in [role.name for role in ctx.guild.roles]:
                self.team_leader_role = [role for role in ctx.guild.roles if role.name == constants.TEAM_LEADER_ROLE_NAME][0]
            else:
                self.team_leader_role = await ctx.guild.create_role(name=constants.TEAM_LEADER_ROLE_NAME, color=discord.Color(0x00ff00))
            
            await ctx.send(f'{self.message_url} has been set up as the team forming channel.')


    #CREATE TEAM
    async def on_create_team(self, interaction: discord.Interaction, approved=False, team_name=""):
        '''
        Creates new team channel on react of specific message
        '''
        print ("on_create_team has run")
        #check if the reaction is not from the bot
        if interaction.user.bot:
            return
        
        #check if Team Editing is frozen
        if self.isFrozen:
            await interaction.response.send_message(constants.FROZEN_TEAM_TEXT, ephemeral=True, delete_after=8)
            return
        
        team_to_leave = None
        #Check if the person reacting is in a team
        for team in self.teams:
            if interaction.user in team.team_members:
                if not approved:
                    if team.team_leader == interaction.user:
                        self.switch_team_message = await interaction.response.send_message("You are the team leader of another team. Are you sure you want to create a new team? Doing so will delete your curent team.", ephemeral=True, view=YesNoButtonView(on_yes=self.on_create_team, switch_interaction=interaction))
                    else:
                        self.switch_team_message = await interaction.response.send_message("You are already in a team. Are you sure you want to create a new team? Doing so will remove you from your current team.", ephemeral=True, view=YesNoButtonView(on_yes=self.on_create_team, switch_interaction=interaction))
                    return
                else:
                    if self.switch_team_message != None:
                        await self.switch_team_message.delete()
                        self.switch_team_message = None
                    team_to_leave = team.team_name
                    break
        
        guild_id = interaction.guild_id
        member = interaction.user
        message_id = interaction.message.id

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
        
        # permissions for team
        overwrites = {
            new_role: discord.PermissionOverwrite(read_messages=True),
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
        }

        channel = await guild.create_text_channel(title, category=teamCategory, overwrites=overwrites)

        await member.add_roles(new_role, atomic=True)
        await member.add_roles(self.team_leader_role, atomic=True)
        
        if team_to_leave != None:
            await self.on_team_leave(interaction=interaction, team_name=team_to_leave)

        await channel.send(f"{member.name} has joined {title}")
        
        new_team = self.Team(team_name=title, team_leader=member, team_members=[member], team_channel=channel, team_role=new_role)
        self.teams.append(new_team)
        
        await self.update_team_dropdown()
        print("team added")
        
    async def on_team_join(self, interaction, team_name, approved=False):
        print("on_team_join has run")
        #await self.team_forming_channel.send(f'You joined team {team_name}!')
        
        if self.isFrozen:
            await interaction.response.send_message(constants.FROZEN_TEAM_TEXT, ephemeral=True, delete_after=8)
            return
        
        if team_name == constants.NO_TEAM_OPTION:
            for team in self.teams:
                if interaction.user in team.team_members:
                    await self.on_team_leave(interaction=interaction, team_name=team.team_name)
                    break
            return
        
        for team in self.teams:
            if team.team_name == team_name:
                
                # Check if the member is already in the team
                if interaction.user in team.team_members:
                    await interaction.response.send_message("You are already in this team.", ephemeral=True)
                    return
                
                # Check if the person is already in a team
                for teamPrev in self.teams:
                    if interaction.user in teamPrev.team_members:
                        if not approved:
                            if teamPrev.team_leader == interaction.user:
                                self.switch_team_message = await interaction.response.send_message("You are the team leader of another team. Are you sure you want to join another team? Doing so will delete your curent team.", ephemeral=True, view=YesNoButtonView(on_yes=self.on_team_join, switch_interaction=interaction, join_team_name=team_name))
                            else:
                                self.switch_team_message = await interaction.response.send_message("You are already in a team. Are you sure you want to join another team? Doing so will remove you from your current team.", ephemeral=True, view=YesNoButtonView(on_yes=self.on_team_join, switch_interaction=interaction, join_team_name=team_name))
                            return
                        else:
                            if self.switch_team_message != None:
                                await self.switch_team_message.delete()
                                self.switch_team_message = None
                            await self.on_team_leave(interaction=interaction, team_name=teamPrev.team_name)
                            break
                
                team.add_member(interaction.user)
                
                if team.team_leader == None:
                    team.team_leader = interaction.user
                    await interaction.user.add_roles(self.team_leader_role, atomic=True)
                
                await team.team_channel.send(f'{interaction.user} joined team {team_name}!')
                # add team role to user
                await interaction.user.add_roles(team.team_role, atomic=True)
                return
    
    async def on_team_leave(self, interaction, team_name):
        print("on_team_leave has run")
        
        for team in self.teams:
            if team.team_name == team_name:
                if interaction.user not in team.team_members:
                    await interaction.response.send_message("You are not in this team.", ephemeral=True)
                    return
                                
                team.remove_member(interaction.user)
                await team.team_channel.send(f'{interaction.user} left team {team_name}!')
                # remove team role from user
                await interaction.user.remove_roles(team.team_role, atomic=True)
                print("team role removed")
                
                if self.team_leader_role in interaction.user.roles:
                    # Delete team
                    for member in team.team_members:
                        await member.remove_roles(team.team_role, atomic=True)
                    
                    await team.team_channel.delete()
                    await team.team_role.delete()
                    
                    await interaction.user.remove_roles(self.team_leader_role, atomic=True)
                    
                    self.teams.remove(team)
                    
                    await self.update_team_dropdown()
                
                return
    
    async def update_team_dropdown(self):
        print("update_team_dropdown has run")
        team_names = [team.team_name for team in self.teams]
        await self.join_message.edit(view=TeamDropdownView(on_team_select=self.on_team_join, teams=team_names))
        print("update_team_dropdown has finished")
    
    @commands.command()
    @has_permissions(administrator=True)
    async def FreezeTeams(self, ctx):
        '''
        Freezes the teams so that no one can join or leave
        '''
        self.isFrozen = True
        await ctx.send("Teams have been frozen!")
    
    @commands.command()
    @has_permissions(administrator=True)
    async def UnfreezeTeams(self, ctx):
        '''
        Unfreezes the teams so that people can join or leave
        '''
        self.isFrozen = False
        await ctx.send("Teams have been unfrozen!")
        
    @commands.command()
    @has_permissions(administrator=True)
    async def HandTeamLeaderTo(self, ctx, newLeader: discord.Member):
        '''
        Hand over team leader role to another member
        '''
        exists = False
        teamToChange = None
        
        # Check if user is a team leader
        for team in self.teams:
            if team.team_leader == ctx.author:
                exists = True
                teamToChange = team
                break
        
        # check if user is in team channel
        if ctx.channel != teamToChange.team_channel:
            return
        
        # check if team editing is frozen
        if self.isFrozen:
            await ctx.send(constants.FROZEN_TEAM_TEXT, delete_after=8)
            return
        
        if not exists:
            await ctx.send("You are not a team leader. Please choose another team.")
            return
        
        # Check if new leader is in the team
        if newLeader not in teamToChange.team_members:
            await ctx.send("That user is not in your team. Please choose another user.")
            return
        
        # Change the team leader
        teamToChange.team_leader = newLeader
        await ctx.author.remove_roles(self.team_leader_role)
        await newLeader.add_roles(self.team_leader_role)
        await ctx.send(f"{newLeader.mention} has successfully been made the team leader of {teamToChange.team_name}.")


async def setup(bot):
    await bot.add_cog(TeamForming(bot))
