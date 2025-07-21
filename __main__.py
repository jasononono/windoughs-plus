from System import requirement
requirement.dependency_check()


import pygame as p
from System.settings import settings
from System.system import System


p.init()
p.font.init()

system = System()
clock = p.time.Clock()

while system.execute:
    clock.tick(settings.fps)
    system.refresh()

    p.display.set_caption(system.title)
    p.mouse.set_cursor(system.cursor)
    p.display.flip()
p.quit()
