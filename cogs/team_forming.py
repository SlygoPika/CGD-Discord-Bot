import discord
from discord.ext import commands
from discord.ext.commands import has_permissions


# message id for react to create team
CREATE_TEAM_MESSAGE_ID = 1197319589151907896
# channel id of the join_message
CHANNEL_ID_FOR_TEAM_CREATION = 1197243258577879171


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

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        print("hello")

        guild_id = payload.guild_id
        print(guild_id)
        guild = await self.bot.fetch_guild(guild_id)
        channel = await guild.create_text_channel("Team 10")
        await channel.send("You have joined Team 10")


async def setup(bot):
    await bot.add_cog(TeamForming(bot))
