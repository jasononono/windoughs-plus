import System.dough as d


class Root:
    def __init__(self):
        self.surface = d.new((400, 300))
        self.surface.use_shortcut(d.shortcut.USER_QUIT)
        self.surface.set_title("Application")

    def refresh(self):
        pass


root = Root()
def refresh():
    root.refresh()