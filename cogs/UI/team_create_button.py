import discord
from discord.ext import commands
import cogs.utils.constants as constants


class TeamCreateButton(discord.ui.Button):
    def __init__(self, on_team_create, emoji=constants.DEFAULT_TEAM_CREATE_EMOJI):
        super().__init__(style=discord.ButtonStyle.primary, label="Create Team", emoji=emoji)
        self.on_team_create = on_team_create
        self.cooldown = commands.CooldownMapping.from_cooldown(1, 180, commands.BucketType.member)

    async def callback(self, interaction: discord.Interaction):
        interaction.message.author = interaction.user
        bucket = self.cooldown.get_bucket(interaction.message)
        retry_after = bucket.update_rate_limit()
        if retry_after:
            await interaction.response.send_message(f"You can't create a team for another {round(retry_after, 1)} seconds.", ephemeral=True, delete_after=8)
            return
        
        await self.on_team_create(interaction=interaction)
        await interaction.response.send_message(f"You created a team!", ephemeral=True, delete_after=8)

class TeamCreateButtonView(discord.ui.View):
    def __init__(self, on_team_create, emoji=constants.DEFAULT_TEAM_CREATE_EMOJI):
        super().__init__(timeout=None)
        self.on_team_create = on_team_create
        self.add_item(TeamCreateButton(on_team_create=on_team_create, emoji=emoji))