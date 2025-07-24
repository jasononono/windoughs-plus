from . import linker
from .surface import RootSurface


def new(size):
    window = RootSurface(linker.application, linker.system.new_window(size = size, resizable = False))
    linker.data[linker.application].root.append(window)
    return window

def quit():
    for i in linker.data[linker.application].root:
        linker.system.destroy_window(i.window)
    linker.data[linker.application] = None