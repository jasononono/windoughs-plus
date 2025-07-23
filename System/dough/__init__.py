from . import linker
from . import control
from .surface import RootSurface

__all__ = ["new", "quit", "control", "RootSurface"]


def new(size):
    window = linker.system.new_window(size = size)
    linker.data[linker.application].windows.append(window)
    return RootSurface(linker.application, window)

def quit():
    for i in linker.data[linker.application].windows:
        linker.system.destroy_window(i)
    linker.data[linker.application] = None