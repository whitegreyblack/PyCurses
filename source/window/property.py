"""property.py"""

class WindowProperty(object):
    __slots__ = [
        'title',
        'title_centered',
        'focused',
        'showing',
        'border',
    ]
    def __new__(cls, props):
        print("WP new obj")
        i = super().__new__(cls)
        i.title = None
        i.title_centered = False
        i.focused = False
        i.showing = True
        i.border = False
        return i
    
    def __init__(self, props):
        print("WP init obj")
        print(props)
        for prop, value in props.items():
            if not prop in self.__slots__:
                raise AttributeError(f"Invalid attribute: {prop}")
            setattr(self, prop, value)

    def __repr__(self):
        attrs = ', '.join(f'{k}: {getattr(self, k)}' for k in self.__slots__)
        return f"WindowProperty({attrs})"

