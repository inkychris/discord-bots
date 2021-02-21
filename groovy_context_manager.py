import getpass
import logging
import os
import re

import discord


def _looks_like_groovy_cmd(string):
    return re.match(r'^\s*-\s*\w+\s*', string) is not None


logger = logging.getLogger('groovy context manager')
intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)


@client.event
async def on_ready():
    logger.info(f'{client.user} connected to Discord!')


async def warn_is_non_groovy_cmd(message):
    await message.reply(
        content=f"That message doesn't look like a groovy command, are you in the right channel?",
        delete_after=10)


async def warn_is_groovy_cmd(message):
    await message.reply(
        content=f"That message looks like a groovy command, are you in the right channel?",
        delete_after=10)


@client.event
async def on_message(message):
    if message.author == client.user or message.author.bot:
        return

    groovy_bot_in_channel = 234395307759108106 in (member.id for member in message.channel.members)
    looks_like_groovy_text_channel = 'groovy' in message.channel.name.lower()
    looks_like_groovy_cmd = _looks_like_groovy_cmd(message.content)

    if groovy_bot_in_channel and looks_like_groovy_text_channel and not looks_like_groovy_cmd:
        await warn_is_non_groovy_cmd(message)
    elif not groovy_bot_in_channel and looks_like_groovy_cmd:
        await warn_is_groovy_cmd(message)


if __name__ == '__main__':
    import coloredlogs

    API_TOKEN = os.getenv('DISCORD_TOKEN')
    if not API_TOKEN:
        API_TOKEN = getpass.getpass('API Token: ')

    coloredlogs.install('INFO')
    client.run(API_TOKEN)
