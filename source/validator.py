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
    attributes = dict()
    def __init__(self, exceptions=False, **kwargs):
        self.exceptions = exceptions
        self.attributes.update(kwargs)

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

        for attr, atype in self.attributes.items():
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
            otype = type(ottr)
            
            if not isinstance(ottr, atype):
                if self.exceptions:
                    raise BaseException(
                        ImproperTypeError.format(
                            d, 
                            attr, 
                            otype, 
                            atype
                        ))
                return False
        return True

if __name__ == "__main__":
    # small tests
    
    # create a validator v with some attributes
    v = Validator(a=int, b=int)
    u = Validator(a=int, b=int, exceptions=True)
    print(v, u)

    # option 1: pass in as dict
    print("v({'a':3, 'b':4}):", v({'a':3, 'b':4}))
    print("v({'a':3, 'b':'a'}):", v({'a':3, 'b':'a'}))
    # using class with attributes pulled with __dict__
    print("v(Example()):", v(Example()))
    print("v(Example(3, 'a')):", v(Example(3, 'a')))

    # Exception cases
    # skips args but raises error on nonmatching attribute
    bypass(u, 3)
    # adds kwargs to validator but missing other attributes
    bypass(u, {'c':5})

    # create a validator v with different definitions than v
    w = Validator(a=int, b=str)
    print(w)

    # given an (int, int) validated by an (int, str)
    # the validator should check the second attribute
    e = Example(2, 2)
    print("w(e):", w(e))

    # try the same example again but with a dictionary object
    # instead of a class object. Using w returns false, v returns true.
    d = {'a':3, 'b':4}
    print("w(d):", w(d))
    print("v(d):", v(d))

    # TODO: nested objects using iterables
    print(list() is Iterable)
    print(isinstance(list(), Iterable))
    print(isinstance(list.__call__(), Iterable))