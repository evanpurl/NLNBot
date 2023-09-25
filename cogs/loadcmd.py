import discord
from discord import app_commands
from discord.ext import commands


class loadcmds(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.has_permissions(manage_channels=True)
    @app_commands.command(name="reload", description="Reloads a named cog. Only works if cog is already loaded.")
    async def reload(self, interaction: discord.Interaction, cogname: str):
        try:
            print(f"Reloading {cogname}")
            await self.bot.reload_extension(f"cogs.{cogname}")
            await interaction.response.send_message(content=f"Cog {cogname} reloaded.", ephemeral=True)
            print(f"{cogname} Reloaded")

        except commands.ExtensionNotLoaded:
            await self.bot.load_extension(f"cogs.{cogname}")
            await interaction.response.send_message(content=f"Cog {cogname} loaded.", ephemeral=True)
        except commands.ExtensionNotFound:
            await interaction.response.send_message(content=f"Cog {cogname} not found.", ephemeral=True)
        except Exception as e:
            print(e)

    @commands.has_permissions(manage_channels=True)
    @app_commands.command(name="load", description="Loads a named cog.")
    async def load(self, interaction: discord.Interaction, cogname: str):
        try:
            print(f"Loading {cogname}")
            await self.bot.load_extension(f"cogs.{cogname}")
            await interaction.response.send_message(content=f"Cog {cogname} loaded.", ephemeral=True)
            print(f"{cogname} Loaded")
        except commands.ExtensionAlreadyLoaded:
            await self.bot.reload_extension(f"cogs.{cogname}")
            await interaction.response.send_message(content=f"Cog {cogname} reloaded.", ephemeral=True)
        except commands.ExtensionNotFound:
            await interaction.response.send_message(content=f"Cog {cogname} not found.", ephemeral=True)
        except Exception as e:
            print(e)

    @reload.error
    @load.error
    async def onerror(self, interaction: discord.Interaction, error: app_commands.MissingPermissions):
        await interaction.response.send_message(content=error,
                                                ephemeral=True)


async def setup(bot):
    await bot.add_cog(loadcmds(bot))
