import getpass
import logging
import os
import re

import discord


def looks_like_groovy_cmd(string):
    return re.match(r'^\s*-\s*\w+\s*', string) is not None


logger = logging.getLogger('groovy context manager')
client = discord.Client()


@client.event
async def on_ready():
    logger.info(f'{client.user} connected to Discord!')


@client.event
async def on_message(message):
    if message.author == client.user or message.author.bot:
        return
    if message.channel.name == 'groovy':
        if not looks_like_groovy_cmd(message.content):
            await message.reply(
                content=f"That message doesn't look like a groovy command, are you in the right channel?",
                delete_after=10)
    else:
        if looks_like_groovy_cmd(message.content):
            await message.reply(
                content=f"That message looks like a groovy command, are you in the right channel?",
                delete_after=10)


if __name__ == '__main__':
    import coloredlogs

    API_TOKEN = os.getenv('DISCORD_TOKEN')
    if not API_TOKEN:
        API_TOKEN = getpass.getpass('API Token: ')

    coloredlogs.install('INFO')
    client.run(API_TOKEN)
