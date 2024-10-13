from collections import deque
from typing import TypeAlias, Optional, Protocol

StreamableSource: TypeAlias = str


class MusicQueue(Protocol):
    def add(self, channel_id: int, url: StreamableSource):
        ...

    def next(self, channel_id: int) -> Optional[StreamableSource]:
        ...

    def empty(self, channel_id: int) -> bool:
        ...


class AsyncQueue(MusicQueue):
    def __init__(self):
        self._queue: dict[int, deque[StreamableSource]] = {}

    def __len__(self):
        return len(self._queue)

    def __getitem__(self, key):
        return self._queue[key]

    def __iter__(self):
        return self

    def add(self, channel_id: int, url: StreamableSource):
        self._queue.setdefault(channel_id, deque()).append(url)

    def next(self, channel_id: int) -> Optional[StreamableSource]:
        try:
            return self._queue[channel_id].popleft()
        except (KeyError, IndexError):
            return

    def empty(self, channel_id: int) -> bool:
        try:
            return len(self._queue[channel_id]) == 0
        except KeyError:
            return True
