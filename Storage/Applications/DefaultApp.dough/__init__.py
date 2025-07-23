import System.dough as d
import pygame as p

surface = d.new((400, 300))

surface.set_title("this is a window ig")


def refresh():
    surface.fill((255, 255, 255))
    surface.flip()

    for e in surface.get_events():
        if e.type == d.control.QUIT:
            d.quit()

    # MAKE PRESET MODULE FOR THESE STUFF (resize package, maximize package, etc.)