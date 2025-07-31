import System.dough as d
import os

from System.templates import Object
from System.TextEngine.text import Label
from System.Assets import palette


class Root(Object):
    def __init__(self):
        super().__init__(size = (400, 300))
        self.surface = d.new((400, 300), resizable = True)
        self.surface.use_shortcut(d.shortcut.USER_QUIT)
        self.surface.set_title("File Explorer")

        self.path = []
        self.pathName = ""

        self.items = []
        self.labels = []

    def refresh(self):
        self.pathName = f".{'/'.join(self.path)}/"
        self.items = sorted([i for i in os.listdir(self.pathName)])

        self.surface.fill(palette.white)

        position = 10
        for i in range(min(len(self.items), len(self.labels))):
            self.labels[i].text = self.items[i]
            self.display(self.labels[i].render(), (10, position))
            position += 30

        if len(self.items) > len(self.labels):
            for i in range(len(self.items) - len(self.labels)):
                self.labels.append(Label(self.items[i]))
                self.display(self.labels[i].render(), (10, position))
                position += 30

        self.surface.flip()


root = Root()
def refresh():
    root.refresh()