# property.py

""" Window property class """

from dataclasses import dataclass


@dataclass
class WindowProperty:
    focusable: bool = True
    focused: bool = False
    showing: bool = True
    border: bool = True

if __name__ == "__main__":
    p = WindowProperty()
    print(p, p.__dict__)
