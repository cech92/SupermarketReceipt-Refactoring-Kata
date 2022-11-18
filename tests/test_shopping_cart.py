import unittest

from models.products import Product, ProductUnit
from shopping_cart import ShoppingCart


class ShoppingCartTestCase(unittest.TestCase):
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

    def setUp(self) -> None:
        self.shopping_cart = ShoppingCart()

    def test_add_item(self):
        self.shopping_cart.add_item(self.apples)

        self.assertEqual(len(self.shopping_cart.items), 1)
        self.assertEqual(self.shopping_cart.product_quantities[self.apples], 1)

    def test_add_item_quantity(self):
        self.shopping_cart.add_item_quantity(self.toothbrush, 3)

        self.assertEqual(len(self.shopping_cart.items), 1)
        self.assertEqual(self.shopping_cart.product_quantities[self.toothbrush], 3)

        self.shopping_cart.add_item_quantity(self.toothbrush, 2)

        self.assertEqual(len(self.shopping_cart.items), 2)
        self.assertEqual(self.shopping_cart.product_quantities[self.toothbrush], 5)
