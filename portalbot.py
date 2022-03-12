#!/usr/bin/env python3

import logging
import os
from dotenv import load_dotenv
import discord
# Configure logging for both logging to a file and logging to stdout.
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("debug.log"),
        logging.StreamHandler()
    ]
)

client = discord.Client()  # create our client


@client.event
async def on_ready():
    """
    event when we log in
    """
    logging.info('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    """
    event when someone sends a message in a channel
    """
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')


def main():
    """
    runs our bot
    """
    load_dotenv()  # load our .env file into environment variables
    # this is used to read our DISCORD_TOKEN in without having
    # the token committed to the repository.

    # Here's how you make a bot:
    # https://discordpy.readthedocs.io/en/stable/discord.html#discord-intro

    # Here's discord.py's quick start:
    # https://discordpy.readthedocs.io/en/stable/quickstart.html

    # Here's discord.py's documentation:
    # https://discordpy.readthedocs.io/en/stable/index.html

    # run the client:
    client.run(os.environ['DISCORD_TOKEN'])
    # this blocks until we press Ctrl-C


if __name__ == "__main__":
    main()
