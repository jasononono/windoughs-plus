from System.templates import Object
from System import icon
from System.Assets import palette

class Button(Object):
    def __init__(self, position, size,
                 colour = palette.light1, hover_colour = None, active_colour = None, pressed_colour = None):
        super().__init__(position, size)
        self.colour = colour
        self.hoverColour = hover_colour or self.colour
        self.activeColour = active_colour or self.hoverColour
        self.pressedColour = pressed_colour or self.hoverColour

        self.status = True
        self.hover = False
        self.active = False
        self.pressed = False

    def content(self, parent):
        parent.display(self.surface, self.rect)

    def refresh(self, system, parent):
        self.rect.refresh(parent.rect)
        if self.collidepoint(system.event.mousePosition):
            self.hover = True
            if system.event.mouse_down():
                self.pressed = True
        else:
            self.hover = False

        if self.status and self.pressed:
            self.fill(self.pressedColour)
        elif self.active:
            self.fill(self.activeColour)
        elif self.status and self.hover:
            self.fill(self.hoverColour)
        else:
            self.fill(self.colour)

        self.content(parent)

        if system.event.mouse_up():
            if self.status and self.hover and self.pressed:
                self.pressed = False
                return True
            self.pressed = False
        return False


class IconButton(Button):
    def __init__(self, position, size, instruction, icon_size, icon_width = 1,
                 colour = palette.light1, hover_colour = None, active_colour = None, pressed_colour = None,
                 icon_colour = palette.light4, icon_hover = None, icon_active = None, icon_pressed = None):
        super().__init__(position, size, colour, hover_colour, active_colour, pressed_colour)
        self.icon = icon.Icon(instruction,
                              icon_size, icon_colour, icon_width)
        self.iconColour = icon_colour
        self.iconHover = icon_hover or self.iconColour
        self.iconActive = icon_active or self.iconHover
        self.iconPressed = icon_pressed or self.iconHover

    def content(self, parent):
        if self.status and self.pressed:
            self.icon.colour = self.iconPressed
        elif self.active:
            self.icon.colour = self.iconActive
        elif self.status and self.hover:
            self.icon.colour = self.iconHover
        else:
            self.icon.colour = self.iconColour

        self.display(self.icon.render(), [(self.rect.size[i] - self.icon.size[i]) / 2 for i in range(2)])
        parent.display(self.surface, self.rect)