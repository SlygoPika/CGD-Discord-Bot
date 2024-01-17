import discord
from discord.ext import commands
from discord.ext.commands import has_permissions


ADMIN = "Admin"
RESERVED_CHANNEL = "team-forming"


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
    @has_permissions(administrator=True)
    async def setTeamFormingChannel(self, ctx, targetChannel):
        all_channels = ctx.guild.channels  # get all channels
        all_text_channel_dict = {channel.name: channel.id for channel in all_channels if isinstance(
            channel, discord.TextChannel)}

        if targetChannel not in all_text_channel_dict.keys():
            await ctx.send(f'{targetChannel} does not exist. Select an existing channel please')
        else:
            channel_id = all_text_channel_dict[targetChannel]

            target_channel = self.bot.get_channel(channel_id)
            await target_channel.send("React here to join")


async def setup(bot):
    await bot.add_cog(TeamForming(bot))
