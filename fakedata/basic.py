"""Basic generators"""
import random

class Money(float):
    def __init__(self, amount):
        self = amount
    def __str__(self):
        return f"${self:0.2f}"
    def __repr__(self):
        return f"Money(amount={self}"
    def __add__(self, other):
        pass

class Age(int):
    def __init__(self, years):
        self = years

    @classmethod
    def random(cls, low=1, high=100):
        return cls(random.randint(low, high))

if __name__ == "__main__":
    m = Money(3)
    print(m)
    m = Money(53)
    print(m)