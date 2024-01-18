import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
import cogs.utils.constants as constants


class TeamForming(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.create_message_id = None
        self.message_url = None

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = member.guild.system_channel
        if channel is not None:
            await channel.send(f'Welcome {member.mention}.')

    @commands.command()
    @has_permissions(administrator=True)
    async def setTeamFormingChannel(self, ctx, targetChannel):
        if self.create_message_id != None:
            await ctx.send(f'Create team message already exists here {self.message_url}')
            return

        all_channels = ctx.guild.channels  # get all channels

        all_text_channel_dict = {channel.name: channel.id for channel in all_channels if isinstance(
            channel, discord.TextChannel)}

        if targetChannel not in all_text_channel_dict.keys():
            await ctx.send(f'{targetChannel} does not exist. Select an existing channel please')
        else:
            channel_id = all_text_channel_dict[targetChannel]
            target_channel = self.bot.get_channel(channel_id)
            message = await target_channel.send("Official: React here to join")
            self.create_message_id = message.id
            self.message_url = message.jump_url

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        guild_id = payload.guild_id
        member = payload.member
        message_id = payload.message_id

        if message_id != self.create_message_id:
            return

        guild = await self.bot.fetch_guild(guild_id)
        teamCategory = self.bot.get_cog('TeamCategory').teamCategory

        if teamCategory is None:
            return

        # Get the existing teams and count the number of teams
        existing_teams = [role.name for role in guild.roles]
        team_count = 0
        title = f"Team-{str(team_count).zfill(4)}"

        while title in existing_teams:
            temp_title = f"Team-{str(team_count).zfill(4)}"
            if temp_title not in existing_teams:
                title = temp_title
                break
            team_count += 1

        new_role = await guild.create_role(name=title)

        await member.add_roles(new_role, atomic=True)

        overwrites = {
            new_role: discord.PermissionOverwrite(read_messages=True),
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            member: discord.PermissionOverwrite(read_messages=False)
        }

        channel = await guild.create_text_channel(title, category=teamCategory, overwrites=overwrites)

        await channel.send(f"You have joined {title}")


async def setup(bot):
    await bot.add_cog(TeamForming(bot))
