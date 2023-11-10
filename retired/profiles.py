import datetime
from sqlite3 import Error

import discord
from discord import app_commands, ui
from discord.ext import commands

from retired.sqlitefunctions import create_db, create_table, createuniqueindex, getprofileconfig


async def getprofile(server, userid):
    conn = await create_db(f"storage/{server}/profiles.db")
    profile = await getprofileconfig(conn, userid)
    if profile is None:
        profile = [userid, "Not edited", "Not edited", "Not edited"]
    return profile


async def insertprofile(server, info):
    conn = await create_db(f"storage/{server}/profiles.db")

    await insertprofileinfo(conn, info)


async def insertprofileinfo(conn, configlist):
    # config list should be a length of 4.
    try:
        datatoinsert = f""" REPLACE INTO profiles(userid, pronouns, dm, bio) VALUES( ?, ?, ?, ?) """
        c = conn.cursor()
        c.execute(datatoinsert, (str(configlist[0]), str(configlist[1]), str(configlist[2]), str(configlist[3])))
        conn.commit()
        c.close()
        conn.close()

    except Error or Exception as e:
        print(f"insert config: {e}")


async def initprofiles(server):
    tabledata = """CREATE TABLE IF NOT EXISTS profiles ( userid text NOT NULL, pronouns text, dm text, bio text);"""
    conn = await create_db(f"storage/{server}/profiles.db")
    await create_table(conn, tabledata)
    await createuniqueindex(conn, f""" CREATE UNIQUE INDEX IF NOT EXISTS idx_userid ON profiles (userid) """)
    print("Profiles Initialized")


async def assembleprofileembed(bot, server, user):

    profile = await getprofile(server.id, user.id)

    embed = discord.Embed(title=f"{user.name}'s Profile", color=discord.Color.blue(),
                          timestamp=datetime.datetime.now())
    embed.set_thumbnail(url=server.icon.url)
    embed.set_author(name=bot.user.name, icon_url=bot.user.avatar)
    embed.add_field(name="Pronouns", value=profile[1], inline=True)
    embed.add_field(name="Dm Preferences", value=profile[2], inline=True)
    embed.add_field(name="Bio", value=profile[3], inline=True)
    return embed


class profilemodal(ui.Modal, title='Update Profile Information'):

    def __init__(self, bot):
        super().__init__()
        self.bot = bot

    pronouns = ui.TextInput(label='Pronouns:', style=discord.TextStyle.short, required=False,
                            placeholder="Leave blank to keep the same")
    dmpref = ui.TextInput(label='DM Preferences:', style=discord.TextStyle.short, required=False,
                          placeholder="Leave blank to keep the same")
    bio = ui.TextInput(label='Bio:', style=discord.TextStyle.paragraph, required=False,
                       placeholder="Leave blank to keep the same")

    async def on_submit(self, interaction: discord.Interaction):

        try:
            profile = await getprofile(interaction.guild.id, interaction.user.id)
            if self.pronouns.value == "":
                self.pronouns = profile[1]
            if self.dmpref.value == "":
                self.dmpref = profile[2]
            if self.bio.value == "":
                self.bio = profile[3]
            await insertprofile(interaction.guild.id, [interaction.user.id, self.pronouns, self.dmpref, self.bio])

            await interaction.response.send_message(content=f"Profile updated!",
                                                    ephemeral=True)
        except Exception as e:
            print(e)


class profilecmd(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="edit-profile", description="Command used to edit your profile")
    async def editprofile(self, interaction: discord.Interaction):
        try:
            await interaction.response.send_modal(profilemodal(self.bot))

        except Exception as e:
            print(e)

    @app_commands.command(name="profile", description="Command used to view a user's profile")
    async def profile(self, interaction: discord.Interaction, user: discord.Member):
        try:
            await interaction.response.send_message(embed=await assembleprofileembed(self.bot, interaction.guild, user), ephemeral=True)
        except Exception as e:
            print(e)

    @editprofile.error
    @profile.error
    async def onerror(self, interaction: discord.Interaction, error: app_commands.MissingPermissions):
        await interaction.response.send_message(content=error,
                                                ephemeral=True)


async def setup(bot):
    await bot.add_cog(profilecmd(bot))
