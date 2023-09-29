import discord
from discord import app_commands
from discord.ext import commands
from aiomysql import Error

from util.databasefunctions import create_pool, insert


class setcmd(commands.GroupCog, name="set"):

    def __init__(self, bot):
        self.bot = bot

    @app_commands.checks.has_permissions(manage_channels=True)
    @app_commands.command(name="welcome-channel", description="Command to set your server's welcome channel.")
    async def welcomechannel(self, interaction: discord.Interaction, channel: discord.TextChannel):
        try:
            mysql = f"""UPDATE {self.bot.user.name.replace(" ", "_")} SET welcomechannelid = {channel.id}  WHERE serverid = {interaction.guild.id};"""
            pool = await create_pool()
            await insert(pool, mysql)
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
            mysql = f"""UPDATE {self.bot.user.name.replace(" ", "_")} SET goodbyechannelid = {channel.id}  WHERE serverid = {interaction.guild.id};"""
            pool = await create_pool()
            await insert(pool, mysql)
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
            mysql = f"""UPDATE {self.bot.user.name.replace(" ", "_")} SET ticketcategoryid = {category.id}  WHERE serverid = {interaction.guild.id};"""
            pool = await create_pool()
            await insert(pool, mysql)
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
            mysql = f"""UPDATE {self.bot.user.name.replace(" ", "_")} SET transcriptchannelid = {channel.id}  WHERE serverid = {interaction.guild.id};"""
            pool = await create_pool()
            await insert(pool, mysql)
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
            mysql = f"""UPDATE {self.bot.user.name.replace(" ", "_")} SET defaultroleid = {role.id}  WHERE serverid = {interaction.guild.id};"""
            pool = await create_pool()
            await insert(pool, mysql)
            await interaction.response.send_message(
                content=f"""Default Role has been set to {role.name}""", ephemeral=True)
        except Exception as e:
            print(e)
            await interaction.response.send_message(content=f"""Something went wrong.""", ephemeral=True)

    @app_commands.checks.has_permissions(manage_channels=True)
    @app_commands.command(name="transaction-category", description="Command to set your server's transaction category.")
    async def transactioncategory(self, interaction: discord.Interaction, category: discord.CategoryChannel):
        try:
            mysql = f"""UPDATE {self.bot.user.name.replace(" ", "_")} SET transactioncategoryid = {category.id}  WHERE serverid = {interaction.guild.id};"""
            pool = await create_pool()
            await insert(pool, mysql)
            await interaction.response.send_message(
                f"Transaction Category has been set to {discord.utils.get(interaction.guild.categories, id=category.id)}.",
                ephemeral=True)
        except Exception as e:
            print(e)
            await interaction.response.send_message(content=f"""Something went wrong.""", ephemeral=True)

    @app_commands.checks.has_permissions(manage_roles=True)
    @app_commands.command(name="supporter-role", description="Command for setting your server's supporter role.")
    async def supporterrole(self, interaction: discord.Interaction, role: discord.Role):
        try:
            mysql = f"""UPDATE {self.bot.user.name.replace(" ", "_")} SET supporterroleid = {role.id}  WHERE serverid = {interaction.guild.id};"""
            pool = await create_pool()
            await insert(pool, mysql)
            await interaction.response.send_message(
                content=f"""Supporter Role has been set to {role.name}""", ephemeral=True)
        except Exception as e:
            print(e)
            await interaction.response.send_message(content=f"""Something went wrong.""", ephemeral=True)

    @welcomechannel.error
    @transcriptlogchannel.error
    @defaultrole.error
    @ticketcategory.error
    @transactioncategory.error
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
            mysql = f"""UPDATE {self.bot.user.name.replace(" ", "_")} SET welcomechannelid = 0  WHERE serverid = {interaction.guild.id};"""
            pool = await create_pool()
            await insert(pool, mysql)
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
            mysql = f"""UPDATE {self.bot.user.name.replace(" ", "_")} SET goodbyechannelid = 0  WHERE serverid = {interaction.guild.id};"""
            pool = await create_pool()
            await insert(pool, mysql)
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
            mysql = f"""UPDATE {self.bot.user.name.replace(" ", "_")} SET ticketcategoryid = 0  WHERE serverid = {interaction.guild.id};"""
            pool = await create_pool()
            await insert(pool, mysql)
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
            mysql = f"""UPDATE {self.bot.user.name.replace(" ", "_")} SET transcriptnchannelid = 0  WHERE serverid = {interaction.guild.id};"""
            pool = await create_pool()
            await insert(pool, mysql)
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
            mysql = f"""UPDATE {self.bot.user.name.replace(" ", "_")} SET defatulroleid = 0  WHERE serverid = {interaction.guild.id};"""
            pool = await create_pool()
            await insert(pool, mysql)
            await interaction.response.send_message(
                content=f"""Default Role has been reset.""", ephemeral=True)
        except Exception as e:
            print(e)
            await interaction.response.send_message(content=f"""Something went wrong.""", ephemeral=True)

    @app_commands.checks.has_permissions(manage_channels=True)
    @app_commands.command(name="transaction-category", description="Command to reset your server's transaction "
                                                                   "category.")
    async def transactioncategory(self, interaction: discord.Interaction):
        try:
            mysql = f"""UPDATE {self.bot.user.name.replace(" ", "_")} SET transactioncategoryid = 0  WHERE serverid = {interaction.guild.id};"""
            pool = await create_pool()
            await insert(pool, mysql)
            await interaction.response.send_message(
                f"Transaction Category has been reset.",
                ephemeral=True)
        except Exception as e:
            print(e)
            await interaction.response.send_message(content=f"""Something went wrong.""", ephemeral=True)

    @app_commands.checks.has_permissions(manage_roles=True)
    @app_commands.command(name="supporter-role", description="Command to reset your server's supporter role.")
    async def supporterrole(self, interaction: discord.Interaction):
        try:
            mysql = f"""UPDATE {self.bot.user.name.replace(" ", "_")} SET supporterroleid = 0  WHERE serverid = {interaction.guild.id};"""
            pool = await create_pool()
            await insert(pool, mysql)
            await interaction.response.send_message(
                content=f"""Support Role has been reset.""", ephemeral=True)
        except Exception as e:
            print(e)
            await interaction.response.send_message(content=f"""Something went wrong.""", ephemeral=True)

    @welcomechannel.error
    @transcriptlogchannel.error
    @defaultrole.error
    @ticketcategory.error
    @transactioncategory.error
    async def onerror(self, interaction: discord.Interaction, error: app_commands.MissingPermissions):
        await interaction.response.send_message(content=error,
                                                ephemeral=True)


async def setup(bot):
    await bot.add_cog(setcmd(bot))
    await bot.add_cog(resetcmd(bot))
