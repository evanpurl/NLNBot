from util.databasefunctions import create_pool, getall, createservermultiple
from aiomysql import Error


async def loadallservers(bot, serverlist):
    servers = []
    for a in serverlist:
        servers.append(a.id)
    await loaddata(bot, servers)


async def loaddata(bot, guildlist):
    """
    Function that loads sqlite data.
    :param guildlist:
    :param bot:
    :return:
    """
    try:
        pool = await create_pool()

        data = await getall(pool, f"""SELECT serverid FROM {bot.user.name.replace(" ", "_")};""")

        missing = set(guildlist).difference(data)

        if len(missing) > 0:
            pool = await create_pool()
            for a in missing:
                guild = await bot.fetch_guild(a)
                print(f"Creating data for {guild.name}")
                await createservermultiple(pool, f"""INSERT IGNORE INTO {bot.user.name.replace(" ", "_")} (serverid, servername) VALUES ({guild.id}, "{guild.name}");""")
                print(f"Data confirmed for guild {guild.name}")
            pool.close()

        print("Data confirmed")

    except Error as e:
        print(f"load data function, ({e})")
