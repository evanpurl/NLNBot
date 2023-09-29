from discord.ext import commands

from util.databasefunctions import create_pool, createserver, deleteserver


class guildfunctions(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        pool = await create_pool()

        await createserver(pool,
                           f"""INSERT IGNORE INTO {self.bot.user.name.replace(" ", "_")} (serverid, servername) VALUES ({guild.id}, {guild.name});""")

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        pool = await create_pool()
        await deleteserver(pool, f"""DELETE IGNORE FROM {self.bot.user.name.replace(" ", "_")} WHERE serverid = ({guild.id});""")


async def setup(bot):
    await bot.add_cog(guildfunctions(bot))
