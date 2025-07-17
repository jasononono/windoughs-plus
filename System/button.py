from System.templates import Object
from System.Assets import palette

class Button(Object):
    def __init__(self, position, size,
                 colour = palette.light2, hover_colour = None, active_colour = None, pressed_colour = None):
        super().__init__(position, size)
        self.colour = colour
        self.hoverColour = hover_colour or colour
        self.activeColour = active_colour or hover_colour
        self.pressedColour = pressed_colour or hover_colour

        self.status = True
        self.hover = False
        self.active = False
        self.pressed = False

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
        parent.display(self.surface, self.rect)

        if system.event.mouse_up():
            self.pressed = False
            if self.status and self.hover:
                return True
        return False