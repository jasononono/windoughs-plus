class Event:
    def __init__(self, reference):
        self.attributes = {"type": reference}

    def __setitem__(self, key, value):
        self.attributes[key] = value

    def __getattr__(self, key):
        return self.attributes[key]


QUIT = 0
HIDDEN = 1
MOTION = 2
RESIZE = 3
MINIMIZE = 4
MAXIMIZE = 5
ACTIVE = 6
INACTIVE = 7

KEYDOWN = 8
KEYUP = 9
MOUSEMOTION = 10
MOUSEBUTTONUP = 11
MOUSEBUTTONDOWN = 12