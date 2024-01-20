import discord
from discord.ext import commands
import cogs.utils.constants as constants

class TeamDropdown(discord.ui.Select):
    def __init__(self, on_team_select, team_options=[]):
        options = []
        
        for team in team_options:
            options.append(discord.SelectOption(label=team))
        
        self.on_team_select = on_team_select
        
        super().__init__(placeholder="Select an option...", min_values=1, max_values=1, options=options)
        
    async def callback(self, interaction: discord.Interaction):
        await self.on_team_select(interaction, self.values[0])
        await interaction.response.send_message(f"You joined {self.values[0]}", ephemeral=True, delete_after=8)

class TeamDropdownView(discord.ui.View):
    def __init__(self, on_team_select, teams=[]):
        super().__init__()
        teams.insert(0, constants.NO_TEAM_OPTION)
        self.add_item(TeamDropdown(on_team_select=on_team_select, team_options=teams))