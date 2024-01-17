import discord
from discord.ext import commands
import cogs.utils.user_utils as user

ADMIN = "Admin"


class TeamForming(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.channel = None

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = member.guild.system_channel
        if channel is not None:
            await channel.send(f'Welcome {member.mention}.')

    @commands.command()
    async def setTeamFormingChannel(self, ctx, *, member: discord.Member = None):
        print("Helllo")
        # member_roles = member.roles
        # print(member.name)
        # print(member_roles)
        # print(ctx.author)
        print(user.get_user_roles(ctx))

        # if ADMIN not in member_roles:
        #     return


async def setup(bot):
    await bot.add_cog(TeamForming(bot))
