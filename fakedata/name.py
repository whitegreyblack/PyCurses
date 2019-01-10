import random

SHORT_FEMALE_NAME_SCHEMA = {'female': [{'format': 'first last', 'count': 1}]}
SHORT_MALE_NAME_SCHEMA = {'male': [{'format': 'first last', 'count': 1}]}
SHORT_NAME_SCHEMA = {**SHORT_FEMALE_NAME_SCHEMA, **SHORT_MALE_NAME_SCHEMA}

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
    names_prefix = ('Dr.',)
    names_males_prefix = ('Mr.', 'Sir',)
    names_females_prefix = ('Mrs.', 'Miss', 'Ms.')
    names_males_suffix = ('I', 'II', 'III', 'IV', 'Jr.', 'Sr.')
    names_suffix = ('M.D.', 'Phd.')
    # number of occurrances increases change of patter being generated
    formats = {
        'male': [
            {'format': 'prefix first last suffix', 'count': 1},
            {'format': 'prefix first last', 'count': 2},
            {'format': 'first last suffix', 'count': 2},
            {'format': 'first last suffix', 'count': 4}
        ],
        'female': [
            {'format': 'prefix first last suffix', 'count': 1},
            {'format': 'prefix first last', 'count': 2},
            {'format': 'first last suffix', 'count': 2},
            {'format': 'first last suffix', 'count': 4}
        ]
        
    }
    formats = (
        ('male', 'prefix first last suffix'),
        ('male', 'prefix first last'),
        ('male', 'prefix first last'),
        ('male', 'prefix first last'),
        ('male', 'first last suffix'),
        ('male', 'first last'),
        ('male', 'first last'),
        ('male', 'first last'),
        ('male', 'first last'),
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
            return self.male_first()
        return self.female_first()
    
    def last(self, gender):
        if gender == "male":
            return self.male_last()
        return self.female_last()

    def suffix(self, gender):
        if gender == "male":
            return male_suffix()
        return self.female_suffix()

    def male_prefix(self):
        if hasattr(self, 'male_prefixes'):
            return random.choice(self.male_prefixes)
        return ''

    def male_first(self):
        if hasattr(self, 'names_males'):
            return random.choice(self.names_females)
        return random.choice(self.names_first)

    def male_last(self):
        if hasattr(self, 'names_males_last'):
            return random.choice(self.male_last)
        return random.choice(self.names_last)

    def male_suffix(self):
        if hasattr(self, 'names_males_suffix'):
            return random.choice(self.male_suffix)
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
        s = self.names_suffix
        if hasattr(self, 'names_females_suffix'):
            s = self.names_females_suffix
        return random.choice(s)

    @classmethod
    def random(cls, formats=None):
        p = cls()
        if not formats:
            formats = cls.formats
        
        # generate formats
        generate = []
        for gender, data in formats.items():
            for d in data:
                frmt = d['format']
                for _ in range(d['count']):
                    generate.append((gender, frmt))

        gender, choices = random.choice(generate)

        for choice in choices.split():
            attr = getattr(p, choice)(gender)
            setattr(p, 'name_' + choice, attr)

        return p

if __name__ == "__main__":
    print(Name.random(SHORT_FEMALE_NAME_SCHEMA))
    print(Name.random(SHORT_MALE_NAME_SCHEMA))