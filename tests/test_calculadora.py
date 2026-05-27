import pytest
from src.calculadora import dividir, calcular_promedio

def test_dividir_normal():
    assert dividir(10, 2) == 5.0

def test_dividir_por_cero():
    with pytest.raises(ZeroDivisionError):
        dividir(10, 0) # calculadora.py actual no maneja esto

def test_promedio_lista_vacia():
    with pytest.raises(ValueError):
        calcular_promedio([]) # calculadora.py actual no maneja esto

def test_promedio_normal():
    assert calcular_promedio([1, 2, 3]) == 2.0