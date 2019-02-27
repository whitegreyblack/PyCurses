"""data.py: data objects"""
from collections import namedtuple

product_info = namedtuple("Product_info", "quantity size price")

class Product(object):
    product_name = "Placeholder Product Name"
    def __init__(self, product_name, product_info=None):
        self.product_name = product_name

class Company(object):
    company_name = "Placeholder Company Name"
    def __init__(self, company_name, products=None):
        self.company_name = company_name
        self.products = []
    def add_product(self, product):
        self.products.append(product)
    def add_products(self, products):
        self.products.extend(products)

if __name__ == "__main__":
    d = Company("Comp Name")
    print(d.company_name)
    print(d.products)
