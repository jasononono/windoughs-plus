import pygame as p
import System.dough as d


surface = d.new((400, 300))
surface.use_shortcut(d.shortcut.USER_QUIT)

surface.set_title("this is a window ig")

tick = 0

def refresh():
    surface.fill((255, 255, 255))

    global tick
    tick += 1
    p.draw.rect(surface, (0, 0, 0), (30, 30, 10 + tick % 100, 30))

    surface.flip()