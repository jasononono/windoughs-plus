import pygame as p

from System.templates import Object, Image
from System.settings import Settings, User


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


class System(Object):
    def __init__(self, size = (800, 600)):
        super().__init__()
        self.surface = p.display.set_mode(size, p.SCALED, vsync = True)
        self.rect.size = size

        self.event = Event()

        self.settings = Settings()
        self.user = User()
        self.user.load("user")

        self.execute = True
        self.title = "Windoughs " + self.settings.version
        self.cursor = p.SYSTEM_CURSOR_ARROW

        self.wallpaper = Image(self.settings.wallpaper)
        self.load_wallpaper()

    def resize(self, size):
        self.surface = p.display.set_mode(size, p.SCALED, vsync = True)
        self.rect.size = size
        self.load_wallpaper()

    def load_wallpaper(self):
        self.wallpaper = Image(self.user.wallpaper or self.settings.wallpaper)
        factor = min(self.wallpaper.size[0] / self.rect.width, self.wallpaper.size[1] / self.rect.height)
        self.wallpaper.resize([i / factor for i in self.wallpaper.size])

    def refresh(self):
        self.event.refresh()
        if self.event.detect(p.QUIT):
            self.execute = False

        self.display(self.wallpaper.surface, [self.rect.center[i] - self.wallpaper.size[i] / 2 for i in range(2)])