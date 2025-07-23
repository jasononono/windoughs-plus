import pygame as p

from . import linker


class RootSurface(p.Surface):
    def __init__(self, parent, window, flags = 0):
        super().__init__(window.content.rect.size, flags)
        self.window = window
        self.parent = parent

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