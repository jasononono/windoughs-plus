import importlib.util

from . import shortcut
from . import control
from . import commands


class Default:
    @staticmethod
    def refresh():
        return


class Application:
    def __init__(self, file):
        self.file = file
        self.root = []


data = {"exec0": Application(Default)}
application = "exec0"
system = None
settings = None
user = None


def start_application(path):
    global application
    i = 1
    while "exec" + str(i) in data.keys():
        i += 1
    name = "exec" + str(i)

    module_spec = importlib.util.spec_from_file_location(name, path + "/__init__.py")
    file = importlib.util.module_from_spec(module_spec)
    data[name] = Application(file)

    application = name
    module_spec.loader.exec_module(file)
    application = "exec0"

def refresh():
    global application

    i = 0
    while i < len(data):
        application = list(data.keys())[i]
        data[application].file.refresh()
        execute_shortcuts()

        if data[application] is None:
            del data[application]
        else:
            i += 1
    application = "exec0"

def execute_shortcuts():

    for r in data[application].root:
        for s in r.shortcuts:

            if s == shortcut.USER_QUIT:
                for e in r.get_events():
                    if e.type == control.QUIT:
                        commands.quit()

            if s == shortcut.USER_CLOSE:
                for e in r.get_events():
                    if e.type == control.QUIT:
                        r.destroy()

        #r.size = r.window.content.rect.size
        # NEED TO SET r.size WITHOUT p.transform.scale RETURNING p.Surface

        # method that involves changing the addr

        # window = p.transform.scale(r, r.window.content.rect.size)
        # root_surface = RootSurface(r.parent, r.window)
        # root_surface.blit(window, (0, 0))
        # r = root_surface