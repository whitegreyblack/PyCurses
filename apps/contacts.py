from source.utils import unicode

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

class Contact:
    def __init__(self, name, number, company=None):
        self.name = name
        self.number = number
        self.company = company

    def __repr__(self):
        # don't really need company info during repr
        return f"Contact(name={self.name}, number={self.number})"