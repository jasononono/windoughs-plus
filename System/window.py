import pygame as p

from System.templates import Object, FancyObject, Image, Event
from System.settings import settings
from System import icon
from System.button import IconButton
from System.TextEngine.text import Label
from System.Assets import palette


class TitleBar(Object):
    def __init__(self, size):
        self.height = size[1]
        super().__init__((1, 1), size)

        self.dragged = False
        self.dragOffset = (0, 0)

        self.icon = Image("System/Assets/iconDefault.png")
        self.icon.resize((16, 16))
        self.title = Label(font_size = 13)

        self.exit = IconButton((0, 0), (40, self.height), icon.x, (10, 10), 2,
                               palette.light0, palette.red, palette.light1,
                               icon_hover = palette.white, icon_active = palette.light3)
        self.maximize = IconButton((0, 0), (40, self.height), icon.square, (10, 10), 1,
                                   palette.light0, palette.light2, palette.light1, icon_active = palette.light3)
        self.minimize = IconButton((0, 0), (40, self.height), icon.hLine, (10, 10), 1,
                                   palette.light0, palette.light2, palette.light1, icon_active = palette.light3)

    def refresh(self, system, parent):
        self.rect.refresh(parent.rect)

        self.fill(palette.light0 if system.active is parent else palette.light1)

        if self.rect.width > 148:
            self.display(self.icon.surface, (12, (self.height - self.icon.size[1]) / 2))

        self.title.foreground = palette.light4 if system.active is parent else palette.light3
        self.title.text = parent.title
        self.display(self.title.render(), (40, (self.height - self.title.size[1]) / 2.1))

        self.draw_rect(palette.light0 if system.active is parent else palette.light1,
                       (self.rect.width - 132, 0, 12, self.height))

        self.exit.rect.topleft = (self.rect.width - 40, 0)
        self.maximize.rect.topleft = (self.rect.width - 80, 0)
        self.minimize.rect.topleft = (self.rect.width - 120, 0)
        self.exit.active = self.maximize.active = self.minimize.active = system.active is not parent
        self.exit.status = self.maximize.status = self.minimize.status = not self.exit.active
        self.maximize.status = parent.resizable and self.maximize.status
        self.maximize.active = not self.maximize.status

        result = self.exit.refresh(system, self)

        if self.maximize.refresh(system, self):
            if parent.snapped:
                parent.resize(parent.restoredSize)
                parent.rect.topleft = parent.restoredPosition
                parent.snapped = False
            else:
                parent.restoredSize = (parent.rect.width, parent.rect.height - self.height)
                parent.restoredPosition = parent.rect.topleft
                parent.resize([i + 2 for i in system.rect.size], False)
                parent.rect.topleft = (-1, -1)
                parent.snapped = True

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
            parent.snapped = False

        return result


class Content(Object):
    def __init__(self, position, size):
        super().__init__(position, size)

    def refresh(self, parent):
        self.rect.refresh(parent.rect)
        parent.display(self.surface, self.rect)


class Window(FancyObject):
    def __init__(self, position, size = (400, 300), title = "New Window", title_height = 32, resizable = True):
        super().__init__(position, (size[0] + 2, size[1] + title_height + 2), True,
                         True, True, settings.cornerRadius, palette.light2)

        self.title = title
        self.titleBar = TitleBar((self.rect.width - 2, title_height))
        self.content = Content((1, self.titleBar.height + 1), size)

        self.minSize = [132, 50]
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
        self.snapped = False

        self.event = Event()

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
                                      (self.rect.abs.left - self.rect.left)),
                                     self.resizeAnchor[0] - self.minSize[0] - 2)
            elif self.resizing in [2, 6, 8]:
                self.resize((system.event.mousePosition[0] - self.resizeOffset[0] - self.resizeAnchor[0],
                             self.rect.size[1]), False)
            if self.resizing in [3, 5, 6]:
                self.resize((self.rect.size[0], self.resizeAnchor[1] -
                             system.event.mousePosition[1] + self.resizeOffset[1]), False)
                self.rect.top = min((system.event.mousePosition[1] - self.resizeOffset[1] -
                                     (self.rect.abs.top - self.rect.top)),
                                    self.resizeAnchor[1] - self.minSize[1] - self.titleBar.height - 2)
            elif self.resizing in [4, 7, 8]:
                self.resize((self.rect.size[0], system.event.mousePosition[1] - self.resizeOffset[1] -
                             self.resizeAnchor[1]), False)
            if self.snapped and (self.rect.left != -1 and self.rect.right != system.rect.width + 1 and
                self.rect.top != -1 and self.rect.bottom != system.rect.height + 1):
                self.snapped = False

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
        self.rect.refresh(parent.rect)
        self.event.refresh()

        if self.hidden:
            return False
        if self.resizable:
            self.user_resize(system)

        result = self.titleBar.refresh(system, self)

        self.rounding = not self.snapped
        self.fancify()

        parent.display(self.surface, self.rect)
        return result