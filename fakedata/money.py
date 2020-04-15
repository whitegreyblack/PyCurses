# Money.py

"""Basic generators"""

import random


class Money:
    """
    Money class that holds dollars and cents value as ints to determine values
    without any loss of precision during arithmetic operations.
        >>> Money(33, 22)
        Money($33.22)
        >>> str(Money(33, 22))
        '$33.22'
        >>> Money(33, 20) + Money(22, 33)
        Money($55.53)
        >>> Money(33, 20) - Money(22, 33)
        Money($10.87)
    """
    def __init__(self, dollars, cents=0):
        self.dollars = dollars
        self.cents = cents
    def __str__(self):
        return f"${self.dollars}.{self.cents:02}"
    def __repr__(self):
        return f"Money({str(self)})"
    def __add__(self, other):
        if isinstance(other, Money):
            total = self.total() + other.total()
            return Money(total // 100, total % 100)
        raise ValueError("Cannot add {other}")
    def __sub__(self, other):
        if isinstance(other, Money):
            total = self.total() - other.total()
            return Money(total // 100, total % 100)
        raise ValueError("Cannot subtract {other}")
    def __mul__(self, other):
        if isinstance(other, int):
            total = self.total() * other
            return Money(total // 100, total % 100)
        return ValueError("Cannot multiply by a non-int value")
    def total(self):
        return self.dollars * 100 + self.cents
    @classmethod
    def from_string(cls, amount):
        return cls(*cls.parse(amount))
    @staticmethod
    def parse(amount):
        values = amount.split('.')
        if len(values) == 2:
            dollars, cents = values
            # handle precision
            if len(cents) == 2:
                ...
            elif len(cents) == 1:
                cents += '0'
            else:
                 raise ValueError(f"""
Input string value has too high precision. Input: {cents}"""[1:])
            # handle dollars
            ...
            print(dollars, cents)
            return int(dollars), int(cents)
        raise ValueError(f"String parsing found multiple '.'s. Input: {amount}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        m = Money(3)
        print(m)
        m = Money(53)
        print(m)
    elif sys.argv[1] == '--test':
        import doctest
        doctest.testmod()
    else:
        print("""
basic.py
Usage: python basic.py [--test]"""[1:])

