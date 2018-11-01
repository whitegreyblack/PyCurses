import random
from source.utils import unicode

sample_first_male = [
    "Bob",
    "Robert",
    "william",
    "Bill",
]
sample_first_female = []
sample_middle_male = []
sample_middle_female = []
sample_last = [
    "McGregor",
    "Telrany",
]

class Name:
    def __init__(self, name):
        names = name.split()
        # assume either two or three names given corresponding to a person's
        # first, middle?, last name
        try:
            self.first, self.middle, self.last = names
        except:
            self.first, self.last = names
            self.middle = None
    def __str__(self):
        if self.middle:
            fullname = f"{self.first} {self.middle} {self.last}"
        else:
            fullname = f"{self.first} {self.last}"
        return fullname
    def __repr__(self):
        f, m, l = self.first, self.middle, self.last
        return f"Name(first={f}, middle={m}, last={l})"
    def __lt__(self, other):
        return unicode(self.first) < unicode(other.first)
    @staticmethod
    def random(self):
        if random.randint(0, 1):
            return random


class Contact:
    def __init__(self, name, number, company=None):
        self.name = name
        self.number = number
        self.company = company

    def __repr__(self):
        # don't really need company info during repr
        return f"Contact(name={self.name}, number={self.number})"

if __name__ == "__main__":
    from 