import pygame as p


class Key:
    def __init__(self, base = None, shift = None, ctrl = None, alt = None):
        self.base = base
        self.shift = shift
        self.ctrl = ctrl
        self.alt = alt


class Command:
    def __init__(self, function, repeat = True, follow = True):
        self.function = function
        self.repeat = repeat
        self.follow = follow

    def __call__(self, *args, **kwargs):
        return self.function(*args, **kwargs)