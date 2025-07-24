import pygame as p

from . import linker
from . import shortcut


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

    def use_shortcut(self, name):
        self.shortcuts.append(name)
        if name == shortcut.USER_RESIZE:
            self.window.resizable = True