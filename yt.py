import re

import yt_dlp

from config import config
from music_queue import StreamableSource
from player import AudioProvider, SongName, URL, SourceFetchError


class Youtube(AudioProvider):
    def is_url(self, song: SongName | URL) -> bool:
        yt_regex = re.compile(
            r"^((?:https?:)?//)?((?:www|m)\.)?((?:youtube(?:-nocookie)?\.com|youtu\.be))(\/(?:[\w\-]+\?v=|embed\/|live\/|v\/)?)([\w\-]+)(\S+)?$"
        )
        return bool(re.match(yt_regex, song))

    def get_from_name(self, song: SongName) -> StreamableSource | None:
        with yt_dlp.YoutubeDL(config["YDL_OPTIONS"]) as ydl:
            try:
                yt_url = ydl.extract_info(f"ytsearch:{song}", download=True)["entries"][
                    0
                ]["webpage_url"]
            except (KeyError, IndexError):
                return None

        return self.get_from_url(yt_url)

    def get_from_url(self, song: URL) -> StreamableSource | None:
        with yt_dlp.YoutubeDL(config["YDL_OPTIONS"]) as ydl:
            info = ydl.extract_info(song, download=True)
        return ydl.prepare_filename(info).replace(".webm", ".m4a")
