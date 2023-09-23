import discord
from discord import app_commands
from discord.ext import commands


class misccommands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="member_count", description="Gets member count on the current server.")
    async def mcount(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            content=f"Current member count in {interaction.guild.name}: {len([m for m in interaction.guild.members if not m.bot])}",
            ephemeral=True)


async def setup(bot):
    await bot.add_cog(misccommands(bot))
