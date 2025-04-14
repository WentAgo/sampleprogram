from main import Product, Cart, Checkout


def test_product_creation():
    p = Product("Jacket", 15000)
    assert p.name == "Jacket"
    assert p.price == 15000


def test_cart_add_product():
    cart = Cart()
    p1 = Product("Sweater", 5000)
    p2 = Product("Trousers", 7000)
    cart.add_product(p1)
    cart.add_product(p2)
    assert len(cart.products) == 2
    assert cart.products[0].name == "Sweater"
    assert cart.products[1].name == "Trousers"


def test_cart_get_total_price():
    cart = Cart()
    cart.add_product(Product("Sweater", 5000))
    cart.add_product(Product("Trousers", 7000))
    assert cart.get_total_price() == 12000


def test_checkout_calculate_total():
    cart = Cart()
    cart.add_product(Product("Sweater", 5000))
    cart.add_product(Product("Trousers", 7000))
    checkout = Checkout(cart)
    assert checkout.calculate_total() == 12000


def test_checkout_process_payment():
    cart = Cart()
    cart.add_product(Product("Sweater", 5000))
    cart.add_product(Product("Trousers", 7000))
    checkout = Checkout(cart)
    final_price = checkout.process_payment()
    assert final_price == 10800


def test_checkout_apply_special_offers():
    cart = Cart()
    cart.add_product(Product("Sweater", 5000))
    cart.add_product(Product("Trousers", 7000))
    checkout = Checkout(cart)
    special_offer_price = checkout.apply_special_offers()
    assert special_offer_price == 9100, "The discount price calculation is incorrect!"


if __name__ == "__main__":
    test_product_creation()
    test_cart_add_product()
    test_cart_get_total_price()
    test_checkout_calculate_total()
    test_checkout_process_payment()
    test_checkout_apply_special_offers()
    print("All tests passed successfully!")
