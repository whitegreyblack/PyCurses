"""Basic generators"""
import random

class Age(int):
    def __init__(self, age):
        self = age

    @classmethod
    def random(cls, low=1, high=100):
        return cls(random.randint(low, high))
