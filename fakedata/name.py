import random

def read_file(dataset):
    container = []
    with open(f'./data/{dataset}.txt', 'r') as data:
        for line in data.readlines():
            container.append(line.strip())
    return container, set(container)

names_last_ordered, names_last = read_file('NAMES_LAST')
names_males_ordered, names_males = read_file('NAMES_MALE')
names_females_ordered, names_females = read_file('NAMES_FEMALE')
# names_males_prefix = set()
# names_males_suffix = set()
# names_females_prefix = set()
# names_females_suffix = set()

# names_males_prefix_ordered = []
# names_males_suffix_ordered = []
# names_females_prefix_ordered = []
# names_females_suffix_ordered = []

# with open('./data/NAMES_MALE.txt', 'r') as names_m:
#     for line in names_m.readlines():
#         names_males.add(line.strip())

# with open('./data/NAMES_FEMALE.txt', 'r') as names_f:
#     for line in names_f.readlines():
#         names_females.add(line.strip())

# with open('./data/NAMES_LAST.txt', 'r') as names_l:
#     for line in names_l.readlines():
#         names_last.add(line.strip())

class Name:
    names_last = names_last_ordered
    names_males = names_males_ordered
    names_females = names_females_ordered
    names_females_prefix = ('Dr.', 'Mrs.', 'Miss', 'Ms.')
    names_females_suffix = ('M.D.', 'Phd.')
    formats = (
        # ('male', ('prefix', 'first', 'last', 'suffix')),
        # ('male', ('prefix', 'first', 'last')),
        # ('male', ('first', 'last', 'suffix')),
        # ('male', ('first', 'last')),
        ('female', 'prefix first last suffix'),
        ('female', 'prefix first last'),
        ('female', 'prefix first last'),
        ('female', 'prefix first last'),
        ('female', 'first last suffix'),
        ('female', 'first last'),
        ('female', 'first last'),
        ('female', 'first last'),
        ('female', 'first last'),
    )
    def __init__(self, first=None, last=None, prefix=None, suffix=None):
        self.name_first = first if first else ''
        self.name_last = last if last else ''
        self.name_prefix = prefix if prefix else ''
        self.name_suffix = suffix if suffix else ''

    def __str__(self):
        p = self.name_prefix
        f = self.name_first
        l = self.name_last
        s = self.name_suffix
        return f"{p}{' ' if p else ''}{f} {l}{' ' if s else ''}{s}"

    def prefix(self, gender):
        if gender == "male":
            return male_prefix()
        return self.female_prefix()

    def first(self, gender):
        if gender == "male":
            return male_first()
        return self.female_first()
    
    def last(self, gender):
        if gender == "male":
            return male_last()
        return self.female_last()

    def suffix(self, gender):
        if gender == "male":
            return male_suffix()
        return self.female_suffix()

    def male_prefix(self):
        if hasattr(self, 'male_prefixes'):
            return random.choice(self.male_prefixes)
        return ''

    def female_prefix(self):
        if hasattr(self, 'names_females_prefix'):
            return random.choice(self.names_females_prefix)
        return ''

    def female_first(self):
        if hasattr(self, 'names_females'):
            return random.choice(self.names_females)
        return random.choice(self.names_first)

    def female_last(self):
        if hasattr(self, 'names_females_last'):
            return random.choice(self.female_last)
        return random.choice(self.names_last)
    
    def female_suffix(self):
        if hasattr(self, 'names_females_suffix'):
            return random.choice(self.names_females_suffix)
        return ''

    @classmethod
    def random(cls, formats=None):
        p = cls()
        if not formats:
            formats = cls.formats
        gender, choices = random.choice(formats)
        for choice in choices.split():
            attr = getattr(p, choice)(gender)
            setattr(p, 'name_' + choice, attr)
        return p

if __name__ == "__main__":
    print(Name.random((('female', 'first last'),)))