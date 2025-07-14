import pygame as p
import json
from System.utility import Object


class Event:
    def __init__(self):
        self.event = None
        self.key = None
        self.mouse = None
        self.mousePosition = None

    def refresh(self):
        self.event = p.event.get()
        self.key = p.key.get_pressed()
        self.mouse = p.mouse.get_pressed()
        self.mousePosition = p.mouse.get_pos()

    def detect(self, event):
        for e in self.event:
            if e.type == event:
                return e
        return None

    def detect_all(self, event):
        events = []
        for e in self.event:
            if e.type == event:
                events.append(e)
        return events

    def key_down(self, key = None):
        event = self.detect_all(p.KEYDOWN)
        keys = [i.key for i in event]
        if key:
            return key if key in keys else None
        return keys

    def key_up(self, key = None):
        event = self.detect_all(p.KEYUP)
        keys = [i.key for i in event]
        if key:
            return key if key in keys else None
        return keys

    def mouse_down(self):
        return self.detect(p.MOUSEBUTTONDOWN)

    def mouse_up(self):
        return self.detect(p.MOUSEBUTTONUP)


class Settings:
    def __init__(self):
        with open("System/settings.json") as f:
            self.data = json.load(f)

        self.execute = True
        self.title = "Windoughs"
        self.cursor = p.SYSTEM_CURSOR_ARROW

    def __getattr__(self, item):
        return self.data[item]


class Screen(Object):
    def __init__(self, size = (800, 600)):
        super().__init__()
        self.surface = p.display.set_mode(size, p.SCALED, vsync = True)
        self.event = Event()
        self.settings = Settings()

    def refresh(self):
        self.event.refresh()
        if self.event.detect(p.QUIT):
            self.settings.execute = False