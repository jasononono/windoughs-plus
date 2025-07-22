import importlib.util


class Default:
    @staticmethod
    def refresh():
        return


class Application:
    def __init__(self, file):
        self.file = file


data = {"exec0": Application(Default)}
application = data["exec0"]
system = None
settings = None
user = None


def start_application(path, name = None):
    global application
    name = name or "exec" + str(len(data.keys()))
    module_spec = importlib.util.spec_from_file_location(name, path + "/__init__.py")
    file = importlib.util.module_from_spec(module_spec)

    application = file
    module_spec.loader.exec_module(file)
    data[name] = Application(file)

    application = data["exec0"]

def refresh():
    global application
    for i in data.values():
        application = i
        i.file.refresh()
    application = data["exec0"]