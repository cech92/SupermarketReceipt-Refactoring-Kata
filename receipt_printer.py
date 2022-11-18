from models.offers import Discount
from models.products import ProductUnit
from receipt import Receipt, ReceiptItem


class ReceiptPrinter:
    def __init__(self, columns: int = 40) -> None:
        self.columns = columns

    def print_receipt(self, receipt: Receipt) -> str:
        result = ""
        for item in receipt.items:
            receipt_item = self.print_receipt_item(item)
            result += receipt_item

        for discount in receipt.discounts:
            discount_presentation = self.print_discount(discount)
            result += discount_presentation

        result += "\n"
        result += self.present_total(receipt)
        return str(result)

    def print_receipt_item(self, item: ReceiptItem) -> str:
        total_price_printed = self.print_price(item.total_price)
        name = item.product.name
        line = self.format_line_with_whitespace(name, total_price_printed)
        if item.quantity != 1:
            line += f"  {self.print_price(item.price)} * {self.print_quantity(item)}\n"
        return line

    def format_line_with_whitespace(self, name: str, value: str) -> str:
        line: str = name
        whitespace_size = self.columns - len(name) - len(value)
        for _ in range(whitespace_size):
            line += " "
        line += value
        line += "\n"
        return line

    @staticmethod
    def print_price(price: float) -> str:
        return "%.2f" % price

    @staticmethod
    def print_quantity(item: ReceiptItem) -> str:
        if ProductUnit.EACH == item.product.unit:
            return str(item.quantity)
        else:
            return "%.3f" % item.quantity

    def print_discount(self, discount: Discount) -> str:
        name = f"{discount.description} ({discount.product.name})"
        value = self.print_price(discount.discount_amount)
        return self.format_line_with_whitespace(name, value)

    def present_total(self, receipt: Receipt) -> str:
        name = "Total: "
        value = self.print_price(receipt.total_price())
        return self.format_line_with_whitespace(name, value)
