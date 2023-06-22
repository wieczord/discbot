from collections import deque


class MusicQueue:
    def __init__(self):
        self.queue: dict = {}

    def __len__(self):
        return len(self.queue)

    def __getitem__(self, key):
        return self.queue[key]

    def add(self, channel_id: str, url: str):
        self.queue.setdefault(channel_id, deque()).append(url)

    def next(self, channel_id: str):
        try:
            return self.queue[channel_id].popleft()
        except IndexError:
            return None

    def empty(self, channel_id: str):
        try:
            return len(self.queue[channel_id]) == 0
        except KeyError:
            return True
