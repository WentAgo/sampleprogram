# Sample program

It models a simple webshop where you can add products to your shopping cart and then apply discounts and promotions as part of the checkout process.

---

## File structure

- **`Product` class:** Represents a product, containing the product name and price.
- **`Cart` class:** Used to manage the cart, add products and aggregate prices.
- **`Checkout` class:** Models the checkout process, handles discounts and promotions.

The example program includes simple, complex and chained methods.

Tests are written for the example program in test_main.py in the tests package.

---

## Output example

### Code:
```python
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
```

### Output:
```
Total price without discounts:  24000
Discounted price (10%):  21600.0
Special price (20% discount and bonus):  18700.0
```
