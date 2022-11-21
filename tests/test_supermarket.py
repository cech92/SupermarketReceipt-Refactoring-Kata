import unittest

import ddt

from models.offers import SpecialOfferType
from models.products import Product, ProductQuantity, ProductUnit
from shopping_cart import ShoppingCart
from teller import Teller
from tests.fake_catalog import FakeCatalog


@ddt.ddt
class SupermarketTestCase(unittest.TestCase):
    catalog: FakeCatalog | None = None
    teller: Teller | None = None
    shopping_cart: ShoppingCart | None = None
    product_prices: list[(Product, float)] = []

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

    @classmethod
    def setUpClass(cls) -> None:
        cls.catalog = FakeCatalog()

        cls.catalog.add_product(product=cls.toothbrush, price=cls.toothbrush_price)
        cls.catalog.add_product(product=cls.apples, price=cls.apples_price)
        cls.catalog.add_product(product=cls.rice, price=cls.rice_price)
        cls.catalog.add_product(product=cls.toothpaste, price=cls.toothpaste_price)
        cls.catalog.add_product(
            product=cls.cherry_tomatoes, price=cls.cherry_tomatoes_price
        )

    def setUp(self) -> None:
        self.shopping_cart = ShoppingCart()
        self.teller = Teller(self.catalog)

    @ddt.data(3, 5, 8, 9)
    def test_three_for_two_discount(self, quantity):
        quotient = quantity // 3
        self.teller.add_special_offer(
            SpecialOfferType.THREE_FOR_TWO, self.toothbrush, None
        )

        self.shopping_cart.add_item_quantity(self.toothbrush, quantity)
        receipt = self.teller.checks_out_articles_from(self.shopping_cart)

        self.assertEqual(len(receipt.items), 1)
        self.assertEqual(len(receipt.discounts), 1)

        discount = receipt.discounts[0]
        self.assertEqual(discount.product, self.toothbrush)
        self.assertEqual(discount.description, "3 for 2")
        self.assertAlmostEqual(
            discount.discount_amount, -self.toothbrush_price * quotient
        )

        receipt_item = receipt.items[0]
        self.assertEqual(receipt_item.product, self.toothbrush)
        self.assertEqual(receipt_item.price, self.toothbrush_price)
        self.assertAlmostEqual(
            receipt_item.total_price, quantity * self.toothbrush_price
        )
        self.assertEqual(receipt_item.quantity, quantity)

    def test_three_for_two_discount_not_apply_lower_quantity(self):
        toothbrush_quantity = 2
        self.teller.add_special_offer(
            SpecialOfferType.THREE_FOR_TWO, self.toothbrush, None
        )

        self.shopping_cart.add_item_quantity(self.toothbrush, toothbrush_quantity)
        receipt = self.teller.checks_out_articles_from(self.shopping_cart)

        self.assertEqual(len(receipt.items), 1)
        self.assertEqual(len(receipt.discounts), 0)

        receipt_item = receipt.items[0]
        self.assertEqual(receipt_item.product, self.toothbrush)
        self.assertEqual(receipt_item.price, self.toothbrush_price)
        self.assertAlmostEqual(
            receipt_item.total_price, toothbrush_quantity * self.toothbrush_price
        )
        self.assertEqual(receipt_item.quantity, toothbrush_quantity)

    def test_three_for_two_discount_not_apply_different_product(self):
        product_quantity = 3
        self.teller.add_special_offer(
            SpecialOfferType.THREE_FOR_TWO, self.toothbrush, None
        )

        self.shopping_cart.add_item_quantity(self.apples, product_quantity)
        receipt = self.teller.checks_out_articles_from(self.shopping_cart)

        self.assertEqual(len(receipt.items), 1)
        self.assertEqual(len(receipt.discounts), 0)

        receipt_item = receipt.items[0]
        self.assertEqual(receipt_item.product, self.apples)
        self.assertEqual(receipt_item.price, self.apples_price)
        self.assertAlmostEqual(
            receipt_item.total_price, product_quantity * self.apples_price
        )
        self.assertEqual(receipt_item.quantity, product_quantity)

    def test_ten_percent_discount(self):
        discount_percentage = 10
        quantity = 10
        self.teller.add_special_offer(
            SpecialOfferType.TEN_PERCENT_DISCOUNT, self.rice, discount_percentage
        )

        self.shopping_cart.add_item_quantity(self.rice, quantity)
        receipt = self.teller.checks_out_articles_from(self.shopping_cart)

        self.assertEqual(len(receipt.items), 1)
        self.assertEqual(len(receipt.discounts), 1)

        discount = receipt.discounts[0]
        self.assertEqual(discount.product, self.rice)
        self.assertEqual(discount.description, f"{discount_percentage}% off")
        self.assertAlmostEqual(
            discount.discount_amount,
            -self.rice_price * discount_percentage / 100 * quantity,
        )

        receipt_item = receipt.items[0]
        self.assertEqual(receipt_item.product, self.rice)
        self.assertEqual(receipt_item.price, self.rice_price)
        self.assertAlmostEqual(receipt_item.total_price, quantity * self.rice_price)
        self.assertEqual(receipt_item.quantity, quantity)

    def test_ten_percent_discount_not_apply_different_product(self):
        discount_percentage = 10
        quantity = 10
        self.teller.add_special_offer(
            SpecialOfferType.TEN_PERCENT_DISCOUNT, self.rice, discount_percentage
        )

        self.shopping_cart.add_item_quantity(self.apples, quantity)
        receipt = self.teller.checks_out_articles_from(self.shopping_cart)

        self.assertEqual(len(receipt.items), 1)
        self.assertEqual(len(receipt.discounts), 0)

        receipt_item = receipt.items[0]
        self.assertEqual(receipt_item.product, self.apples)
        self.assertEqual(receipt_item.price, self.apples_price)
        self.assertAlmostEqual(receipt_item.total_price, quantity * self.apples_price)
        self.assertEqual(receipt_item.quantity, quantity)

    @ddt.data(5, 7, 10, 12)
    def test_five_for_amount_discount(self, quantity):
        fixed_price = 7.49
        quotient = quantity // 5

        self.teller.add_special_offer(
            SpecialOfferType.FIVE_FOR_AMOUNT, self.toothpaste, fixed_price
        )

        self.shopping_cart.add_item_quantity(self.toothpaste, quantity)
        receipt = self.teller.checks_out_articles_from(self.shopping_cart)

        self.assertEqual(len(receipt.items), 1)
        self.assertEqual(len(receipt.discounts), 1)

        discount = receipt.discounts[0]
        self.assertEqual(discount.product, self.toothpaste)
        self.assertEqual(discount.description, f"5 for {fixed_price}")
        self.assertAlmostEqual(
            discount.discount_amount,
            -5 * quotient * self.toothpaste_price + (fixed_price * quotient),
        )

        receipt_item = receipt.items[0]
        self.assertEqual(receipt_item.product, self.toothpaste)
        self.assertEqual(receipt_item.price, self.toothpaste_price)
        self.assertAlmostEqual(
            receipt_item.total_price, quantity * self.toothpaste_price
        )
        self.assertEqual(receipt_item.quantity, quantity)

    @ddt.data(2, 3, 9, 12)
    def test_two_for_amount_discount(self, quantity):
        fixed_price = 0.99
        quotient = quantity // 2

        self.teller.add_special_offer(
            SpecialOfferType.TWO_FOR_AMOUNT, self.cherry_tomatoes, fixed_price
        )

        self.shopping_cart.add_item_quantity(self.cherry_tomatoes, quantity)
        receipt = self.teller.checks_out_articles_from(self.shopping_cart)

        self.assertEqual(len(receipt.items), 1)
        self.assertEqual(len(receipt.discounts), 1)

        discount = receipt.discounts[0]
        self.assertEqual(discount.product, self.cherry_tomatoes)
        self.assertEqual(discount.description, f"2 for {fixed_price}")
        self.assertAlmostEqual(
            discount.discount_amount,
            -2 * quotient * self.cherry_tomatoes_price + (fixed_price * quotient),
        )

        receipt_item = receipt.items[0]
        self.assertEqual(receipt_item.product, self.cherry_tomatoes)
        self.assertEqual(receipt_item.price, self.cherry_tomatoes_price)
        self.assertAlmostEqual(
            receipt_item.total_price, quantity * self.cherry_tomatoes_price
        )
        self.assertEqual(receipt_item.quantity, quantity)

    @ddt.data((2, 1), (3, 1), (4, 2), (4, 3))
    def test_bundle_ten_percent_discount(self, quantities):
        discount_percentage = 10

        product_quantities = [
            ProductQuantity(product=self.toothbrush, quantity=2),
            ProductQuantity(product=self.toothpaste, quantity=1),
        ]
        self.teller.add_bundle_offer(
            offer_type=SpecialOfferType.TEN_PERCENT_DISCOUNT,
            product_quantities=product_quantities,
            argument=discount_percentage,
        )

        self.shopping_cart.add_item_quantity(self.toothbrush, quantity=quantities[0])
        self.shopping_cart.add_item_quantity(self.toothpaste, quantity=quantities[1])
        receipt = self.teller.checks_out_articles_from(self.shopping_cart)

        min_mult = min(quantities[0] // 2, quantities[1] // 1)

        self.assertEqual(len(receipt.items), 2)
        self.assertEqual(len(receipt.discounts), 2)

        discounts = receipt.discounts
        self.assertEqual(discounts[0].product, self.toothbrush)
        self.assertEqual(discounts[0].description, f"{discount_percentage}% off")
        self.assertAlmostEqual(
            discounts[0].discount_amount,
            -self.toothbrush_price * discount_percentage / 100 * min_mult * 2,
        )
        self.assertEqual(discounts[1].product, self.toothpaste)
        self.assertEqual(discounts[1].description, f"{discount_percentage}% off")
        self.assertAlmostEqual(
            discounts[1].discount_amount,
            -self.toothpaste_price * discount_percentage / 100 * min_mult * 1,
        )

        receipt_items = receipt.items
        self.assertEqual(receipt_items[0].product, self.toothbrush)
        self.assertEqual(receipt_items[0].price, self.toothbrush_price)
        self.assertAlmostEqual(
            receipt_items[0].total_price, quantities[0] * self.toothbrush_price
        )
        self.assertEqual(receipt_items[0].quantity, quantities[0])
        self.assertEqual(receipt_items[1].product, self.toothpaste)
        self.assertEqual(receipt_items[1].price, self.toothpaste_price)
        self.assertAlmostEqual(
            receipt_items[1].total_price, quantities[1] * self.toothpaste_price
        )
        self.assertEqual(receipt_items[1].quantity, quantities[1])

    def test_bundle_ten_percent_discount_not_apply_incompleted(self):
        discount_percentage = 10

        product_quantities = [
            ProductQuantity(product=self.toothbrush, quantity=2),
            ProductQuantity(product=self.toothpaste, quantity=1),
        ]
        self.teller.add_bundle_offer(
            offer_type=SpecialOfferType.TEN_PERCENT_DISCOUNT,
            product_quantities=product_quantities,
            argument=discount_percentage,
        )

        self.shopping_cart.add_item_quantity(self.toothbrush, quantity=1)
        self.shopping_cart.add_item_quantity(self.toothpaste, quantity=1)
        receipt = self.teller.checks_out_articles_from(self.shopping_cart)

        self.assertEqual(len(receipt.items), 2)
        self.assertEqual(len(receipt.discounts), 0)

        receipt_items = receipt.items
        self.assertEqual(receipt_items[0].product, self.toothbrush)
        self.assertEqual(receipt_items[0].price, self.toothbrush_price)
        self.assertAlmostEqual(receipt_items[0].total_price, 1 * self.toothbrush_price)
        self.assertEqual(receipt_items[0].quantity, 1)
        self.assertEqual(receipt_items[1].product, self.toothpaste)
        self.assertEqual(receipt_items[1].price, self.toothpaste_price)
        self.assertAlmostEqual(receipt_items[1].total_price, 1 * self.toothpaste_price)
        self.assertEqual(receipt_items[1].quantity, 1)
