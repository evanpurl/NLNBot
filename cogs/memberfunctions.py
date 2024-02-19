import datetime

import discord
from discord.ext import commands

from util.databasefunctions import get


def userembed(user, server):
    embed = discord.Embed(title="**Welcome!**",
                          description=f"Welcome to {server.name} {user.mention}! Please make sure "
                                      f"to review the rules! This server has {len([m for m in server.members if not m.bot])} members!",
                          color=discord.Color.blue(),
                          timestamp=datetime.datetime.now())
    embed.set_author(name=user.name, icon_url=user.avatar)
    return embed


def userembedbye(user):
    embed = discord.Embed(title="**Goodbye**", description=f"Goodbye {user.name}.", color=discord.Color.dark_red(),
                          timestamp=datetime.datetime.now())
    embed.set_author(name=user.name, icon_url=user.avatar)
    return embed


class memberfunctions(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        try:
            welcome_channel = await get(self.bot.database,
                                        f"""SELECT configoption FROM server_{str(member.guild.id)} WHERE configname='welcome_channel'""")
            default_role = await get(self.bot.database,
                                     f"""SELECT configoption FROM server_{str(member.guild.id)} WHERE configname='default_role'""")
            channel = discord.utils.get(member.guild.channels, id=welcome_channel)
            if channel:
                await channel.send(embed=userembed(member, member.guild))
            role = discord.utils.get(member.guild.roles, id=default_role)
            if role:
                await member.add_roles(role)
        except Exception as e:
            print(e)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        goodbye_channel = await get(self.bot.database,
                                    f"""SELECT configoption FROM server_{str(member.guild.id)} WHERE configname='goodbye_channel'""")
        channel = discord.utils.get(member.guild.channels, id=goodbye_channel)
        if channel:
            await channel.send(embed=userembedbye(member))


async def setup(bot):
    await bot.add_cog(memberfunctions(bot))
