from typing import Protocol, TypeAlias

import discord

SongName: TypeAlias = str
URL: TypeAlias = str


class AudioProvider(Protocol):
    def get_source(self, song: SongName | URL) -> discord.FFmpegPCMAudio:
        ...


class Player(Protocol):
    audio_provider: AudioProvider

    def play(self, song: SongName | URL, channel: discord.VoiceChannel) -> None:
        ...


class MusicPlayer(Player):
    def __init__(self, audio_provider: AudioProvider):
        self.audio_provider = audio_provider

    def play(self, song: SongName | URL, channel: discord.VoiceChannel) -> None:
        source = self.audio_provider.get_source(song)
        channel.play(source)
