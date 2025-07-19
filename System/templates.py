import pygame as p
from pygame import gfxdraw


class Rect(p.Rect):
    def __init__(self, position, size):
        super().__init__(position, size)
        self.abs = self.copy()

    def refresh(self, rect):
        self.abs.topleft = (self.x + rect.abs.x, self.y + rect.abs.y)
        self.abs.size = self.size


class Object:
    def __init__(self, position = (0, 0), size = (0, 0), alpha = False):
        self.surface = p.Surface(size, p.SRCALPHA) if alpha else p.Surface(size)
        self.rect = Rect(position, size)

    def resize(self, size):
        self.surface = p.transform.scale(self.surface, size)
        self.rect.size = size

    def fill(self, *colour):
        self.surface.fill(colour)

    def display(self, surface, position):
        self.surface.blit(surface, position)

    def draw_rect(self, *args, **kwargs):
        p.draw.rect(self.surface, *args, **kwargs)

    def draw_circle(self, *args, **kwargs):
        p.draw.circle(self.surface, *args, **kwargs)

    def draw_aacircle(self, *args, **kwargs):
        gfxdraw.aacircle(self.surface, *args, **kwargs)

    def draw_line(self, *args, **kwargs):
        p.draw.line(self.surface, *args, **kwargs)

    def draw_aaline(self, *args, **kwargs):
        p.draw.aaline(self.surface, *args, **kwargs)

    def collidepoint(self, position, absolute = True):
        return self.rect.abs.collidepoint(position) if absolute else self.rect.collidepoint(position)


class Image:
    def __init__(self, name):
        self.name = name
        self.surface = p.image.load(name)
        self.size = self.surface.get_size()

    def resize(self, size):
        self.size = size
        self.surface = p.transform.smoothscale(self.surface, size)