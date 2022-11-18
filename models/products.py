from enum import Enum


class ProductUnit(Enum):
    EACH = 1
    KILO = 2


class Product:
    def __init__(self, name: str, unit: ProductUnit) -> None:
        self.name = name
        self.unit = unit


class ProductQuantity:
    def __init__(self, product: Product, quantity: float) -> None:
        self.product = product
        self.quantity = quantity
