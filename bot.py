import os

import discord
from discord.ext.commands import Bot
from dotenv import load_dotenv

from cogs.music import MusicCog
from config import config

from events import on_ready

load_dotenv()


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


def run_bot() -> None:
    token = os.environ.get("TOKEN")
    bot = create_bot()
    bot.run(token)
    init_bot(bot)


def init_bot(bot: Bot) -> None:
    init_cogs(bot)
    init_events(bot)


def init_cogs(bot: Bot) -> None:
    bot.add_cog(MusicCog(bot))


def init_events(bot: Bot) -> None:
    bot.add_listener(on_ready, 'on_ready')
