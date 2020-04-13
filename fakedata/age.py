# age.py

"""Basic class to hold an age value"""

import random


class Age(int):
    """
    Age class for all non-negative values
    >>> Age(3)
    Age(value=3)
    """
    def __init__(self, years):
        if years < 0:
            raise ValueError(f"Years cannot be less than 0. Got: {years}")
        self = years
    def __repr__(self):
        return f"{self.__class__.__name__}(value={self})"
    @classmethod
    def random(cls, low=1, high=100):
        return cls(random.randint(low, high))

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print(Age(3))
    elif sys.argv[1] == '--test':
        import doctest
        doctest.testmod()
    elif int(sys.argv[1]):
        print(Age(int(sys.argv[1])))
    else:
        print("""
age.py
Usage: python basic.py [--test]"""[1:])

