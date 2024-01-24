import discord
from discord.ext import commands
from discord.ext.commands import has_permissions

class Help(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(aliases=["h", "H", "help"], help="Displays a message explaining the available commands.")
    async def Help(self, ctx):
        embed = discord.Embed(title="Help", description="Here are the commands you can use.", color=0x00ff00)
        for command in self.bot.commands:
            # check if the command has the has_permissions decorator
            if len(command.checks) == 0:
                embed.add_field(name=command.name, value=command.help, inline=False)
            
        await ctx.send(embed=embed)
    
    @commands.command(aliases=["ha", "HA", "helpadmin", "helpAdmin"], help="Admin Command: Displays the admin commands.")
    @has_permissions(administrator=True)
    async def HelpAdmin(self, ctx):
        embed = discord.Embed(title="Help", description="Here are the commands you can use.", color=0x00ff00)
        
        for command in self.bot.commands:
            embed.add_field(name=command.name, value=command.help, inline=False)
            
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Help(bot))
