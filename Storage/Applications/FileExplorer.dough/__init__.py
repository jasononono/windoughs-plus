import System.dough as d

from System.templates import Object
from System.Assets import palette


class Root(Object):
    def __init__(self):
        super().__init__(size = (400, 300))
        self.surface = d.new((400, 300), resizable = True)
        self.surface.use_shortcut(d.shortcut.USER_QUIT)
        self.surface.set_title("File Explorer")

        self.path = []
        self.pathName = ""

    def refresh(self):
        self.surface.fill(palette.white)

        self.pathName = "Storage/" + '/'.join(self.path)

        self.surface.flip()


root = Root()
def refresh():
    root.refresh()