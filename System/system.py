import pygame as p

from System.templates import Object, Image
from System.settings import Settings, User
from System.window import Window


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
        self.active = None
        self.title = "Windoughs " + self.settings.version
        self.cursor = p.SYSTEM_CURSOR_ARROW

        self.wallpaper = Image(self.settings.wallpaper)
        self.load_wallpaper()

        self.windows = []

    def resize(self, size):
        self.surface = p.display.set_mode(size, p.SCALED, vsync = True)
        self.rect.size = size
        self.load_wallpaper()

    def load_wallpaper(self):
        self.wallpaper = Image(self.user.wallpaper or self.settings.wallpaper)
        factor = min(self.wallpaper.size[0] / self.rect.width, self.wallpaper.size[1] / self.rect.height)
        self.wallpaper.resize([i / factor for i in self.wallpaper.size])

    def overlapping_window(self, position):
        for i in self.windows:
            if list(i.rect.topleft) == position:
                return True
        return False

    def new_window(self, position = None, *args, **kwargs):
        if position is None:
            position = [0, 0]
            while self.overlapping_window(position):
                position[0] += 10
                position[1] += 10
        self.windows.append(Window(self, position, *args, **kwargs))
        self.active = self.windows[-1]

    def activate_window(self, window = None):
        if window:
            self.active = window
            self.windows.remove(window)
            self.windows.append(window)
        else:
            self.active = None

    def refresh(self):
        self.event.refresh()
        if self.event.detect(p.QUIT):
            self.execute = False
        if self.event.detect(p.KEYDOWN):
            self.new_window()

        self.display(self.wallpaper.surface, [self.rect.center[i] - self.wallpaper.size[i] / 2 for i in range(2)])

        mouse_down = self.event.mouse_down()
        bring_to_front = None
        for i in self.windows:
            i.refresh(self, self)
            if mouse_down and i.collidepoint(self.event.mousePosition):
                bring_to_front = i
        if mouse_down:
            self.activate_window(bring_to_front)