from util.databasefunctions import create_table, create_unique_index
from aiomysql import Error


async def loadallservers(bot):
    try:
        for a in bot.guilds:
            await create_table(bot.database,
                               f"""CREATE TABLE IF NOT EXISTS server_%s ( configname text, configoption text );""",
                               a.id)
            await create_unique_index(bot.database,
                                      f""" CREATE UNIQUE INDEX IF NOT EXISTS idx_configname ON server_%s (configname); """,
                                      a.id)

        print("Data confirmed")

        return

    except Exception or Error as e:
        print(f"load data: {e}")

    except Error or Exception as e:
        print(f"load data function, ({e})")
