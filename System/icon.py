from System.templates import Model
from System.Assets import palette


class Instruction:
    def __init__(self):
        self.template = []

    def push(self, command, *args, **kwargs):
        self.template.append((command, args, kwargs))


class Icon(Model):
    def __init__(self, instruction, size = (0, 0), colour = palette.white, width = 1):
        super().__init__(size, True, ("size", "instruction", "colour", "width"))
        self.instruction = instruction
        self.colour = colour
        self.width = width
        self.auto = True

    def refresh(self):
        super().refresh()
        self.fill(palette.alpha)
        for i in self.instruction.template:
            i[0](self, *i[1], **i[2])

    def to_location(self, position):
        return [position[i] * (self.size[i] - (1 if self.width % 2 else 2)) for i in range(2)]

    def draw_line(self, start, end):
        super().draw_line(self.colour, self.to_location(start), self.to_location(end), self.width)


x = Instruction()
x.push(Icon.draw_line, (0, 0), (1, 1))
x.push(Icon.draw_line, (0, 1), (1, 0))

square = Instruction()
square.push(Icon.draw_line, (0, 0), (1, 0))
square.push(Icon.draw_line, (1, 0), (1, 1))
square.push(Icon.draw_line, (1, 1), (0, 1))
square.push(Icon.draw_line, (0, 1), (0, 0))

hLine = Instruction()
hLine.push(Icon.draw_line, (0, 0.5), (1, 0.5))