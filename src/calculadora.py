def dividir(a, b):
    # nuevos cambios
    if b == 0:
        raise ZeroDivisionError("division by zero")
    return a / b

def calcular_promedio(numeros):
    # mas cambios
    return sum(numeros) / len(numeros)
