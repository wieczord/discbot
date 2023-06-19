import os
from dotenv import load_dotenv

load_dotenv()

import discord
import yt_dlp
from discord.ext import commands
import json

# Load the configuration from config.json
with open('config.json', 'r') as config_file:
    config = json.load(config_file)

intents = discord.Intents.default()

intents.voice_states = True
intents.presences = True
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix=config['prefix'], intents=intents)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name} ({bot.user.id})")
    print("Bot is ready to receive commands")


@bot.command()
async def join(ctx):
    channel = ctx.author.voice.channel
    voice_client = await channel.connect()


@bot.command()
async def leave(ctx):
    voice_client = ctx.voice_client
    await voice_client.disconnect()


@bot.command()
async def play(ctx, url):
    voice_client = ctx.voice_client
    if voice_client is None:
        channel = ctx.author.voice.channel
        voice_client = await channel.connect()

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'noplaylist': True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        url2 = info['url']
        voice_client.play(discord.FFmpegPCMAudio(url2))


token = os.environ.get("TOKEN")
bot.run(token)
