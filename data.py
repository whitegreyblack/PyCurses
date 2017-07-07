from datetime import date

class Data:
    def __init__(self, data):
        self.data = data
        self.size = len(data)
        self.pos = 0

    def __repr__(self):
        return "{}".format(self.__class__.__name__)

class Body:
    def __init__(self, data):
        self.data = data
        self.size = len(data)
        self.pos = 0

    def __repr__(self):
        return "{}".format(self.__class__.__name__)

class RecieptData(Data):
    def __init__(self, data, body=None):
        super().__init__(data)

        self.maxas = self.getMax()
        self.month = self.getMon()
        self.total = self.getTot()

    def scroll_up(self):
        old = self.pos
        self.pos = max(min(self.size-1, self.pos+1), 0)
    
    def scroll_dn(self):
        old = self.pos
        self.pos = max(min(self.size-1, self.pos-1), 0)

    def getMax(self):
        maxa = 0
        for s, _, _, _, _, _, _ in self.data:
            if len(s) > maxa: maxa = len(s)
        return maxa

    def getMon(self):
        months = {}
        for _, c, _, _, _, _, t in self.data:
            y, m, d = c.split('-')
            getDate = date(int(y), int(m), int(d))
            if getDate.month in months.keys():
                months[getDate.month] += t
            else:
                months[getDate.month] = t
        return [[month, months[month]] for month in months.keys()]

    def getTot(self):
        return int(sum([t for _, _, _, _, _, _, t in self.data])*100)/100