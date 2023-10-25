config = {
    "PREFIX": "!",
    "FFMPEG_OPTIONS": {
        "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
        "options": "-vn",
    },
    "YDL_OPTIONS": {
        "format": "bestaudio/best",
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "aac",
                "preferredquality": "64",
            }
        ],
        "noplaylist": True,
        "extractaudio": True,
    },
}
