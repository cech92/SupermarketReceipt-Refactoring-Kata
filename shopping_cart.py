import typing

from catalog import SupermarketCatalog
from models.offers import Offer
from models.products import Product, ProductQuantity
from receipt import Receipt


class ShoppingCart:
    def __init__(self) -> None:
        self._items = []
        self._product_quantities = {}

    @property
    def items(self) -> list[ProductQuantity]:
        return self._items

    def add_item(self, product: Product) -> None:
        self.add_item_quantity(product, 1.0)

    @property
    def product_quantities(self) -> typing.Dict[Product, float]:
        return self._product_quantities

    def add_item_quantity(self, product: Product, quantity: float) -> None:
        self._items.append(ProductQuantity(product, quantity))
        if product in self._product_quantities.keys():
            self._product_quantities[product] = (
                self._product_quantities[product] + quantity
            )
        else:
            self._product_quantities[product] = quantity

    def handle_offers(
        self, receipt: Receipt, offers: typing.Dict[Offer], catalog: SupermarketCatalog
    ) -> None:
        for p in self._product_quantities.keys():
            quantity = self._product_quantities[p]
            if p in offers.keys():
                offer = offers[p]
                receipt.manage_offer(offer, quantity, catalog)
