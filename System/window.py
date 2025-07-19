import pygame as p

from System.templates import Object
from System import icon
from System.button import IconButton
from System.Assets import palette


class TitleBar(Object):
    def __init__(self, size):
        self.height = size[1]
        super().__init__((1, 1), size)

        self.dragged = False
        self.dragOffset = (0, 0)

        self.exit = IconButton((0, 0), (40, self.height), icon.x, (10, 10), 2,
                               palette.light0, palette.red, palette.light1, icon_hover = palette.white, icon_active = palette.light3)
        self.maximize = IconButton((0, 0), (40, self.height), icon.square, (10, 10), 1,
                                   palette.light0, palette.light1)
        self.minimize = IconButton((0, 0), (40, self.height), icon.hLine, (10, 10), 1,
                                   palette.light0, palette.light1)

    def refresh(self, system, parent):
        self.rect.refresh(parent.rect)

        self.fill(palette.light0 if system.active is parent else palette.light1)

        self.exit.rect.topleft = (self.rect.width - 40, 0)
        self.maximize.rect.topleft = (self.rect.width - 80, 0)
        self.minimize.rect.topleft = (self.rect.width - 120, 0)
        self.exit.active = self.maximize.active = self.minimize.active = system.active is not parent
        self.exit.status = self.maximize.status = self.minimize.status = not self.exit.active

        result = self.exit.refresh(system, self)

        if self.maximize.refresh(system, self):
            if parent.rect.size == system.rect.size:
                parent.resize(parent.restoredSize)
                parent.rect.topleft = parent.restoredPosition
                parent.rounded = True
            else:
                parent.restoredSize = (parent.rect.width, parent.rect.height - self.height)
                parent.restoredPosition = parent.rect.topleft
                parent.resize(system.rect.size, False)
                parent.rect.topleft = (0, 0)
                parent.rounded = False

        if self.minimize.refresh(system, self):
            parent.hidden = True
            system.active = None

        parent.display(self.surface, self.rect)

        if (system.event.mouse_down() and not parent.resizing and self.collidepoint(system.event.mousePosition) and
            system.event.mousePosition[0] < self.rect.abs.right - 120):
            self.dragged = True
            self.dragOffset = [system.event.mousePosition[i] - parent.rect.abs.topleft[i] for i in range(2)]
        if system.event.mouse_up():
            self.dragged = False
        if system.active is parent and self.dragged:
            parent.rect.topleft = [system.event.mousePosition[i] - self.dragOffset[i] for i in range(2)]

        return result


class Content(Object):
    def __init__(self, position, size):
        super().__init__(position, size)

    def refresh(self, parent):
        self.rect.refresh(parent.rect)
        parent.display(self.surface, self.rect)


