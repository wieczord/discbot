from typing import Protocol, TypeAlias, Optional

import discord

from music_queue import MusicQueue, StreamableSource

SongName: TypeAlias = str
URL: TypeAlias = str


class SourceFetchError(Exception):
    ...


class AudioProvider(Protocol):
    def get_source(self, song: SongName | URL) -> Optional[StreamableSource]:
        ...


class Player(Protocol):
    audio_provider: AudioProvider

    async def play(self, song: SongName | URL, channel: discord.VoiceChannel) -> None:
        ...


class MusicPlayer(Player):
    def __init__(self, audio_provider: AudioProvider, queue: MusicQueue):
        self.audio_provider = audio_provider
        self.music_queue = queue

    async def play(
        self, song: Optional[SongName | URL], client: discord.VoiceClient, channel_id: int
    ) -> None:
        if song is None:
            source = await self.music_queue.next(channel_id=client.channel.id) #TODO ujednolicic typ tego channelu bo jest syf, wszedzie inaczej
        else:
            source = self.audio_provider.get_source(song)
        if not source:
            raise SourceFetchError

        client.play(discord.FFmpegPCMAudio(source))

    async def add_to_queue(self, channel_id: int, url: URL) -> None:
        source = self.audio_provider.get_source(url)
        if not source:
            raise SourceFetchError
        self.music_queue.add(channel_id, source)


# TODO TRZYMANIE TEGO W QUEUE JAKO -SOURCE BEDZIE CHUJOWE, lepiej przerzucac te urle i napisac jakis wrapper na discord.FFmpegPCMAudio
