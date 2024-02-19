from discord.ext import commands
from util.load_data import loadallservers


class onready(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.wait_until_ready()
        await loadallservers(self.bot)
        print(f"Confirming server data.")
        print(f'We have logged in as {self.bot.user}')


async def setup(bot):
    await bot.add_cog(onready(bot))
