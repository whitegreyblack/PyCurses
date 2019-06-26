"""picklist.py

Similar to scrollable in that there is scrolling but selectable elements are
divided into named sections. A bit more complexity involved in selecting the
elements in the list since each named group can be collapsed or expanded

See 'pycurses/data/sectionpicklist.txt' for more information on implementation
"""

from source.window.base import Window

class PickListElement(object):
    def __init__(self, name, children):
        self.name = name
        self.children = children
        self.visible = True
        self.expanded = False

    def add_child(self, el):
        self.children.append(el)

    def add_children(self, els):
        self.children.extend(els)

    def rem_children(self, els):
        for el in els:
            self.rem_child(el)

    def rem_child(self, el):
        self.children.remove(el)


class Picklist(Window):
    def __init__(self, props):
        # data is list of all named sections in the list
        self.data = props['data']

        self.picklist = []
        for d in self.data:
            if d.visible:
                self.picklist.append(d)
            if d.children:
                for c in d.children:
                    if c.visible:
                        self.picklist.append(c)

    def expand(self, i):
        if data[i].children:
            for c in d.children:
                if not c.visible:
                    self.picklist.append(c)

    def collapse(self, i):
        if data[i].children:
            for c in d.children:
                if c.visible:
                    self.picklist.remove(c)