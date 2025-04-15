class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price

class Cart:
    def __init__(self):
        self.products = []

    def add_product(self, product):
        self.products.append(product)


    def get_total_price(self):
        return sum([product.price for product in self.products])

class Checkout:
    def __init__(self, cart):
        self.cart = cart

    def calculate_total(self):
        return self.cart.get_total_price()

    def process_payment(self):
        total = self.calculate_total()
        return self._apply_discount(total)

    def _apply_discount(self, total):
        return self._calculate_final_price(total)

    def _calculate_final_price(self, total):
        return total * 0.9

    def apply_special_offers(self):
        discounted_prices = self._get_discounted_prices()
        total_after_discounts = self._calculate_total_after_discounts(discounted_prices)
        final_price = self._finalize_special_offer_price(total_after_discounts)
        return final_price

    def _get_discounted_prices(self):
        discounts = [self._calculate_discount(p.price) for p in self.cart.products]
        return self._apply_discounts_to_products(discounts)

    def _calculate_total_after_discounts(self, discounted_prices):
        return self._sum_discounted_prices(discounted_prices) + self._add_special_offer_bonus()

    def _calculate_discount(self, price):
        return price * 0.8

    def _apply_discounts_to_products(self, discounts):
        return [discount for discount in discounts]

    def _sum_discounted_prices(self, discounted_prices):
        return sum(discounted_prices)

    def _add_special_offer_bonus(self):
        return -499

    def _finalize_special_offer_price(self, total):
        return max(total, 0)

if __name__ == "__main__":
    print("It models a simple webshop where you can add products to your shopping cart and then apply discounts and promotions as part of the checkout process.")
    p1 = Product("Sweater", 5000)
    p2 = Product("Trousers", 7000)
    p3 = Product("Shoes", 12000)

    cart = Cart()
    cart.add_product(p1)
    cart.add_product(p2)
    cart.add_product(p3)

    checkout = Checkout(cart)
    print("Total price without discounts: ", checkout.calculate_total())
    print("Discounted price (10%): ", checkout.process_payment())
    print("Special price (20% discount and bonus): ", checkout.apply_special_offers())