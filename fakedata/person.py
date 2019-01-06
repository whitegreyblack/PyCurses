import random

names_males = set()
names_females = set()
names_males_ordered = []
names_females_ordered = []

with open('./data/NAMES_MALE.txt', 'r') as names_m:
    for line in names_m.readlines():
        names_males.add(line.strip())

with open('./data/NAMES_FEMALE.txt', 'r') as names_f:
    for line in names_f.readlines():
        names_females.add(line.strip())

class Person:
    def __init__(self, name, age, phone, address):
        self.name = name
        self.age = age
        self.phonenumber = phone
        self.address = address

    @classmethod
    def random(cls):
        # TODO: Name.Random(), Age.Random(), Phone.Random(), address.Random()
        #       A random person is still faraway from where the generator is
        #       currently at. We would need at least random name, age and 
        #       phone number to create a basic person object.
        return cls(None, None, None, None)

if __name__ == "__main__":
    print(names_males)
    print(names_females)