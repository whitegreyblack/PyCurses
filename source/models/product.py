"""Product Model"""

__author__ = "Samuel Whang"

# import sys
# sys.path.append('..')

from source.utils import Currency

class Product:
    def __init__(self, name: str, price: Currency):
        self.name = name
        self.name_format = '{}'
        self.price = float(price)
        self.price_format = '{:.2f}'

    def __repr__(self):
        return f"{self.__class__.__name__}({self.name}: ${self.price:.2f})"

    @property
    def description(self):
        return self.name, self.price
    
    @property
    def formats(self):
        return self.name_format, self.price_format

    @property
    def format_criteria(self):
        return '{}{}{:.2f}'

if __name__ == "__main__":
    p = Product('example', 123)
    print(p)
