import math

from System.templates import Object


class Window(Object):
    def __init__(self, system, size = (400, 300), position = (0, 0)):
        super().__init__(position, size, True)
        self.corner_sequence = []
        self.get_corner_sequence(system.settings.borderRadius)

    def refresh(self, system, parent):
        self.rect.refresh(parent.rect)

        self.fill((0, 0, 0))

        self.round_corners()
        parent.display(self.surface, self.rect)

    def get_corner_sequence(self, radius = 0):
        self.corner_sequence = []
        for i in range(radius):
            self.corner_sequence.append(round(radius - (radius ** 2 - (i + 1) ** 2) ** 0.5))

    def round_corners(self):
        length = len(self.corner_sequence)
        for i, n in enumerate(self.corner_sequence):
            for j in range(n):
                width = self.rect.width - length + i
                height = self.rect.height - j - 1
                self.surface.set_at((length - i - 1, j), (0, 0, 0, 0))
                self.surface.set_at((width, j), (0, 0, 0, 0))
                self.surface.set_at((length - i - 1, height), (0, 0, 0, 0))
                self.surface.set_at((width, height), (0, 0, 0, 0))