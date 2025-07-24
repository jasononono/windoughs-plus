from System import requirement
requirement.dependency_check()


import pygame as p
import math
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

    # fps counter

    # if clock.get_fps() != 0:
    #     fps = math.log(60, 2) - math.log(clock.get_fps(), 2)
    #     print(str(max(0, round((1 - 0.1 ** fps) * 100))) + "%")

p.quit()
