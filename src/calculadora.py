def dividir(a, b):
    if b == 0:
        raise ZeroDivisionError("division by zero")
    return a / b

def calcular_promedio(numeros):
    return sum(numeros) / len(numeros)
