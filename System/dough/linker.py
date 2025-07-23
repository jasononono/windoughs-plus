import importlib.util


class Default:
    @staticmethod
    def refresh():
        return


class Application:
    def __init__(self, file):
        self.file = file
        self.windows = []


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
        if data[application] is None:
            del data[application]
        else:
            i += 1
    application = "exec0"