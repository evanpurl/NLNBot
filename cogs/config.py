import discord
from discord import app_commands
from discord.ext import commands
from aiomysql import Error

from util.databasefunctions import insert


class setcmd(commands.GroupCog, name="set"):

    def __init__(self, bot):
        self.bot = bot

    @app_commands.checks.has_permissions(manage_channels=True)
    @app_commands.command(name="welcome-channel", description="Command to set your server's welcome channel.")
    async def welcomechannel(self, interaction: discord.Interaction, channel: discord.TextChannel):
        try:

            await insert(self.bot.database, f"""REPLACE INTO server_{str(interaction.guild.id)} (configname, configoption) VALUES( 'welcome_channel', {channel.id})""")
            await interaction.response.send_message(
                f"Welcome Channel has been set to {discord.utils.get(interaction.guild.channels, id=channel.id).mention}.",
                ephemeral=True)
        except Error as e:
            print(e)
            await interaction.response.send_message(content=f"""Something went wrong.""", ephemeral=True)

    @app_commands.checks.has_permissions(manage_channels=True)
    @app_commands.command(name="goodbye-channel", description="Command to set your server's goodbye channel.")
    async def goodbyechannel(self, interaction: discord.Interaction, channel: discord.TextChannel):
        try:
            await insert(self.bot.database,
                         f"""REPLACE INTO server_{str(interaction.guild.id)} (configname, configoption) VALUES( 'goodbye_channel', {channel.id})""")
            await interaction.response.send_message(
                f"Goodbye Channel has been set to {discord.utils.get(interaction.guild.channels, id=channel.id)}.",
                ephemeral=True)
        except Exception as e:
            print(e)
            await interaction.response.send_message(content=f"""Something went wrong.""", ephemeral=True)

    @app_commands.checks.has_permissions(manage_channels=True)
    @app_commands.command(name="ticket-category", description="Command to set your server's ticket category.")
    async def ticketcategory(self, interaction: discord.Interaction, category: discord.CategoryChannel):
        try:
            await insert(self.bot.database,
                         f"""REPLACE INTO server_{str(interaction.guild.id)} (configname, configoption) VALUES( 'ticket_category', {category.id})""")
            await interaction.response.send_message(
                f"Ticket Category has been set to {discord.utils.get(interaction.guild.categories, id=category.id)}.",
                ephemeral=True)
        except Exception as e:
            print(e)
            await interaction.response.send_message(content=f"""Something went wrong.""", ephemeral=True)

    @app_commands.checks.has_permissions(manage_channels=True)
    @app_commands.command(name="transcript-log-channel",
                          description="Command to set your server's transcript log channel.")
    async def transcriptlogchannel(self, interaction: discord.Interaction, channel: discord.TextChannel):
        try:
            await insert(self.bot.database,
                         f"""REPLACE INTO server_{str(interaction.guild.id)} (configname, configoption) VALUES( 'transcript_channel', {channel.id})""")
            await interaction.response.send_message(
                f"Transcript Log Channel has been set to {discord.utils.get(interaction.guild.channels, id=channel.id)}.",
                ephemeral=True)
        except Exception as e:
            print(e)
            await interaction.response.send_message(content=f"""Something went wrong.""", ephemeral=True)

    @app_commands.checks.has_permissions(manage_roles=True)
    @app_commands.command(name="default-role", description="Command for setting your server's Default role.")
    async def defaultrole(self, interaction: discord.Interaction, role: discord.Role):
        try:
            await insert(self.bot.database,
                         f"""REPLACE INTO server_{str(interaction.guild.id)} (configname, configoption) VALUES( 'default_role', {role.id})""")
            await interaction.response.send_message(
                content=f"""Default Role has been set to {role.name}""", ephemeral=True)
        except Exception as e:
            print(e)
            await interaction.response.send_message(content=f"""Something went wrong.""", ephemeral=True)

    @app_commands.checks.has_permissions(manage_roles=True)
    @app_commands.command(name="supporter-role", description="Command for setting your server's supporter role.")
    async def supporterrole(self, interaction: discord.Interaction, role: discord.Role):
        try:
            await insert(self.bot.database,
                         f"""REPLACE INTO server_{str(interaction.guild.id)} (configname, configoption) VALUES( 'supporter_role', {role.id})""")
            await interaction.response.send_message(
                content=f"""Supporter Role has been set to {role.name}""", ephemeral=True)
        except Exception as e:
            print(e)
            await interaction.response.send_message(content=f"""Something went wrong.""", ephemeral=True)

    @welcomechannel.error
    @transcriptlogchannel.error
    @defaultrole.error
    @ticketcategory.error
    async def onerror(self, interaction: discord.Interaction, error: app_commands.MissingPermissions):
        await interaction.response.send_message(content=error,
                                                ephemeral=True)