class Window(Object):
    def __init__(self, system, position, size = (400, 300), title_height = 32, resizable = True):
        super().__init__(position, (size[0] + 2, size[1] + title_height + 2), True)
        self.border_colour = palette.light2
        self.rounded = True
        self.aaStrength = 2
        self.corner_sequence = []
        self.get_corner_sequence(system.settings.borderRadius)

        self.titleBar = TitleBar((self.rect.width - 2, title_height))
        self.content = Content((1, self.titleBar.height + 1), size)

        self.minSize = [120, 50]
        self.resizable = resizable
        self.resizing = 0
        self.resizeOffset = [0, 0]
        self.resizeAnchor = [0, 0]
        self.resize_cursors = [p.SYSTEM_CURSOR_SIZEWE, p.SYSTEM_CURSOR_SIZEWE,
                               p.SYSTEM_CURSOR_SIZENS, p.SYSTEM_CURSOR_SIZENS,
                               p.SYSTEM_CURSOR_SIZENWSE, p.SYSTEM_CURSOR_SIZENESW,
                               p.SYSTEM_CURSOR_SIZENESW, p.SYSTEM_CURSOR_SIZENWSE]

        self.restoredSize = size
        self.restoredPosition = position
        self.hidden = False

    def resize(self, size, content = True):
        size = list(size)
        if content:
            size[0] = max(size[0], self.minSize[0])
            size[1] = max(size[1], self.minSize[1])
            super().resize((size[0] + 2, size[1] + self.titleBar.height + 2))
            self.content.resize(size)
            self.titleBar.resize((size[0], self.titleBar.height))
        else:
            size[0] = max(size[0], self.minSize[0] + 2)
            size[1] = max(size[1], self.minSize[1] + self.titleBar.height + 2)
            super().resize(size)
            self.content.resize((size[0] - 2, size[1] - self.titleBar.height - 2))
            self.titleBar.resize((size[0] - 2, self.titleBar.height))

    def user_resize(self, system):
        if system.event.mouse_up():
            self.resizing = 0
        if self.resizing:
            system.cursor = self.resize_cursors[self.resizing - 1]
            if self.resizing in [1, 5, 7]:
                self.resize((self.resizeAnchor[0] - system.event.mousePosition[0] + self.resizeOffset[0],
                             self.rect.size[1]), False)
                self.rect.left = min((system.event.mousePosition[0] - self.resizeOffset[0] -
                                      (self.rect.abs.left - self.rect.left)), self.resizeAnchor[0] - self.minSize[0])
            elif self.resizing in [2, 6, 8]:
                self.resize((system.event.mousePosition[0] - self.resizeOffset[0] - self.resizeAnchor[0],
                             self.rect.size[1]), False)
            if self.resizing in [3, 5, 6]:
                self.resize((self.rect.size[0], self.resizeAnchor[1] -
                             system.event.mousePosition[1] + self.resizeOffset[1]), False)
                self.rect.top = min((system.event.mousePosition[1] - self.resizeOffset[1] -
                                     (self.rect.abs.top - self.rect.top)),
                                    self.resizeAnchor[1] - self.minSize[1] - self.titleBar.height)
            elif self.resizing in [4, 7, 8]:
                self.resize((self.rect.size[0], system.event.mousePosition[1] - self.resizeOffset[1] -
                             self.resizeAnchor[1]), False)
            return

        if self.titleBar.exit.hover or self.titleBar.maximize.hover or self.titleBar.minimize.hover:
            return

        resize = 0
        if system.active is self:
            if self.rect.abs.top - 2 <= system.event.mousePosition[1] <= self.rect.abs.bottom + 2:
                if abs(system.event.mousePosition[0] - self.rect.abs.left) < 4:
                    resize = 1
                elif abs(system.event.mousePosition[0] - self.rect.abs.right) < 4:
                    resize = 2
            if self.rect.abs.left - 2 <= system.event.mousePosition[0] <= self.rect.abs.right + 2:
                if abs(system.event.mousePosition[1] - self.rect.abs.top) < 4:
                    resize = resize + 4 if resize else 3
                elif abs(system.event.mousePosition[1] - self.rect.abs.bottom) < 4:
                    resize = resize + 6 if resize else 4
        if resize:
            system.cursor = self.resize_cursors[resize - 1]
            if system.event.mouse_down():
                self.resizing = resize
                if resize in [1, 5, 7]:
                    self.resizeAnchor[0] = self.rect.abs.right
                    self.resizeOffset[0] = system.event.mousePosition[0] - self.rect.abs.left
                elif resize in [2, 6, 8]:
                    self.resizeAnchor[0] = self.rect.abs.left
                    self.resizeOffset[0] = system.event.mousePosition[0] - self.rect.abs.right
                if resize in [3, 5, 6]:
                    self.resizeAnchor[1] = self.rect.abs.bottom
                    self.resizeOffset[1] = system.event.mousePosition[1] - self.rect.abs.top
                elif resize in [4, 7, 8]:
                    self.resizeAnchor[1] = self.rect.abs.top
                    self.resizeOffset[1] = system.event.mousePosition[1] - self.rect.abs.bottom

    def refresh(self, system, parent):
        if self.hidden:
            return False
        if self.resizable:
            self.user_resize(system)

        self.rect.refresh(parent.rect)
        self.content.refresh(self)

        if self.titleBar.refresh(system, self):
            parent.destroy_window(self)
            return True
        self.draw_rect(self.border_colour, (0, 0, self.rect.width, self.rect.height), 1)
        if self.rounded:
            self.round_corners()
        parent.display(self.surface, self.rect)
        return False

    def get_corner_sequence(self, radius = 0):
        self.corner_sequence = []
        for i in range(radius):
            self.corner_sequence.append(radius if i >= radius - self.aaStrength else
                                        round(radius - ((radius - self.aaStrength - i) *
                                                        (radius - self.aaStrength + i)) ** 0.5))

    def antialias(self, pixel, center, radius):
        distance = sum([(pixel[i] - center[i]) ** 2 for i in range(2)]) ** 0.5
        if distance >= radius:
            alpha = -255 * (distance - radius - self.aaStrength) / self.aaStrength
            self.surface.set_at(pixel, list(self.border_colour) + [min(255, max(0, alpha))])
        else:
            alpha = (distance - radius + self.aaStrength / 2) / self.aaStrength * 2
            alpha = min(1, max(0, alpha))
            original = self.surface.get_at(pixel)
            self.surface.set_at(pixel, [self.border_colour[i] * alpha + original[i] * (1 - alpha) for i in range(3)])

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