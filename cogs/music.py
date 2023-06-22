from discord.ext.commands import Cog, command

from player import MusicPlayer, AudioProvider


class MusicCog(Cog):
    def __init__(self, bot, provider: AudioProvider):
        self.bot = bot
        self.provider = provider
        self.player = MusicPlayer(audio_provider=self.provider)
        self.voice_client = None

    @command()
    async def join(self, ctx):
        channel = ctx.author.voice.channel
        self.voice_client = await channel.connect()

    @command()
    async def leave(self, ctx):
        voice_client = ctx.voice_client
        await voice_client.disconnect()
        self.voice_client = None

    @command()
    async def play(self, ctx, url: str = ""):
        if self.voice_client is None:
            await ctx.invoke(self.join)
        self.player.play(url, self.voice_client)
