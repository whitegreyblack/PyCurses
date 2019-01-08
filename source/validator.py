"""validator.py"""
import typing
from collections.abc import Iterable

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
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def __call__(self, *other, **kwargs):
        if len(kwargs.items()) > 0 and not other:
            other = (kwargs,)   # create a dictionary from all key word args
        
        for d in other:
            if not isinstance(d, dict) and not hasattr(d, '__dict__'):
                raise BaseException(InvalidObjectTypeError)
            
            if not isinstance(d, dict):
                d = d.__dict__

            for attr, atype in self.__dict__.items():
                if not attr in d.keys():
                    raise BaseException(NonExistantAttributeError.format(d, attr, atype))
                ottr = d[attr]
                otype = type(ottr)
                if not isinstance(ottr, atype):
                    raise BaseException(ImproperTypeError.format(d, attr, otype, atype))

if __name__ == "__main__":
    v = Validator(a=int, b=int) # create a validator v with some attributes

    v(a=3, b=4)                 # option 1: pass in as kwargs
    v({'a':3, 'b':4})           # option 2: pass in as object

    v(Example())                # using class with attributes pulled with __dict__
    bypass(v, Example(2, 'a'))  # raises error due to wrong type

    bypass(v, 3)                # skips args but raises error on nonmatching attribute
    bypass(v, {'c':5})          # adds kwargs to validator but missing other attributes

    # TODO: nested objects using iterables
    print(list() is Iterable)
    print(isinstance(list(), Iterable))
    print(isinstance(list.__call__(), Iterable))

    # TODO: pass in multiple objects using *args