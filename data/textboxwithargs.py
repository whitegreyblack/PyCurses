"""textbox that prints a string with call handlers to other data"""
import random

def get_a_number():
    return random.randint(0, 100)

class Text:
    def __init__(self, string, *datacalls):
        self.string = string
        self.calls = datacalls

    def __str__(self):
        return self.string.format(*(c() for c in self.calls))

if __name__ == "__main__":
    t = Text("My number is: {}", get_a_number)
    print(t)