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


class pollmodal(ui.Modal, title='Poll Information'):

    def __init__(self, bot, channel, role):
        super().__init__()
        self.bot = bot
        self.channel = channel
        self.role = role

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

            await interaction.response.send_message(content=f"Poll created at {msg.jump_url}",
                                                    ephemeral=True)
        except Exception as e:
            print(e)


class pollcmd(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.has_permissions(manage_channels=True)
    @app_commands.command(name="poll", description="Command used to start a new poll.")
    async def poll(self, interaction: discord.Interaction, channel: discord.TextChannel,
                   roletotag: discord.Role = None):
        try:
            await interaction.response.send_modal(pollmodal(self.bot, channel, roletotag))

        except Exception as e:
            print(e)

    @poll.error
    async def onerror(self, interaction: discord.Interaction, error: app_commands.MissingPermissions):
        await interaction.response.send_message(content=error,
                                                ephemeral=True)


async def setup(bot):
    await bot.add_cog(pollcmd(bot))
