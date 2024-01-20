import discord
from discord.ext import commands
import cogs.utils.constants as constants

button_emoji = constants.DEFAULT_TEAM_CREATE_EMOJI

class TeamCreateButtonView(discord.ui.View):
    def __init__(self, on_team_create, emoji=constants.DEFAULT_TEAM_CREATE_EMOJI):
        super().__init__()
        self.on_team_create = on_team_create
        button_emoji = emoji

    @discord.ui.button(label="Create Team", style=discord.ButtonStyle.primary, emoji=button_emoji)
    async def button_callback(self, interaction: discord.Interaction, button):
        await self.on_team_create(interaction=interaction)
        await interaction.response.send_message(f"You created a team!", ephemeral=True, delete_after=8)