import collections
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

music_queue = collections.deque()
# redis would be good for this? or just a dict of deques with guild.id as key

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
async def play(ctx, url: str = ""):
    if not url:
        if not music_queue:
            await ctx.send("No URL provided.")
        else:
            url = music_queue.popleft()

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

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:  # TODO url search
        info = ydl.extract_info(url, download=False)
        url2 = info['url']
        # Check if there are any songs in the queue
        if len(music_queue) > 0:
            # Add the URL to the queue
            music_queue.extend(url2)
            await ctx.send("Added to queue: " + url)
        else:
            # Play the song immediately
            voice_client.play(discord.FFmpegPCMAudio(url2))
            await ctx.send("Now playing: " + url)
        voice_client.play(discord.FFmpegPCMAudio(url2))


@bot.command()
async def queue(ctx, url):
    voice_channel = ctx.author.voice.channel

    if voice_channel is None:
        await ctx.send("You must be in a voice channel to use this command.")
        return

    music_queue.append(url)
    await ctx.send("Added to queue: " + url)


@bot.command()
async def show_queue(ctx):
    if len(queue) > 0:
        return "\n".join(queue)
    else:
        return "The queue is empty."


@bot.command()
async def skip(ctx):
    if not music_queue:
        await ctx.send("No URL provided.")
        return

    url = music_queue.popleft()

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

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:  # TODO url search
        if voice_client.is_playing():
            voice_client.stop()
        info = ydl.extract_info(url, download=False)
        url2 = info['url']
        voice_client.play(discord.FFmpegPCMAudio(url2))


token = os.environ.get("TOKEN")
bot.run(token)
