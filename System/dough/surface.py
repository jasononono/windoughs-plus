import pygame as p

from . import linker


class RootSurface(p.Surface):
    def __init__(self, parent, window):
        super().__init__(window.content.rect.size)
        self.window = window
        self.parent = parent
        self.shortcuts = []

    def set_title(self, title):
        self.window.title = title

    def set_mode(self, size):
        self.window.resize(size)

    def flip(self):
        self.window.content.display(self, (0, 0))

    def destroy(self):
        linker.system.destroy_window(self.window)
        self.parent.windows.remove(self.window)

    def get_events(self):
        return self.window.events

    def get_keys(self):
        return self.window.key

    def get_mouse(self):
        return self.window.mouse

    def get_mouse_position(self):
        return self.window.mousePosition

    def use_shortcut(self, name):
        self.shortcuts.append(name)

    def set_resizable(self, status = True, min_size = None):
        self.window.resizable = status
        if min_size:
            self.window.minSize = min_size