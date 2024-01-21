import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
import pandas as pd
import os

class ExportTeamData(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    @has_permissions(administrator=True)
    async def ExportTeamData(self, ctx):
        await ctx.send("Exporting team data...")
        teams = self.bot.get_cog("TeamForming").teams
        
        # Create a Pandas dataframe of format:
        # ID        | Team Name | Team Leader | Team Members
        # 1         | team-1    | user-1      | user-1          | user-2         | user-3
        # ...
        
        new_teams_dict = {
            "ID": [],
            "Team Name": [],
            "Team Leader": [],
            "Team Members": []
        }
        counter = 1
        most_members = 0
        for team in teams:
            new_teams_dict["ID"].append(counter)
            new_teams_dict["Team Name"].append(team.team_name)
            new_teams_dict["Team Leader"].append(team.team_leader)
            
            if len(team.team_members) > most_members:
                most_members = len(team.team_members)
            
            if len(team.team_members) > 0:
                new_teams_dict["Team Members"].append(team.team_members[0].name)
            else:
                new_teams_dict["Team Members"].append("")
            counter += 1

        other_members = []
        
        for i in range(1, most_members):
            print(i)
            other_members.append([])
            for team in teams:
                if len(team.team_members) > i:
                    other_members[i - 1].append(team.team_members[i].name)
                else:
                    other_members[i - 1].append("")
        
        print(new_teams_dict)
        new_teams_df = pd.DataFrame(new_teams_dict)
        counter = new_teams_df.columns.get_loc("Team Members") + 1
        for arr in other_members:
            new_teams_df.insert(counter, "", arr)
            counter += 1
        new_teams_df.to_excel("teams.xlsx", index=False)
        
        # Send the file to the user
        await ctx.send("Here's the team data!", file=discord.File("teams.xlsx"))
        
        # Delete the file
        os.remove("teams.xlsx")
        

async def setup(bot):
    await bot.add_cog(ExportTeamData(bot))
