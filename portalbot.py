#!/usr/bin/env python3

import logging
import os
import time
from dotenv import load_dotenv
import discord
from userdata import PointsData
# Configure logging for both logging to a file and logging to stdout.
logging.basicConfig(
    level=logging.WARNING,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("portalbot.log"),
        logging.StreamHandler()
    ]
)

# per https://stackoverflow.com/a/73821983:
# > Since discord.py 2.0, you must now activate privleged intents for
# >  specific actions. Messages are one of those actions.
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)  # create our client

data = PointsData('data.json')
mod_role_id = None


def validate_role(message: discord.Message):
    # validate that the message author has the right role:
    user_has_role = False
    for role in message.author.roles:
        logging.debug(f"role id: {role.id}")
        if int(role.id) == int(mod_role_id):
            user_has_role = True
            logging.debug("User has role.")
            break

    return user_has_role


@client.event
async def on_ready():
    """
    event when we log in
    """
    logging.info('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message: discord.Message):
    """
    event when someone sends a message in a channel
    """
    if message.author == client.user:
        logging.debug("Ignoring own message event.")
        return

    if message.content.startswith('!add'):
        logging.debug(f'Got "add" message from {message.author.display_name}')

        # validate they have the right role:
        if not validate_role(message):
            await message.add_reaction('❌')
            logging.warning(
                f'User {str(message.author.display_name)} !add-ed without role.')
            return

        content = message.content
        # format should be `!add @Saone#1234 num`
        tokens = content.split()

        # insert into our data:
        try:
            for user in message.mentions:
                logging.debug(f'Adding points for {str(user)}')
                data.modify_points(str(user), int(tokens[-1]))
        except (ValueError, IndexError):
            # if the message is malformed, don't do anything
            await message.add_reaction('❌')
            await message.channel.send("Error parsing message. Try `!add <mention> num`.")
            logging.error(f'Error adding points to user {str(user)}')
            return

        await message.add_reaction('✅')

    if message.content.startswith("!resetuser"):
        logging.debug(
            f'Got "resetuser" message from {message.author.display_name}')

        # validate they have the right role:
        if not validate_role(message):
            await message.add_reaction('❌')
            logging.warning(
                f'User {str(message.author.display_name)} !resetuser-ed without role.')
            return

        try:
            for user in message.mentions:
                logging.debug(f'Resetting points for {str(user)}')
                data.reset_points(str(user))
        except (ValueError, IndexError):
            # if the message is malformed, don't do anything
            await message.add_reaction('❌')
            await message.channel.send("Error parsing message. Try `!resetuser <mention>`.")
            logging.error(f'Error resetting points for user {str(user)}')
            return

        await message.add_reaction('✅')

    if message.content.startswith('!showpoints'):
        output = data.pretty_print()
        output = "Points Summary: \n" + output
        await message.channel.send(output)

    # if message.content.startswith('!help'):
    # (todo: write)
    #     await message.channel.send("")


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

    global mod_role_id
    mod_role_id = os.environ['MOD_ROLE_ID']
    logging.debug(f'Mod role id: {mod_role_id}')
    # run the client:
    client.run(os.environ['DISCORD_TOKEN'])
    # this blocks until we press Ctrl-C


if __name__ == "__main__":
    main()
