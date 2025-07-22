import pygame as p


class RootSurface(p.Surface):
    def __init__(self, window, flags = 0):
        super().__init__(window.content.rect.size, flags)
        self.window = window

    def set_title(self, title):
        self.window.title = title

    def set_mode(self, size):
        self.window.resize(size)

    def flip(self):
        self.window.content.display(self, (0, 0))