"""Text label UI component"""
from source.utils import point, size, box

# This is probably this simplest UI component to create. Use this class
# to determine specific properties for other components.
# TODO: add focusable, selectable, and hoverable? ie. More properties
class Text:
    focusable = False
    selectable = False
    default_label = ""
    def __init__(self, label=None):
        self.label = label if label else Text.default_label
        self.focused = False
        self.selected = False
    def draw(self, screen):
        pass
