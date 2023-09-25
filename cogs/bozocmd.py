import discord
from discord.ext import commands


class messagefunctions(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:  # If message is from itself, do nothing
            return
        if message.author.bot:  # If message is a bot, do nothing
            return
        if message.content.isupper():
            await message.reply(f"Watch the caps bozo.")


async def setup(bot):
    await bot.add_cog(messagefunctions(bot))
