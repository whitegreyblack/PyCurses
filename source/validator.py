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

    def __repr__(self):
        d = ', '.join(f'{k}: {v}' for k, v in self.__dict__.items())
        return f"Validator({d})"

    def __call__(self, other):
        is_obj = False
        if not isinstance(other, dict) and not hasattr(other, '__dict__'):
            raise BaseException(InvalidObjectTypeError)
        
        d = other
        if not isinstance(d, dict):
            is_obj = True
            d = d.__dict__

        for attr, atype in self.__dict__.items():
            if not attr in d.keys():
                raise BaseException(NonExistantAttributeError.format(d, attr, atype))
            
            ottr = d[attr]
            otype = type(ottr)
            
            if not isinstance(ottr, atype):
                try:
                    converted = atype(ottr)
                except:
                    raise BaseException(ImproperTypeError.format(d, attr, otype, atype))
                else:
                    if is_obj:
                        setattr(other, attr, converted)
                    else:
                        other[attr] = converted

if __name__ == "__main__":
    # small tests
    
    # create a validator v with some attributes
    v = Validator(a=int, b=int)
    print(v)

    # option 1: pass in as dict
    v({'a':3, 'b':4})
    # using class with attributes pulled with __dict__
    v(Example())
    # raises error due to wrong type
    bypass(v, Example(2, 'a'))

    # skips args but raises error on nonmatching attribute
    bypass(v, 3)
    # adds kwargs to validator but missing other attributes
    bypass(v, {'c':5})

    # create a validator v with different definitions than v
    w = Validator(a=int, b=str)
    print(w)

    # given an (int, int) validated by an (int, str)
    # the validator should check if the second attribute is
    # convertable to a str type. If so, then no exceptions
    # are raised and the object attr has a new value and type.
    e = Example(2, 2)
    print(e.b, type(e.b))
    w(e)       
    print(e.b, type(e.b))

    # try the same example again but with a dictionary object
    # instead of a class object. Should modify the reference
    # passed in and change the type of the attribute that is 
    # different than the validator definition.
    # try changing it back to the original definition using 
    # the first validator and checking the attribute type.
    d = {'a':3, 'b':4}
    print(d['b'], type(d['b']))
    w(d)
    print(d['b'], type(d['b']))
    v(d)
    print(d['b'], type(d['b']))

    # TODO: nested objects using iterables
    print(list() is Iterable)
    print(isinstance(list(), Iterable))
    print(isinstance(list.__call__(), Iterable))