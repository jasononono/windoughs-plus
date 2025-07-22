import pygame as p

from System.templates import Object, Image
from System.settings import settings, user
from System.window import Window

from System.dough import linker


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

        user.load("user")

        self.execute = True
        self.active = None
        self.title = "Windoughs " + settings.version
        self.cursor = p.SYSTEM_CURSOR_ARROW

        self.wallpaper = Image(settings.wallpaper)
        self.load_wallpaper()

        self.windows = []

        linker.system = self
        linker.settings = settings
        linker.user = user

        linker.start_application("/Users/jason/Documents/CS/windoughs+/Storage/Applications/DefaultApp.dough")

    def resize(self, size):
        self.surface = p.display.set_mode(size, p.SCALED, vsync = True)
        self.rect.size = size
        self.load_wallpaper()

    def load_wallpaper(self):
        self.wallpaper = Image(user.wallpaper or settings.wallpaper)
        factor = min(self.wallpaper.size[0] / self.rect.width, self.wallpaper.size[1] / self.rect.height)
        self.wallpaper.resize([i / factor for i in self.wallpaper.size])

    def overlapping_window(self, position):
        for i in self.windows:
            if not i.hidden and list(i.rect.topleft) == position:
                return True
        return False

    def new_window(self, position = None, *args, **kwargs):
        self.windows.append(Window((0, 0), *args, **kwargs))
        if position is None:
            position = [self.rect.center[i] - self.windows[-1].rect.size[i] / 2 for i in range(2)]
            while self.overlapping_window(position):
                position[0] += 20
                position[1] += 20
        self.windows[-1].rect.topleft = position
        self.active = self.windows[-1]

        return self.windows[-1]

    def destroy_window(self, window):
        self.windows.remove(window)
        if self.active is window:
            self.activate_topmost_window()

    def activate_topmost_window(self):
        for i in self.windows[::-1]:
            if not i.hidden:
                self.activate_window(i)
                return
        self.active = None

    def activate_window(self, window = None):
        if window:
            self.active = window
            self.windows.remove(window)
            self.windows.append(window)
        else:
            self.active = None

    def refresh(self):
        self.event.refresh()
        self.cursor = p.SYSTEM_CURSOR_ARROW
        if self.event.detect(p.QUIT):
            self.execute = False

        self.display(self.wallpaper.surface, [self.rect.center[i] - self.wallpaper.size[i] / 2 for i in range(2)])

        ###
        # self.display(self.font.render("press W to summon a new window", True, palette.black), (10, 10))
        # self.display(self.font.render("press H to retrieve minimized windows", True, palette.black), (10, 40))
        # if self.event.key_down(p.K_w):
        #     self.new_window()
        # if self.event.key_down(p.K_h):
        #     for i in self.windows:
        #         i.hidden = False
        ###

        mouse_down = self.event.mouse_down()
        bring_to_front = None
        i = 0
        while i < len(self.windows):
            result = self.windows[i].refresh(self, self)
            if not result:
                if (mouse_down and not self.windows[i].hidden and
                    (self.windows[i].collidepoint(self.event.mousePosition) or self.windows[i].resizing)):
                    bring_to_front = self.windows[i]
                i += 1
        if mouse_down:
            self.activate_window(bring_to_front)