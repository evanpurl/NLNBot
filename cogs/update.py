import datetime

import discord
from discord import app_commands, ui
from discord.ext import commands


async def assembleembed(bot, server, choice, added, removed, updated):
    embed = discord.Embed(title=f"{server.name} | New Updates",
                          description=f"Here are the current updates for **{choice}**", color=discord.Color.blue(),
                          timestamp=datetime.datetime.now(), )
    embed.set_thumbnail(url=server.icon.url)
    embed.set_author(name=bot.user.name, icon_url=bot.user.avatar)
    embed.add_field(name="Added", value=added, inline=False)
    embed.add_field(name="Removed", value=removed, inline=False)
    embed.add_field(name="Updated", value=updated, inline=False)
    return embed


class Updatemodal(ui.Modal, title='Update Information'):

    def __init__(self, bot, channel, topic):
        super().__init__()
        self.bot = bot
        self.channel = channel
        self.topic = topic

    added = ui.TextInput(label='Added:', style=discord.TextStyle.long,
                         placeholder="N/A", required=False)
    removed = ui.TextInput(label='Removed:', style=discord.TextStyle.long,
                           placeholder="N/A", required=False)
    updated = ui.TextInput(label='Updated:', style=discord.TextStyle.long,
                           placeholder="N/A", required=False)

    async def on_submit(self, interaction: discord.Interaction):

        await self.channel.send(
            embed=await assembleembed(self.bot, interaction.guild, self.topic, self.added, self.removed, self.updated))

        await interaction.response.send_message(content=f"Update Sent!",
                                                ephemeral=True)


class updatecmd(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.has_permissions(manage_channels=True)
    @app_commands.command(name="update", description="Command used to create an update Embed.")
    @app_commands.choices(topic=[
        app_commands.Choice(name='General', value=1),
        app_commands.Choice(name='Discord', value=2),
        app_commands.Choice(name='Tycoon', value=3),
        app_commands.Choice(name='LifeSteal', value=4),
        app_commands.Choice(name='Applications', value=5),
        app_commands.Choice(name='Other', value=6),
    ])
    async def update(self, interaction: discord.Interaction, topic: app_commands.Choice[int], channel: discord.TextChannel):
        try:

            await interaction.response.send_modal(Updatemodal(self.bot, channel, topic.name))

        except Exception as e:
            print(e)


async def setup(bot):
    await bot.add_cog(updatecmd(bot))
