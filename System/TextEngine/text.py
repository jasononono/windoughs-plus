from System.templates import Model
from System.TextEngine.font import Font
from System.Assets import palette


class Label(Model):
    def __init__(self, text = "", font_size = 16, font_name = None, size = None,
                 foreground = palette.light4, background = None, bold = False, italic = False):
        super().__init__(size or (0, 0), True, ("maxSize", "text", "fontSize", "fontName", "bold", "italic",
                                                "foreground", "background"))
        self.maxSize = size
        self.text = text

        self.fontSize = font_size
        self.fontName = font_name
        self.bold = bold
        self.italic = italic
        self.font = None

        self.foreground = foreground
        self.background = background

        self.auto = True

    def resize(self, size = None):
        self.maxSize = size

    def refresh(self):
        self.font = Font(self.fontSize, self.fontName, self.bold, self.italic, self.foreground, self.background)
        if self.maxSize:
            self.size = self.maxSize
        else:
            pointer = 0
            for i in self.text:
                pointer += self.font.glyphs[i]
            self.size = pointer, self.font.height

        super().refresh()
        self.fill(self.background or palette.alpha)
        pointer = 0
        for i in self.text:
            self.display(self.font.render(i), (pointer, 0))
            pointer += self.font.glyphs[i]