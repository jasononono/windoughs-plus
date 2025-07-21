import pygame as p
import string

from System.settings import settings
from System.Assets import palette


class Font:
    def __init__(self, size, name = None, bold = False, italic = False, foreground = palette.light4, background = None):
        self.modifier = ("bolditalic" if italic else "bold") if bold else ("italic" if italic else "regular")
        self.size = size
        self.name = name or settings.systemFont
        self.foreground = foreground
        self.background = background

        self.template = p.font.Font(f"System/TextEngine/Fonts/{self.name}/{self.modifier}.ttf", size)
        self.glyphs = {i: j[4] for i, j in zip(string.printable, self.template.metrics(string.printable))}
        self.height = self.template.get_height()

    def render(self, text, foreground = None, background = False):
        return self.template.render(text, True,
                                    foreground or self.foreground, background or self.background or None)