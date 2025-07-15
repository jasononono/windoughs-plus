import json

class Settings:
    def __init__(self):
        self.data = {}
        self.load()

    def __getattr__(self, item):
        return self.data[item]

    def load(self):
        with open("System/settings.json", 'r') as f:
            self.data = json.load(f)

    def write(self):
        with open("System/settings.json", 'w') as f:
            json.dump(self.data, f)


class User:
    def __init__(self):
        self.name = ""
        self.data = {}

    def __getattr__(self, item):
        return self.data[item]

    def load(self, name):
        self.name = name
        with open("Storage/User/" + self.name + "/settings.json", 'r') as f:
            self.data = json.load(f)

    def write(self):
        with open("Storage/User/" + self.name + "/settings.json", 'w') as f:
            json.dump(self.data, f)