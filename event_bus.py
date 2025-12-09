# event_bus.py
from typing import Callable
import asyncio
import inspect


class EventBus:
    def __init__(self):
        self.subscribers: dict[str, list[Callable]] = {}

    def subscribe(self, event_type: str, callback: Callable):
        if event_type not in self.subscribers:
            self.subscribers[event_type] = []
        self.subscribers[event_type].append(callback)

    async def publish(self, event_type: str, data):
        if event_type in self.subscribers:
            for callback in self.subscribers[event_type]:
                result = callback(data)
                if inspect.iscoroutine(result):
                    asyncio.create_task(result)