import unittest

from models.offers import Discount
from models.products import Product, ProductUnit
from receipt import Receipt


class ReceiptTestCase(unittest.TestCase):
    receipt: Receipt | None = None

    toothbrush = Product("toothbrush", ProductUnit.EACH)
    toothbrush_price = 0.99

    apples = Product("apples", ProductUnit.KILO)
    apples_price = 1.99

    rice = Product("rice", ProductUnit.EACH)
    rice_price = 2.49

    toothpaste = Product("toothpaste", ProductUnit.EACH)
    toothpaste_price = 1.79

    cherry_tomatoes = Product("cherry_tomatoes", ProductUnit.EACH)
    cherry_tomatoes_price = 0.69

    def setUp(self) -> None:
        self.receipt = Receipt()

    def test_add_product(self):
        quantity = 2
        self.receipt.add_product(
            product=self.apples,
            quantity=quantity,
            price=self.apples_price,
            total_price=quantity * self.apples_price,
        )

        self.assertEqual(len(self.receipt.items), 1)
        self.assertEqual(self.receipt.items[0].product, self.apples)

    def test_add_discount(self):
        discount = Discount(
            product=self.apples, description="Test discount", discount_amount=-1.50
        )
        self.receipt.add_discount(discount)

        self.assertEqual(len(self.receipt.discounts), 1)
        self.assertEqual(self.receipt.discounts[0].product, self.apples)
        self.assertEqual(
            self.receipt.discounts[0].discount_amount, discount.discount_amount
        )

    def test_add_discounts(self):
        discounts = [
            Discount(
                product=self.apples, description="Test apples", discount_amount=-1.50
            ),
            Discount(
                product=self.toothbrush,
                description="Test toothbrush",
                discount_amount=-0.50,
            ),
            Discount(product=self.rice, description="Test rice", discount_amount=-0.20),
        ]
        self.receipt.add_discounts(discounts)

        self.assertEqual(len(self.receipt.discounts), 3)
        self.assertEqual(self.receipt.discounts[0].product, self.apples)
        self.assertEqual(
            self.receipt.discounts[0].discount_amount, discounts[0].discount_amount
        )

    def test_total_price(self):
        apples_quantity = 5

        discount = Discount(
            product=self.apples, description="Test discount", discount_amount=-1.50
        )

        self.receipt.add_product(
            product=self.apples,
            quantity=apples_quantity,
            price=self.apples_price,
            total_price=apples_quantity * self.apples_price,
        )
        self.receipt.add_discount(discount)

        self.assertEqual(
            self.receipt.total_price(),
            apples_quantity * self.apples_price + discount.discount_amount,
        )
