"""Broker system to handle messages between objects"""

__author__ = "Samuel Whang"

class Broker:
    def __init__(self, name):
        self.name = name
        self.handlers = dict()

    def add_location(self, name, handler):
        if name in self.handlers.keys():
            raise ValueError(f"Location with {name} already exists in broker.")
        self.handlers[name] = handler

    def send(self, name_from, name_to, message):
        if name_to not in self.handlers.keys():
            raise ValueError(f"Location with {name_to} does not exist in broker.")
        self.handlers[name_to](name_from, message)

if __name__ == "__main__":
    class Test:
        def __init__(self, name, b):
            self.name = name
            self.b = b

        def send(self):
            self.b.send(self.name, 'B', 'sent from A')

        def recieve(self, name_from, message):
            print(f"{self.name}: {message}")

    broker = Broker("test")
    a = Test('A', broker)
    b = Test('B', broker)
    broker.add_location(b.name, b.recieve)
    a.send()
