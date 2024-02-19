from discord.ext import commands
from aiomysql import Error
from util.databasefunctions import drop_server, create_table, create_unique_index


class guildfunctions(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_join(self, guild):

        await create_table(self.bot.database,
                           f"""CREATE TABLE IF NOT EXISTS server_%s ( configname text, configoption text );""",
                           guild.id)
        await create_unique_index(self.bot.database,
                                  f""" CREATE UNIQUE INDEX IF NOT EXISTS idx_configname ON server_%s (configname); """,
                                  guild.id)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        try:
            await drop_server(self.bot.database, f"""DROP TABLE server_{str(guild.id)};""")
        except Exception or Error as e:
            print(f"Drop Server: {e}")


async def setup(bot):
    await bot.add_cog(guildfunctions(bot))
