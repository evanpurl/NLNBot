import argparse
import asyncio
import os
import subprocess
import sys

import discord
from util.load_extensions import load_extensions  # Our code
from discord.ext import commands
from dotenv import load_dotenv

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

client = commands.Bot(command_prefix="$", intents=intents)

load_dotenv()

parser = argparse.ArgumentParser(description='Nite Life Network Bot')


async def install_requirements():
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--upgrade', 'pip'])
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])


# Main function to load extensions and then load bot.
async def main():
    await install_requirements()
    async with client:
        try:
            token = os.getenv('token')

            await load_extensions(client)
            print("Bot Ready!")
            await client.start(token)
        except KeyboardInterrupt:
            pass


asyncio.run(main())  # Runs main function above
