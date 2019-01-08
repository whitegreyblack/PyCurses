"""validator.py
Discontinued since Cerberus already exists.
May revisit later.
"""
import typing
from collections.abc import Iterable, Sequence

InvalidObjectTypeError = """
InvalidObjectTypeError: Object argument must be of type dict or have an attribute dict."""[1:]
NonExistantAttributeError = """
NonExistantAttributeError: {} is missing a validation attribute. Expected: {} of type {}."""[1:]
ImproperTypeError = """
ImproperTypeError: {} does not have the correct type for the attribute {}.
Expected: {}. Got {}."""[1:]

def bypass(fn, *args, **kwargs):
    try:
        fn(*args, **kwargs)
    except BaseException as e:
        print(e)

class Example:
    def __init__(self, a=1, b=2):
        self.a = a
        self.b = b
    def __repr__(self):
        return f"Example (a={self.a}, b={self.b})"

class Validator:
    types = {
        'int': int,
        'str': str,
        'list': list,
    }
    def __init__(self, model=None, exceptions=False):
        self.attributes = dict()
        self.exceptions = exceptions
        if model:
            self.attributes.update(model)

    def __repr__(self) -> str:
        d = ', '.join(f'{k}: {v}' for k, v in self.attributes.items())
        return f"Validator({d})"

    def __call__(self, other) -> bool:
        is_obj = False
        if not isinstance(other, dict) and not hasattr(other, '__dict__'):
            if self.exceptions:
                raise BaseException(InvalidObjectTypeError)
            return False
        
        d = other
        if not isinstance(d, dict):
            is_obj = True
            d = d.__dict__

        for attr, adef in self.attributes.items():
            # explicit keys required by other object
            # TODO: remove this so we chan check for all missing keys
            #       and return them as an exception list
            if not attr in d.keys():
                if self.exceptions:
                    raise BaseException(
                        NonExistantAttributeError.format(
                            d, 
                            attr, 
                            atype
                        ))
                return False

            ottr = d[attr]
            atype = adef['type']

            # top level element is true (int, str, list)
            if not isinstance(ottr, self.types[atype]):
                if self.exceptions:
                    raise BaseException(
                        ImproperTypeError.format(
                            d, 
                            attr, 
                            type(ottr),
                            atype
                        ))
                return False

            # singular types ('int', 'str') are single level. skip them
            if isinstance(ottr, Sequence):
                etype = adef['el']['type']
                for el in ottr:
                    if not isinstance(el, self.types[etype]):
                        raise BaseException(
                            ImproperTypeError.format(
                                d,
                                attr,
                                type(ottr[0]),
                                etype
                            ))
        return True

if __name__ == "__main__":
    # small tests
    v = Validator({'a': {'type': 'int'}})
    print(v({'a':3}))

    # TODO: nested objects using iterables
    x = Validator({'a': {'type': 'list', 'el': {'type': 'int'}}})
    print(x)
    x({'a': [1,2,3]})
    x({'a': [1,2,'a']})

    # TODO: nested objects after two levels