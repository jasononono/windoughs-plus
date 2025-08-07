class Root:
    def __init__(self, system):
        self.system = system
        self.window = system.new_window(size = (400, 300))
        self.window.content.draw_rect((255, 255, 255), (10, 10, 20, 30))

    def refresh(self):
        return