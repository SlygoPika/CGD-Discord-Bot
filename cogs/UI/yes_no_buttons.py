import discord
from discord.ext import commands

class YesNoButton(discord.ui.Button):
    def __init__(self, is_yes, switch_interaction=None, on_click=None, join_team_name=""):
        style = discord.ButtonStyle.danger if is_yes else discord.ButtonStyle.primary
        super().__init__(style=style, label="Yes" if is_yes else "No")
        self.on_click = on_click
        self.is_yes = is_yes
        self.switch_interaction = switch_interaction
        self.join_team_name = join_team_name

    async def callback(self, interaction: discord.Interaction):
        if self.is_yes:
            print("yes")
            await self.on_click(interaction=self.switch_interaction, team_name=self.join_team_name, approved=True)
            #delete the interaction response
            await interaction.response.send_message(f"You switched team!", ephemeral=True, delete_after=8)
            await self.switch_interaction.delete_original_response()
        else:
            await interaction.response.send_message(f"You stayed on the same team.", ephemeral=True, delete_after=8)
            await self.switch_interaction.delete_original_response()

class YesNoButtonView(discord.ui.View):
    def __init__(self, on_yes, switch_interaction, join_team_name=""):
        super().__init__(timeout=None)
        self.on_yes = on_yes
        self.add_item(YesNoButton(on_click=on_yes, is_yes=True, switch_interaction=switch_interaction, join_team_name=join_team_name))
        self.add_item(YesNoButton(on_click=None, is_yes=False, switch_interaction=switch_interaction, join_team_name=""))