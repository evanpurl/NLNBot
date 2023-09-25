import asyncio
import datetime
import discord
from discord import app_commands, ui
from discord.ext import commands


async def assemblepollembed(bot, server, role, information, pollname):
    if role is None:
        embed = discord.Embed(title=f"{pollname}",
                              description=f"Made using the poll command.", color=discord.Color.blue(),
                              timestamp=datetime.datetime.now())
    else:
        embed = discord.Embed(title=f"{pollname}",
                              description=f"{role.mention} Made using the poll command.", color=discord.Color.blue(),
                              timestamp=datetime.datetime.now())
    embed.set_thumbnail(url=server.icon.url)
    embed.add_field(name="Information", value=information, inline=False)
    embed.set_footer(text=f"{bot.user.name}")
    return embed


async def assemblepollendembed(bot, server, msg):
    reactions = [msg.reactions[0].count, msg.reactions[1].count]
    embed = discord.Embed(title=f"Poll Ended",
                          description=f"Made using the poll command.", color=discord.Color.blue(),
                          timestamp=datetime.datetime.now())
    embed.set_thumbnail(url=server.icon.url)
    embed.add_field(name="❌", value=reactions[0]-1, inline=True)
    embed.add_field(name="✅", value=reactions[1]-1, inline=True)
    embed.set_footer(text=f"{bot.user.name}")
    return embed


class pollmodal(ui.Modal, title='Poll Information'):

    def __init__(self, bot, channel, role, time):
        super().__init__()
        self.bot = bot
        self.channel = channel
        self.role = role
        self.time = time
        self.timehours = time

    name = ui.TextInput(label='Poll Name:', style=discord.TextStyle.short,
                        placeholder="N/A", required=True)
    information = ui.TextInput(label='Poll Information:', style=discord.TextStyle.paragraph,
                               placeholder="N/A", required=True)

    async def on_submit(self, interaction: discord.Interaction):
        try:
            msg = await self.channel.send(
                embed=await assemblepollembed(self.bot, interaction.guild, self.role, self.information, self.name))

            await msg.add_reaction("❌")
            await msg.add_reaction("✅")

            msgid = msg.id

            if self.time != 0:
                self.time = self.time * 3600  # Converts timer from hours to seconds.

                await interaction.response.send_message(
                    content=f"Poll created at {msg.jump_url}, timer started for {self.timehours} hours.",
                    ephemeral=True)

                while True:
                    await asyncio.sleep(60)
                    self.time -= 60
                    if self.time <= 0:
                        cache_msg = discord.utils.get(self.bot.cached_messages, id=msgid)
                        await cache_msg.reply(embed=await assemblepollendembed(self.bot, interaction.guild, cache_msg))
                        await cache_msg.clear_reactions()  # Clears reactions from previous poll.
                    break

            else:
                await interaction.response.send_message(
                    content=f"Poll created at {msg.jump_url}.",
                    ephemeral=True)


        except Exception as e:
            print(e)


class pollcmd(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.has_permissions(manage_channels=True)
    @app_commands.command(name="poll", description="Command used to start a new poll.")
    async def poll(self, interaction: discord.Interaction, channel: discord.TextChannel,
                   roletotag: discord.Role = None, timerhrs: int = None):
        try:
            if timerhrs == 0:
                timerhrs = None  # Default no timer
            await interaction.response.send_modal(pollmodal(self.bot, channel, roletotag, timerhrs))

        except Exception as e:
            print(e)

    @poll.error
    async def onerror(self, interaction: discord.Interaction, error: app_commands.MissingPermissions):
        await interaction.response.send_message(content=error,
                                                ephemeral=True)


async def setup(bot):
    await bot.add_cog(pollcmd(bot))
