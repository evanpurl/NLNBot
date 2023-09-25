import datetime
import discord
from discord import app_commands, ui
from discord.ext import commands


class memecmds(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="bozo", description="Command used to call someone a bozo")
    async def bozo(self, interaction: discord.Interaction):
        try:
            await interaction.response.send_message(content="https://media.tenor.com/89Jno9ZDsXIAAAAd/bozo-detected.gif")

        except Exception as e:
            print(e)

    @bozo.error
    async def onerror(self, interaction: discord.Interaction, error: app_commands.MissingPermissions):
        await interaction.response.send_message(content=error,
                                                ephemeral=True)


async def setup(bot):
    await bot.add_cog(memecmds(bot))
