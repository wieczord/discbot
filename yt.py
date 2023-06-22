import discord
import yt_dlp

from config import config
from player import AudioProvider, SongName, URL


class Youtube(AudioProvider):

    def get_source(self, song: SongName | URL) -> discord.FFmpegPCMAudio:
        with yt_dlp.YoutubeDL(config["YDL_OPTIONS"]) as ydl:
            info = ydl.extract_info(song, download=False)
            source = info['formats'][0]['url']
        return discord.FFmpegPCMAudio(source)
