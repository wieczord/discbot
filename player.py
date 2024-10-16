from abc import ABC, abstractmethod
from functools import partial
from typing import Protocol, TypeAlias, Optional

import discord

from music_queue import MusicQueue, StreamableSource

SongName: TypeAlias = str
URL: TypeAlias = str


class SourceFetchError(Exception):
    ...


class AudioProvider(ABC):
    def get_source(self, song: SongName | URL) -> Optional[StreamableSource]:
        if self.is_url(song):
            return self.get_from_url(song)
        return self.get_from_name(song)

    @abstractmethod
    def is_url(self, song: SongName | URL) -> bool:
        ...

    @abstractmethod
    def get_from_url(self, song: URL) -> StreamableSource | None:
        ...

    @abstractmethod
    def get_from_name(self, song):
        ...


class Player(Protocol):
    audio_provider: AudioProvider

    def play(
        self,
        client: discord.VoiceClient,
        song: SongName | URL | None = None,
    ) -> None:
        ...


class MusicPlayer(Player):
    def __init__(self, audio_provider: AudioProvider, queue: MusicQueue):
        self.audio_provider = audio_provider
        self.music_queue = queue

    def play(
        self,
        client: discord.VoiceClient,
        song: SongName | URL | None = None,
    ) -> None:
        if song is None:
            source = self.music_queue.next(channel_id=client.channel.id)
        else:
            source = self.audio_provider.get_source(song)
        if not source:
            raise SourceFetchError

        client.play(discord.FFmpegPCMAudio(source), after=partial(self.play, client))

    async def add_to_queue(
        self,
        channel_id: int,
        song: SongName | URL | None = None,
    ) -> None:
        source = self.audio_provider.get_source(song)
        if not source:
            raise SourceFetchError
        self.music_queue.add(channel_id, source)
