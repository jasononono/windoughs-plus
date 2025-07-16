from System.templates import Object
from System.Assets import palette


class TitleBar(Object):
    def __init__(self, size):
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
        if self.dragged:
            parent.rect.topleft = [system.event.mousePosition[i] - self.dragOffset[i] for i in range(2)]


class Window(Object):
    def __init__(self, system, size = (400, 300), position = (0, 0), title_bar_height = 32):
        super().__init__(position, size, True)
        self.corner_sequence = []
        self.get_corner_sequence(system.settings.borderRadius)

        self.titleBar = TitleBar((self.rect.width, title_bar_height))

    def refresh(self, system, parent):
        self.rect.refresh(parent.rect)

        self.fill(palette.light0)

        self.titleBar.refresh(system, self)
        #self.draw_rect(palette.light4, (0, 0, self.rect.width, self.rect.height), 1)
        self.round_corners()
        parent.display(self.surface, self.rect)

    def get_corner_sequence(self, radius = 0):
        self.corner_sequence = []
        for i in range(radius):
            self.corner_sequence.append(round(radius - (radius ** 2 - (i + 1) ** 2) ** 0.5))

    def antialias(self, pixel, center, radius, strength = 1):
        distance = sum([(pixel[i] - center[i]) ** 2 for i in range(2)]) ** 0.5
        alpha = (85 * radius + 255) * (distance - radius - strength) / -(radius + strength)
        original = list(self.surface.get_at(pixel))
        original[3] = min(255, max(0, alpha))
        self.surface.set_at(pixel, original)

    def round_corners(self):
        radius = len(self.corner_sequence)
        for i, n in enumerate(self.corner_sequence):
            for j in range(n):
                width = self.rect.width - radius
                height = self.rect.height - 1 - j
                self.antialias((radius - i - 1, j), (radius - 1, radius - 1), radius)
                self.antialias((width + i, j), (width, radius - 1), radius)
                self.antialias((radius - i - 1, height), (radius - 1, self.rect.height - radius), radius)
                self.antialias((width + i, height), (width, self.rect.height - radius), radius)