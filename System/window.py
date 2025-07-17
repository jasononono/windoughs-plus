from System.templates import Object
from System.Assets import palette


class TitleBar(Object):
    def __init__(self, size):
        self.height = size[1]
        super().__init__((0, 0), size)

        self.dragged = False
        self.dragOffset = (0, 0)

    def refresh(self, system, parent):
        self.rect.refresh(parent.rect)

        self.fill(palette.light1)
        parent.display(self.surface, self.rect)

        if system.event.mouse_down() and self.collidepoint(system.event.mousePosition):
            self.dragged = True
            self.dragOffset = [system.event.mousePosition[i] - parent.rect.abs.topleft[i] for i in range(2)]
        if system.event.mouse_up():
            self.dragged = False
        if system.active is parent and self.dragged:
            parent.rect.topleft = [system.event.mousePosition[i] - self.dragOffset[i] for i in range(2)]


class Content(Object):
    def __init__(self, position, size):
        super().__init__(position, size)

    def refresh(self, system, parent):
        self.rect.refresh(parent.rect)


class Window(Object):
    def __init__(self, system, position, size = (400, 300), title_height = 32):
        super().__init__(position, (size[0], size[1] + title_height), True)
        self.corner_sequence = []
        self.get_corner_sequence(system.settings.borderRadius)
        self.border_colour = palette.light3

        self.titleBar = TitleBar((self.rect.width, title_height))
        self.content = Content((0, self.titleBar.height), size)

    def refresh(self, system, parent):
        self.rect.refresh(parent.rect)

        self.border_colour = palette.light0 if system.active is self else palette.light3

        self.display(self.content.surface, self.content.rect)
        self.titleBar.refresh(system, self)
        self.draw_rect(self.border_colour, (0, 0, self.rect.width, self.rect.height), 1)
        self.round_corners()
        parent.display(self.surface, self.rect)

    def get_corner_sequence(self, radius = 0):
        self.corner_sequence = []
        for i in range(radius):
            self.corner_sequence.append(round(radius - (radius ** 2 - (i + 1) ** 2) ** 0.5))

    def antialias(self, pixel, center, radius, strength = 3):
        distance = sum([(pixel[i] - center[i]) ** 2 for i in range(2)]) ** 0.5
        alpha = 255 - (255 * (distance - radius - strength) / strength + 255)
        self.surface.set_at(pixel, list(self.border_colour) + [min(255, max(0, alpha))])

    def round_corners(self):
        radius = len(self.corner_sequence)
        width = self.rect.width - radius
        for i, n in enumerate(self.corner_sequence):
            for j in range(n):
                height = self.rect.height - 1 - j
                self.antialias((radius - i - 1, j), (radius, radius), radius)
                self.antialias((width + i, j), (width - 1, radius), radius)
                self.antialias((radius - i - 1, height), (radius, self.rect.height - radius - 1), radius)
                self.antialias((width + i, height), (width - 1, self.rect.height - radius - 1), radius)