class resetcmd(commands.GroupCog, name="reset"):

    def __init__(self, bot):
        self.bot = bot

    @app_commands.checks.has_permissions(manage_channels=True)
    @app_commands.command(name="welcome-channel", description="Command to reset your server's welcome channel.")
    async def welcomechannel(self, interaction: discord.Interaction):
        try:
            await insert(self.bot.database,
                         f"""REPLACE INTO server_{str(interaction.guild.id)} (configname, configoption) VALUES( 'welcome_channel', 0)""")
            await interaction.response.send_message(
                f"Welcome Channel has been reset.",
                ephemeral=True)
        except Exception as e:
            print(e)
            await interaction.response.send_message(content=f"""Something went wrong.""", ephemeral=True)

    @app_commands.checks.has_permissions(manage_channels=True)
    @app_commands.command(name="goodbye-channel", description="Command to reset your server's goodbye channel.")
    async def goodbyechannel(self, interaction: discord.Interaction):
        try:
            await insert(self.bot.database,
                         f"""REPLACE INTO server_{str(interaction.guild.id)} (configname, configoption) VALUES( 'goodbye_channel', 0)""")
            await interaction.response.send_message(
                f"Goodbye Channel has been reset.",
                ephemeral=True)
        except Exception as e:
            print(e)
            await interaction.response.send_message(content=f"""Something went wrong.""", ephemeral=True)

    @app_commands.checks.has_permissions(manage_channels=True)
    @app_commands.command(name="ticket-category", description="Command to reset your server's ticket category.")
    async def ticketcategory(self, interaction: discord.Interaction):
        try:
            await insert(self.bot.database,
                         f"""REPLACE INTO server_{str(interaction.guild.id)} (configname, configoption) VALUES( 'ticket_category', 0)""")
            await interaction.response.send_message(
                f"Ticket Category has been reset.",
                ephemeral=True)
        except Exception as e:
            print(e)
            await interaction.response.send_message(content=f"""Something went wrong.""", ephemeral=True)

    @app_commands.checks.has_permissions(manage_channels=True)
    @app_commands.command(name="transcript-log-channel",
                          description="Command to reset your server's transcript log channel.")
    async def transcriptlogchannel(self, interaction: discord.Interaction):
        try:
            await insert(self.bot.database,
                         f"""REPLACE INTO server_{str(interaction.guild.id)} (configname, configoption) VALUES( 'transcript_channel', 0)""")
            await interaction.response.send_message(
                f"Transcript log channel has been reset.",
                ephemeral=True)
        except Exception as e:
            print(e)
            await interaction.response.send_message(content=f"""Something went wrong.""", ephemeral=True)

    @app_commands.checks.has_permissions(manage_roles=True)
    @app_commands.command(name="default-role", description="Command to reset your server's Default role.")
    async def defaultrole(self, interaction: discord.Interaction):
        try:
            await insert(self.bot.database,
                         f"""REPLACE INTO server_{str(interaction.guild.id)} (configname, configoption) VALUES( 'default_role', 0)""")
            await interaction.response.send_message(
                content=f"""Default Role has been reset.""", ephemeral=True)
        except Exception as e:
            print(e)
            await interaction.response.send_message(content=f"""Something went wrong.""", ephemeral=True)

    @app_commands.checks.has_permissions(manage_roles=True)
    @app_commands.command(name="supporter-role", description="Command to reset your server's supporter role.")
    async def supporterrole(self, interaction: discord.Interaction):
        try:
            await insert(self.bot.database,
                         f"""REPLACE INTO server_{str(interaction.guild.id)} (configname, configoption) VALUES( 'supporter_role', 0)""")
            await interaction.response.send_message(
                content=f"""Support Role has been reset.""", ephemeral=True)
        except Exception as e:
            print(e)
            await interaction.response.send_message(content=f"""Something went wrong.""", ephemeral=True)

    @welcomechannel.error
    @transcriptlogchannel.error
    @defaultrole.error
    @ticketcategory.error
    async def onerror(self, interaction: discord.Interaction, error: app_commands.MissingPermissions):
        await interaction.response.send_message(content=error,
                                                ephemeral=True)


async def setup(bot):
    await bot.add_cog(setcmd(bot))
    await bot.add_cog(resetcmd(bot))
