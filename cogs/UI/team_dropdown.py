import discord
from discord.ext import commands

class TeamDropdown(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="Option 1", description="This is the first option"),
            discord.SelectOption(label="Option 2", description="This is the second option"),
        ]    
        
        super().__init__(placeholder="Select an option...", min_values=1, max_values=1, options=options)
        
    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"You selected {self.values[0]}", ephemeral=True)

class TeamDropdownView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(TeamDropdown())