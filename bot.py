import os

import discord
from discord.ext.commands import Bot
from dotenv import load_dotenv

from cogs.music import MusicCog
from config import config

from events import on_ready
from player import AudioProvider
from yt import Youtube

load_dotenv()


def get_default_provider() -> AudioProvider:
    return Youtube()


def create_intents() -> discord.Intents:
    intents = discord.Intents.default()
    intents.voice_states = True
    intents.presences = True
    intents.message_content = True
    intents.members = True
    return intents


def create_bot() -> Bot:
    bot = Bot(command_prefix=config['PREFIX'], intents=create_intents())
    return bot


async def run_bot() -> None:
    token = os.environ.get("TOKEN")
    bot = create_bot()
    await init_bot(bot)
    await bot.start(token)


async def init_bot(bot: Bot) -> None:
    await init_cogs(bot)
    init_events(bot)


async def init_cogs(bot: Bot) -> None:
    await bot.add_cog(MusicCog(bot, provider=get_default_provider()))


def init_events(bot: Bot) -> None:
    bot.add_listener(on_ready, 'on_ready')
