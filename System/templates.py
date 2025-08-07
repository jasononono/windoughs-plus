import pygame as p

from System.Assets import palette


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
        self.alpha = alpha

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
        self.pendingRefresh = False
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
            self.pendingRefresh = True

    def refresh(self):
        self.surface = p.Surface(self.size, p.SRCALPHA) if self.alpha else p.Surface(self.size)

    def render(self):
        if self.pendingRefresh:
            self.refresh()
        return self.surface


class Object(Template):
    def __init__(self, position = (0, 0), size = (0, 0), alpha = False):
        super().__init__(size, alpha)
        self.rect = Rect(position, size)

    def resize(self, size):
        self.surface = p.transform.scale(self.surface, size)
        self.rect.size = size

    def collidepoint(self, position, absolute = True):
        return self.rect.abs.collidepoint(position) if absolute else self.rect.collidepoint(position)


class FancyObject(Object):
    def __init__(self, position = (0, 0), size = (0, 0), alpha = False,
                 rounding = False, border = False, corner_radius = 0, border_colour = palette.alpha):
        super().__init__(position, size, alpha)
        self.rounding = rounding
        self.border = border
        self.border_colour = border_colour
        self.aaStrength = 2
        self.corner_sequence = []
        self.get_corner_sequence(corner_radius)

    def get_corner_sequence(self, radius = 0):
        self.corner_sequence = []
        for i in range(radius):
            self.corner_sequence.append(radius if i >= radius - self.aaStrength else
                                        round(radius - ((radius - self.aaStrength - i) *
                                                        (radius - self.aaStrength + i)) ** 0.5))

    def fancify(self):
        if self.border:
            self.draw_rect(self.border_colour, (0, 0, self.rect.width, self.rect.height), 1)
        if self.rounding:
            self.corners()

    def corners(self):
        radius = len(self.corner_sequence)
        if radius == 0:
            return

        width = self.rect.width - radius
        for i, n in enumerate(self.corner_sequence):
            for j in range(n):
                height = self.rect.height - 1 - j
                self.antialias((radius - i - 1, j), (radius, radius), radius)
                self.antialias((width + i, j), (width - 1, radius), radius)
                self.antialias((radius - i - 1, height), (radius, self.rect.height - radius - 1), radius)
                self.antialias((width + i, height), (width - 1, self.rect.height - radius - 1), radius)

    def antialias(self, pixel, center, radius):
        distance = sum([(pixel[i] - center[i]) ** 2 for i in range(2)]) ** 0.5
        original = self.surface.get_at(pixel)
        if distance >= radius:
            alpha = -255 * (distance - radius - self.aaStrength) / self.aaStrength
            alpha = min(255, max(0, alpha))
            if self.border:
                self.surface.set_at(pixel, list(self.border_colour) + [alpha])
            else:
                original.a = int(alpha)
                self.surface.set_at(pixel, original)

        else:
            alpha = (distance - radius + self.aaStrength / 2) / self.aaStrength * 2
            alpha = min(1, max(0, alpha))
            if self.border:
                self.surface.set_at(pixel, ([self.border_colour[i] * alpha +
                                             original[i] * (1 - alpha) for i in range(3)]))


class Image:
    def __init__(self, name):
        self.name = name
        self.surface = p.image.load(name)
        self.size = self.surface.get_size()

    def resize(self, size):
        self.size = size
        self.surface = p.transform.smoothscale(self.surface, size)


class Event:
    def __init__(self):
        self.event = None
        self.key = None
        self.mouse = None
        self.mousePosition = None

    def refresh(self):
        self.event = []
        self.key = []
        self.mouse = []
        self.mousePosition = []

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