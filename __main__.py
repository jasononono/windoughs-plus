from System import requirement
requirement.dependency_check()


import pygame as p
from System.windoughs import Screen


screen = Screen()
clock = p.time.Clock()

while screen.settings.execute:
    clock.tick(screen.settings.fps)
    screen.refresh()

    p.display.set_caption(screen.settings.title)
    p.mouse.set_cursor(screen.settings.cursor)
    p.display.flip()
p.quit()
