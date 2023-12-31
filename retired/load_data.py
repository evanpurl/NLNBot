from util.databasefunctions import create_pool, create_table, create_unique_index
from aiomysql import Error


async def loadallservers(bot):
    try:
        pool = await create_pool()
        for a in bot.guilds:
            await create_table(pool,
                               f"""CREATE TABLE IF NOT EXISTS server_%s ( configname text, configoption text );""",
                               a.id)
            await create_unique_index(pool,
                                      f""" CREATE UNIQUE INDEX IF NOT EXISTS idx_configname ON server_%s (configname); """,
                                      a.id)

        #  SE Data
        se = 955962668756385792
        await create_table(pool, f"""CREATE TABLE IF NOT EXISTS SE_%s ( userid bigint NOT NULL, roleid bigint );""",
                           se)
        await create_unique_index(pool, f""" CREATE UNIQUE INDEX IF NOT EXISTS idx_userid ON SE_%s (userid);""", se)
        #

        print("Data confirmed")

        return

    except Exception or Error as e:
        print(f"load data: {e}")

    except Error or Exception as e:
        print(f"load data function, ({e})")
