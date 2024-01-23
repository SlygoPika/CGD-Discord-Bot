import discord
from discord.ext import commands
import cogs.utils.constants as constants

class TeamDropdown(discord.ui.Select):
    def __init__(self, on_team_select, team_options=[]):
        options = []
        
        first = True
        for team in team_options:
            if first:
                first = False
                options.append(discord.SelectOption(label=team, description="Leave your current team.", emoji=constants.NO_TEAM_EMOJI))
                continue
            options.append(discord.SelectOption(label=team.team_name, description=f"Join {team.team_leader.name}'s team", emoji=team.team_emoji))
        
        self.on_team_select = on_team_select
        
        super().__init__(placeholder="Select an option...", min_values=1, max_values=1, options=options)
        
    async def callback(self, interaction: discord.Interaction):
        await self.on_team_select(interaction, self.values[0])

class TeamDropdownView(discord.ui.View):
    def __init__(self, on_team_select, teams=[]):
        super().__init__(timeout=None)
        new_teams = [constants.NO_TEAM_OPTION]
        for team in teams:
            new_teams.append(team)
        self.add_item(TeamDropdown(on_team_select=on_team_select, team_options=new_teams))