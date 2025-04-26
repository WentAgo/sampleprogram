from calculator import Calculator
def test_calculator():
    calc = Calculator()
    a = calc.add(1,1)
    b = calc.multiply(a,3)
    assert a + b == 8

def test_add():
    calc = Calculator()
    a = calc.add(1,2)
    b = calc.square (2)
    assert calc.add(a,b) == 7

def test_square():
    calc = Calculator()
    assert calc.square(3) == 9
def test_add_two_two():
    calc = Calculator()
    assert calc.add(2, 2) == 4

def test_multiply_zero_zero():
    calc = Calculator()
    assert calc.multiply(0,0) == 0

def test_multiply_zero_six():
    calc = Calculator()
    assert calc.multiply(0,6) == 0

def test_multiply_zero_seven():
    calc = Calculator()
    assert calc.multiply(0, 7) == 0