# age.py

"""Basic class to hold an age value"""

import random


class Age(int):
    def __init__(self, years):
        self = years

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
    else:
        print("""
age.py
Usage: python basic.py [--test]"""[1:])

