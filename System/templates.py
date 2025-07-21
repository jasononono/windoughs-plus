import pygame as p


class Rect(p.Rect):
    def __init__(self, position, size):
        super().__init__(position, size)
        self.abs = self.copy()

    def refresh(self, rect):
        self.abs.topleft = (self.x + rect.abs.x, self.y + rect.abs.y)
        self.abs.size = self.size


class Template:
    def __init__(self, size = (0, 0), alpha = False):
        self.surface = p.Surface(size, p.SRCALPHA) if alpha else p.Surface(size)

    def fill(self, *colour):
        self.surface.fill(colour)

    def display(self, surface, position):
        self.surface.blit(surface, position)

    def draw_rect(self, *args, **kwargs):
        p.draw.rect(self.surface, *args, **kwargs)

    def draw_circle(self, *args, **kwargs):
        p.draw.circle(self.surface, *args, **kwargs)

    def draw_line(self, *args, **kwargs):
        p.draw.line(self.surface, *args, **kwargs)

    def draw_aaline(self, *args, **kwargs):
        p.draw.aaline(self.surface, *args, **kwargs)


class Model(Template):
    def __init__(self, size = (0, 0), alpha = False, auto_refresh = tuple("size")):
        self.auto = False
        self.autoRefresh = auto_refresh

        super().__init__(size, alpha)
        self.size = size

    def __setattr__(self, key, value):
        super().__setattr__(key, value)
        if key == "auto" and value == False:
            return
        if key != "auto" and not self.auto:
            return
        if key in self.autoRefresh:
            self.update()

    def update(self):
        return

    def resize(self, size):
        self.surface = p.transform.scale(self.surface, size)
        self.size = size


class Object(Template):
    def __init__(self, position = (0, 0), size = (0, 0), alpha = False):
        super().__init__(size, alpha)
        self.rect = Rect(position, size)

    def resize(self, size):
        self.surface = p.transform.scale(self.surface, size)
        self.rect.size = size

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