import pygame as p
import importlib.util

from System.templates import Object, Image, Event
from System.settings import settings, user
from System.window import Window


class System(Object):
    def __init__(self, size = (800, 600)):
        super().__init__()
        self.surface = p.display.set_mode(size, p.SCALED, vsync = True)
        self.rect.size = size

        self.event = Event()

        user.load("user")

        self.execute = True
        self.active = None
        self.title = "Windoughs+ " + settings.version
        self.cursor = p.SYSTEM_CURSOR_ARROW

        self.wallpaper = Image(settings.wallpaper)
        self.load_wallpaper()

        self.windows = []
        self.applications = {}

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
        self.activate_window()

    def activate_window(self, window = None):
        if window:
            self.active = window
            self.windows.remove(window)
            self.windows.append(window)
        else:
            self.active = None

    def open_application(self, path):
        index = 0
        while "exec" + str(index) in self.applications.keys():
            index += 1
        name = "exec" + str(index)
        module_spec = importlib.util.spec_from_file_location(name, path + "/__init__.py")
        file = importlib.util.module_from_spec(module_spec)

        module_spec.loader.exec_module(file)
        self.applications[name] = file.Root(self)

    def refresh(self):
        self.event.event = p.event.get()
        self.event.key = p.key.get_pressed()
        self.event.mouse = p.mouse.get_pressed()
        self.event.mousePosition = p.mouse.get_pos()

        self.cursor = p.SYSTEM_CURSOR_ARROW
        if self.event.detect(p.QUIT):
            self.execute = False

        self.display(self.wallpaper.surface, [self.rect.center[i] - self.wallpaper.size[i] / 2 for i in range(2)])

        if self.event.key_down(p.K_w):
            self.open_application("Storage/Applications/DefaultApp.dough")

        mouse_down = self.event.mouse_down()
        bring_to_front = None
        i = 0
        while i < len(self.windows):
            if self.windows[i].refresh(self, self):
                self.destroy_window(self.windows[i])
            if (mouse_down and not self.windows[i].hidden and
                (self.windows[i].collidepoint(self.event.mousePosition) or self.windows[i].resizing)):
                bring_to_front = self.windows[i]
            i += 1
        if mouse_down:
            self.activate_window(bring_to_front)

        for i in self.applications.values():
            i.refresh()

        for i in self.windows:
            i.content.refresh(i)