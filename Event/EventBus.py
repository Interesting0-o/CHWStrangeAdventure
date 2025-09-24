import pygame as pg

class EventBus:
    # 这个类用于管理事件的发布与订阅
    # 这就是观察者模式的一种实现，也我之前说的是事件系统的实现
    instance = None

    def __new__(cls):
        if not cls.instance:
            cls.instance = super().__new__(cls)
        return cls.instance

    def __init__(self):
        self._topics: dict[str, list[callable]] = {}

    def on(self, topic: str, callback: callable):
        self._topics.setdefault(topic, []).append(callback)

    def off(self, topic: str, callback: callable):
        if topic in self._topics:
            self._topics[topic].remove(callback)

    def emit(self, topic: str, *args, **kwargs):
        for cb in self._topics.get(topic, []):
            cb(*args, **kwargs)