import getpass
import logging
import os
import re

import discord


def _looks_like_groovy_cmd(string):
    return re.match(r'^\s*-\s*\w+\s*', string) is not None


class CustomClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_specific_prompts = {}


logger = logging.getLogger('groovy context manager')
intents = discord.Intents.default()
intents.members = True
client = CustomClient(intents=intents)


@client.event
async def on_ready():
    logger.info(f'{client.user} connected to Discord!')


async def warn_groovy_cmd(message, positive=True, user_specific_prompts=None):
    user_specific_prompts = user_specific_prompts or {}
    verb = "looks" if positive else "doesn't look"
    content = f"That message {verb} like a groovy command, "
    if message.author.id in user_specific_prompts.keys():
        content += user_specific_prompts[message.author.id]
    else:
        content += 'are you in the right channel?'
    await message.reply(content=content, delete_after=10)


@client.event
async def on_message(message):
    if message.author == client.user or message.author.bot:
        return

    groovy_bot_in_channel = 234395307759108106 in (member.id for member in message.channel.members)
    looks_like_groovy_text_channel = 'groovy' in message.channel.name.lower()
    looks_like_groovy_cmd = _looks_like_groovy_cmd(message.content)

    if groovy_bot_in_channel and looks_like_groovy_text_channel and not looks_like_groovy_cmd:
        await warn_groovy_cmd(message, positive=False, user_specific_prompts=client.user_specific_prompts)
    elif not groovy_bot_in_channel and looks_like_groovy_cmd:
        await warn_groovy_cmd(message, user_specific_prompts=client.user_specific_prompts)


if __name__ == '__main__':
    import coloredlogs

    API_TOKEN = os.getenv('DISCORD_TOKEN')
    if not API_TOKEN:
        API_TOKEN = getpass.getpass('API Token: ')

    coloredlogs.install('INFO')
    client.run(API_TOKEN)
