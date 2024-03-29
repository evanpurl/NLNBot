import os
import asyncio
import discord
from util.load_extensions import load_extensions  # Our code
from discord.ext import commands
from dotenv import load_dotenv
from util.databasefunctions import create_pool

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

client = commands.Bot(command_prefix="$", intents=intents)

load_dotenv()


# Main function to load extensions and then load bot.
async def main():
    async with client:
        try:
            token = os.getenv('token')
            client.database = await create_pool()
            print("Connected to Bot Database!")
            await load_extensions(client)
            print("Bot Ready!")
            await client.start(token)
        except KeyboardInterrupt:
            pass


asyncio.run(main())  # Runs main function above
