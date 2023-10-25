from typing import Optional

import yt_dlp

from config import config
from music_queue import StreamableSource
from player import AudioProvider, SongName, URL


class Youtube(AudioProvider):

    def get_source(self, song: SongName | URL) -> Optional[StreamableSource]:
        with yt_dlp.YoutubeDL(config["YDL_OPTIONS"]) as ydl:
            info = ydl.extract_info(song, download=True)
        return ydl.prepare_filename(info).replace(".webm", ".m4a")

