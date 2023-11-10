import asyncio
import datetime
import io
import chat_exporter
import discord
from discord import app_commands
from discord.ext import commands

from util.databasefunctions import create_pool, get

timeout = 300  # seconds


# Needs "manage role" perms
# ticket-username

async def ticketembed(bot):
    embed = discord.Embed(description=f"When you are finished, click the close ticket button below. This ticket will "
                                      f"close in 5 minutes if no message is sent.", color=discord.Color.blue(),
                          timestamp=datetime.datetime.now())
    embed.set_author(name=bot.user.name, icon_url=bot.user.avatar)
    return embed


async def tickettypeembed(bot):
    embed = discord.Embed(description=f"Choose your ticket category!", color=discord.Color.blue(),
                          timestamp=datetime.datetime.now())
    embed.set_author(name=bot.user.name, icon_url=bot.user.avatar)
    return embed


class tickettypes(discord.ui.View):

    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Report a player", style=discord.ButtonStyle.red,
                       custom_id="ticket:playerreport")
    async def report_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            await interaction.message.edit(view=None)
            await interaction.response.send_message(content="Hello! To report a player, send any sort of evidence you "
                                                            "have against the player here.")
        except Exception as e:
            print(e)

    @discord.ui.button(label="Server Issue", style=discord.ButtonStyle.blurple,
                       custom_id="ticket:serverissue")
    async def server_issue(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            await interaction.message.edit(view=None)
            await interaction.response.send_message(content="Hello! To report a server issue, list the server you are "
                                                            "having an issue with, as well as the issue. Feel free to "
                                                            "send any pictures or videos to better show us what "
                                                            "happened.")
        except Exception as e:
            print(e)

    @discord.ui.button(label="Other", style=discord.ButtonStyle.blurple,
                       custom_id="ticket:other")
    async def other(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            await interaction.message.edit(view=None)
            await interaction.response.send_message(content="Hello! This category is for anything not related to "
                                                            "existing categories.")
        except Exception as e:
            print(e)


class ticketbuttonpanel(discord.ui.View):

    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Close Ticket", emoji="🗑️", style=discord.ButtonStyle.red,
                       custom_id="ticket:close")
    async def close_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            pool = await create_pool()
            data = await get(pool,
                             f"""SELECT configoption FROM server_{str(interaction.guild.id)} WHERE configname='transcript_channel'""")
            logchannel = discord.utils.get(interaction.guild.channels,
                                           id=int(data))
            if logchannel:
                transcript = await chat_exporter.export(
                    interaction.channel,
                )
                if transcript is None:
                    return

                transcript_file = discord.File(
                    io.BytesIO(transcript.encode()),
                    filename=f"transcript-{interaction.channel.name}.html",
                )

                message = await logchannel.send(file=transcript_file)
                await interaction.channel.delete()
                return
            else:
                await interaction.channel.delete()
        except Exception as e:
            print(e)

    @commands.has_permissions(manage_channels=True)
    @discord.ui.button(label="Auto-Close Ticket", emoji="⏲️", style=discord.ButtonStyle.gray,
                       custom_id="ticket:autoclose")
    async def auto_close_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            if interaction.user.guild_permissions.manage_channels:
                await interaction.response.send_message(content="Timer started.", ephemeral=True)

                def check(m: discord.Message):  # m = discord.Message.
                    return m.author.id == interaction.user.id and m.channel.id == interaction.channel.id

                try:
                    while True:
                        msg = await interaction.client.wait_for('message', check=check, timeout=timeout)
                except asyncio.TimeoutError:
                    pool = await create_pool()
                    data = await get(pool,
                                     f"""SELECT configoption FROM server_{str(interaction.guild.id)} WHERE configname='transcript_channel'""")
                    logchannel = discord.utils.get(interaction.guild.channels,
                                                   id=int(data))
                    if logchannel:
                        transcript = await chat_exporter.export(
                            interaction.channel,
                        )
                        if transcript is None:
                            return

                        transcript_file = discord.File(
                            io.BytesIO(transcript.encode()),
                            filename=f"transcript-{interaction.channel.name}.html",
                        )

                        message = await logchannel.send(file=transcript_file)
                        await interaction.channel.delete()
                        return
                    else:
                        await interaction.channel.delete()
            else:
                await interaction.response.send_message(content="You don't have permission to do that.", ephemeral=True)
        except Exception as e:
            print(e)


class ticketbutton(discord.ui.View):

    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Create Ticket", emoji="📨", style=discord.ButtonStyle.blurple,
                       custom_id="ticketbutton")
    async def gray_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            existticket = discord.utils.get(interaction.guild.channels,
                                            name=f"ticket-{interaction.user.name.lower()}")
            if existticket:
                await interaction.response.send_message(
                    content=f"You already have an existing ticket you silly goose. {existticket.mention}",
                    ephemeral=True)
            else:
                overwrites = {
                    interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False),
                    interaction.user: discord.PermissionOverwrite(read_messages=True),
                    interaction.guild.me: discord.PermissionOverwrite(read_messages=True)}
                pool = await create_pool()
                data = await get(pool,
                                 f"""SELECT configoption FROM server_{str(interaction.guild.id)} WHERE configname='ticket_category'""")
                ticketcat = discord.utils.get(interaction.guild.categories, id=int(data))
                if ticketcat:
                    ticketchan = await interaction.guild.create_text_channel(
                        f"ticket-{interaction.user.name}", category=ticketcat,
                        overwrites=overwrites)
                    await interaction.response.send_message(content=f"Ticket created in {ticketchan.mention}!",
                                                            ephemeral=True)
                    await ticketchan.send(
                        content=f"{interaction.user.mention} created a ticket!")
                    await ticketchan.send(
                        embed=await ticketembed(interaction.client),
                        view=ticketbuttonpanel())
                    await ticketchan.send(
                        embed=await tickettypeembed(interaction.client),
                        view=tickettypes())

                    def check(m: discord.Message):  # m = discord.Message.
                        return m.author.id == interaction.user.id and m.channel.id == ticketchan.id

                    try:
                        msg = await interaction.client.wait_for('message', check=check, timeout=timeout)
                    except asyncio.TimeoutError:
                        pool = await create_pool()
                        data = await get(pool,
                                         f"""SELECT configoption FROM server_{str(interaction.guild.id)} WHERE configname='transcript_channel'""")
                        logchannel = discord.utils.get(interaction.guild.channels,
                                                       id=int(data))
                        if logchannel:
                            transcript = await chat_exporter.export(
                                ticketchan,
                            )
                            if transcript is None:
                                return

                            transcript_file = discord.File(
                                io.BytesIO(transcript.encode()),
                                filename=f"transcript-{ticketchan.name}.html",
                            )

                            await logchannel.send(file=transcript_file)

                        await ticketchan.delete()

                else:
                    ticketchan = await interaction.guild.create_text_channel(
                        f"ticket-{interaction.user.name}", overwrites=overwrites)
                    await interaction.response.send_message(content=f"Ticket created in {ticketchan.mention}!",
                                                            ephemeral=True)
                    await ticketchan.send(
                        content=f"{interaction.user.mention} created a ticket!")
                    await ticketchan.send(
                        embed=await ticketembed(interaction.client),
                        view=ticketbuttonpanel())
                    await ticketchan.send(
                        embed=await tickettypeembed(interaction.client),
                        view=tickettypes())

                    def check(m: discord.Message):  # m = discord.Message.
                        return m.author.id == interaction.user.id and m.channel.id == ticketchan.id

                    try:
                        msg = await interaction.client.wait_for('message', check=check, timeout=timeout)
                    except asyncio.TimeoutError:
                        pool = await create_pool()
                        data = await get(pool,
                                         f"""SELECT configoption FROM server_{str(interaction.guild.id)} WHERE configname='transcript_channel'""")
                        logchannel = discord.utils.get(interaction.guild.channels,
                                                       id=int(data))
                        if logchannel:
                            transcript = await chat_exporter.export(
                                ticketchan,
                            )
                            if transcript is None:
                                return

                            transcript_file = discord.File(
                                io.BytesIO(transcript.encode()),
                                filename=f"transcript-{ticketchan.name}.html",
                            )

                            await logchannel.send(file=transcript_file)
                        await ticketchan.delete()
        except Exception as e:
            print(e)


def ticketmessageembed(bot):
    embed = discord.Embed(title="**Tickets**",
                          description=f"Have an issue? Make a ticket!",
                          color=discord.Color.blue(),
                          timestamp=datetime.datetime.now())
    embed.set_author(name=bot.user.name, icon_url=bot.user.avatar)
    return embed


class ticketcmd(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.has_permissions(manage_roles=True)
    @app_commands.command(name="ticket", description="Command used by admin to create the ticket message.")
    async def ticket(self, interaction: discord.Interaction) -> None:
        try:
            await interaction.response.send_message(embed=ticketmessageembed(self.bot), view=ticketbutton())
        except Exception as e:
            print(e)

    @ticket.error
    async def onerror(self, interaction: discord.Interaction, error: app_commands.MissingPermissions):
        await interaction.response.send_message(content=error,
                                                ephemeral=True)


async def setup(bot):
    await bot.add_cog(ticketcmd(bot))
    bot.add_view(ticketbutton())  # lines that init persistent view
    bot.add_view(ticketbuttonpanel())
    bot.add_view(tickettypes())
