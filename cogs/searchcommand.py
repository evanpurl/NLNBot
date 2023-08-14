import datetime

import discord
from discord import app_commands, ui

from discord.ext import commands
from util.sqlitefunctions import create_db, gettickets


def searchembed(user, tickets):
    embed = discord.Embed(title=f"{user.name}", description=f"Found {len(tickets)} ticket(s)", color=discord.Color.blue(),
                          timestamp=datetime.datetime.now())
    embed.set_author(name=user.name, icon_url=user.avatar)
    if len(tickets) == 0:
        pass
    else:
        for val in tickets:
            embed.add_field(name=val[0], value=val[2], inline=True)
    return embed


class searchcmd(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @app_commands.checks.has_permissions(manage_messages=True)
    @app_commands.command(name="search-tickets", description="Command used to search for a user's tickets.")
    async def search(self, interaction: discord.Interaction, user: discord.Member):
        try:
            conn = await create_db(f"storage/global/tickets.db")
            tickets = await gettickets(conn=conn, userid=user.id)
            await interaction.response.send_message(embed=searchembed(user, tickets), ephemeral=True)
        except Exception as e:
            print(e)


async def setup(bot):
    await bot.add_cog(searchcmd(bot))
