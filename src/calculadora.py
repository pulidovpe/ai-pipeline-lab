def dividir(a, b):
  if b == 0:
    raise ZeroDivisionError("No se puede dividir por cero")
  return a / b

def calcular_promedio(numeros):
  if len(numeros) == 0:
    raise ValueError("No se puede calcular el promedio de una lista vacia")
  return sum(numeros) / len(numeros)
