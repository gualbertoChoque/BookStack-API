def sumar(a: int, b: int) -> int:
    return a + b

def test_sumar_basico():
    assert sumar(2, 3) == 5

def test_sumar_cero():
    assert sumar(0, 7) == 7
