import typing

from catalog import SupermarketCatalog
from models.products import Product


class FakeCatalog(SupermarketCatalog):
    def __init__(self):
        self.products = {}
        self.prices = {}

    def add_product(self, product: Product, price: float):
        self.products[product.name] = product
        self.prices[product.name] = price

    def unit_price(self, product: Product) -> typing.Dict[str, float]:
        return self.prices[product.name]
