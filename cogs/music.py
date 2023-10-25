from typing import Optional

from discord.ext.commands import Cog, command

from music_queue import MusicQueue
from player import MusicPlayer, AudioProvider, SourceFetchError, URL, SongName


class MusicCog(Cog):
    def __init__(self, bot, provider: AudioProvider, queue: MusicQueue):
        self.bot = bot
        self.provider = provider
        self.player = MusicPlayer(audio_provider=self.provider, queue=queue)
        self.voice_client = None
        self.channel_id = None

    @command()
    async def join(self, ctx):
        channel = ctx.author.voice.channel
        self.voice_client = await channel.connect()
        self.channel_id = self.voice_client.channel.id

    @command()
    async def leave(self, ctx):
        voice_client = ctx.voice_client
        await voice_client.disconnect()
        self.voice_client = None
        '''
!play https://www.youtube.com/watch?v=zI383uEwA6Q
!queue https://www.youtube.com/watch?v=JjbnO5yUpYc
        '''

    @command()
    async def play(self, ctx, song: Optional[SongName | URL] = None):
        if self.voice_client is None:
            await ctx.invoke(self.join)
        try:
            await self.player.play(song=song, client=self.voice_client, channel_id=self.channel_id)
        except SourceFetchError:
            await ctx.send("No song found")

    @command()
    async def stop(self, ctx):
        self.voice_client.stop()

    @command()
    async def pause(self, ctx):
        self.voice_client.pause()

    @command()
    async def resume(self, ctx):
        self.voice_client.resume()

    @command()
    async def skip(self, ctx):
        self.voice_client.stop()
        await ctx.invoke(self.play)

    @command()
    async def queue(self, ctx, url: str = ""):
        try:
            await self.player.add_to_queue(url=url, channel_id=self.channel_id)  # TODO ID sie beda zgadzac zawsze?
            await ctx.send(f"Added {url} to queue")
        except SourceFetchError:
            await ctx.send(f"Could not add {url} to queue")
