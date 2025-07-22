from . import linker
from .surface import RootSurface


def new(size):
    return RootSurface(linker.system.new_window(size = size))