from catalog import SupermarketCatalog
from models.offers import Discount, Offer, SpecialOfferType
from models.products import Product


class ReceiptItem:
    def __init__(
        self, product: Product, quantity: float, price: float, total_price: float
    ) -> None:
        self.product = product
        self.quantity = quantity
        self.price = price
        self.total_price = total_price


class Receipt:
    def __init__(self) -> None:
        self._items = []
        self._discounts = []

    def total_price(self) -> float:
        total: float = 0
        for item in self.items:
            total += item.total_price
        for discount in self.discounts:
            total += discount.discount_amount
        return total

    def add_product(
        self, product: Product, quantity: float, price: float, total_price: float
    ) -> None:
        self._items.append(ReceiptItem(product, quantity, price, total_price))

    def add_discount(self, discount: Discount) -> None:
        self._discounts.append(discount)

    @property
    def items(self) -> list[ReceiptItem]:
        return self._items[:]

    @property
    def discounts(self) -> list[Discount]:
        return self._discounts[:]

    def manage_offer(self, offer: Offer, quantity: float, catalog: SupermarketCatalog):
        discount = None
        if offer.offer_type == SpecialOfferType.THREE_FOR_TWO and quantity > 2:
            discount = offer.three_per_due(quantity, catalog)
        if offer.offer_type == SpecialOfferType.TWO_FOR_AMOUNT and quantity >= 2:
            discount = offer.two_for_amount(quantity, catalog)
        if offer.offer_type == SpecialOfferType.FIVE_FOR_AMOUNT and quantity >= 5:
            discount = offer.five_for_amount(quantity, catalog)
        if offer.offer_type == SpecialOfferType.TEN_PERCENT_DISCOUNT:
            discount = offer.ten_percent(quantity, catalog)
        if discount:
            self.add_discount(discount)
