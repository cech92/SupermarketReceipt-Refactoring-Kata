from enum import Enum

from catalog import SupermarketCatalog
from models.products import Product, ProductQuantity


class Bundle:
    def __init__(
        self, product_quantities: list[ProductQuantity], discount: float
    ) -> None:
        self.product_quantities = product_quantities
        self.discount = discount


class SpecialOfferType(Enum):
    THREE_FOR_TWO = 1
    TEN_PERCENT_DISCOUNT = 2
    TWO_FOR_AMOUNT = 3
    FIVE_FOR_AMOUNT = 4


class Offer:
    def __init__(
        self, offer_type: SpecialOfferType, product: Product, argument: float
    ) -> None:
        self.offer_type = offer_type
        self.product = product
        self.argument = argument

    def three_per_due(self, quantity: float, catalog: SupermarketCatalog):
        unit_price = catalog.unit_price(self.product)
        quotient = quantity // 3
        discount_amount = quantity * unit_price - (
            (quotient * 2 * unit_price) + quantity % 3 * unit_price
        )
        return Discount(self.product, "3 for 2", -discount_amount)

    def two_for_amount(self, quantity: float, catalog: SupermarketCatalog):
        unit_price = catalog.unit_price(self.product)
        total = self.argument * (quantity // 2) + quantity % 2 * unit_price
        discount_n = unit_price * quantity - total
        return Discount(self.product, "2 for " + str(self.argument), -discount_n)

    def five_for_amount(self, quantity: float, catalog: SupermarketCatalog):
        unit_price = catalog.unit_price(self.product)
        quotient = quantity // 5
        discount_total = unit_price * quantity - (
            self.argument * quotient + quantity % 5 * unit_price
        )
        return Discount(self.product, "5 for " + str(self.argument), -discount_total)

    def ten_percent(self, quantity: float, catalog: SupermarketCatalog):
        unit_price = catalog.unit_price(self.product)
        return Discount(
            self.product,
            str(self.argument) + "% off",
            -quantity * unit_price * self.argument / 100.0,
        )


class Discount:
    def __init__(
        self, product: Product, description: str, discount_amount: float
    ) -> None:
        self.product = product
        self.description = description
        self.discount_amount = discount_amount
