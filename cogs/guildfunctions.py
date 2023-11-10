from discord.ext import commands
from aiomysql import Error
from util.databasefunctions import create_pool, drop_server, create_table, create_unique_index


class guildfunctions(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        pool = await create_pool()

        await create_table(pool,
                           f"""CREATE TABLE IF NOT EXISTS server_%s ( configname text, configoption text );""",
                           str(guild.id))
        await create_unique_index(pool,
                                  f""" CREATE UNIQUE INDEX IF NOT EXISTS idx_configname ON server_%s (configname); """,
                                  str(guild.id))

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        try:
            pool = await create_pool()
            await drop_server(pool, f"""DROP TABLE server_{str(guild.id)};""")
        except Exception or Error as e:
            print(f"Drop Server: {e}")


async def setup(bot):
    await bot.add_cog(guildfunctions(bot))
