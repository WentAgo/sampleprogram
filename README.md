# Példaprogram

Ez a program egy egyszerű webshopot modellez, ahol termékeket lehet a kosárba helyezni, majd a fizetési folyamat részeként kedvezményeket és akciós árajánlatokat is lehet alkalmazni.

---

## Fájl struktúra

- **`Product` osztály:** Egy terméket reprezentál, amely tartalmazza a termék nevét és árát.
- **`Cart` osztály:** A kosár kezelésére szolgál, termékek hozzáadását és az árak összesítését végzi.
- **`Checkout` osztály:** A fizetési folyamatot modellezi, kedvezményeket és akciós árajánlatokat kezel.

---

A példaprogram tartalmaz egyszerű, összetett és láncba fűzött metódusokat is.

A példaprogramhoz a tests package-ben található test_main.py-ban vannak tesztek írva.

---

## Kimenet példa

### Kód:
```python
p1 = Product("Pulóver", 5000)
p2 = Product("Nadrág", 7000)
p3 = Product("Cipő", 12000)

cart = Cart()
cart.add_product(p1)
cart.add_product(p2)
cart.add_product(p3)

checkout = Checkout(cart)
print("Teljes ár kedvezmények nélkül:", checkout.calculate_total())
print("Kedvezményes ár (10%):", checkout.process_payment())
print("Akciós ár (20% kedvezmény és bónusz):", checkout.apply_special_offers())
```

### Kimenet:
```
Teljes ár kedvezmények nélkül: 24000
Kedvezményes ár (10%): 21600
Akciós ár (20% kedvezmény és bónusz): 18700
```
