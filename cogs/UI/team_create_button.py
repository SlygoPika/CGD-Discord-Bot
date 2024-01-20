import discord
from discord.ext import commands
import cogs.utils.constants as constants


class TeamCreateButton(discord.ui.Button):
    def __init__(self, on_team_create, emoji=constants.DEFAULT_TEAM_CREATE_EMOJI):
        super().__init__(style=discord.ButtonStyle.primary, label="Create Team", emoji=emoji)
        self.on_team_create = on_team_create

    async def callback(self, interaction: discord.Interaction):
        await self.on_team_create(interaction=interaction)
        await interaction.response.send_message(f"You created a team!", ephemeral=True, delete_after=8)

class TeamCreateButtonView(discord.ui.View):
    def __init__(self, on_team_create, emoji=constants.DEFAULT_TEAM_CREATE_EMOJI):
        super().__init__()
        self.on_team_create = on_team_create
        self.add_item(TeamCreateButton(on_team_create=on_team_create, emoji=emoji))