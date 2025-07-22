import System.dough as d
import pygame as p

surface = d.display.new((400, 400))

surface.set_title("hello")

surface.fill((255, 255, 255))
p.draw.rect(surface, (0, 0, 0), (10, 10, 10, 10))
surface.flip()

def refresh():
    pass