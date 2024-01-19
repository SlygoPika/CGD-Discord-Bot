import discord
from discord.ext import commands

teams = ["Test"]
class TeamDropdown(discord.ui.Select):
    def __init__(self, on_team_select, team_options=[]):
        options = []
        
        for team in team_options:
            options.append(discord.SelectOption(label=team, description=f"Team {team}"))
        
        self.on_team_select = on_team_select
        
        super().__init__(placeholder="Select an option...", min_values=1, max_values=1, options=options)
        
    async def callback(self, interaction: discord.Interaction):
        await self.on_team_select(interaction, self.values[0])
        await interaction.response.send_message(f"You selected {self.values[0]}", ephemeral=True)

class TeamDropdownView(discord.ui.View):
    def __init__(self, on_team_select, new_team_name=None,):
        super().__init__()
        if new_team_name != None:
            teams.append(new_team_name)
        self.add_item(TeamDropdown(on_team_select=on_team_select, team_options=teams))