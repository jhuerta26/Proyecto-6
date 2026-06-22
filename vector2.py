import math

EPSILON = 1e-9


def longitud(x, y):
    return math.hypot(x, y)


def normalizar(x, y):
    d = math.hypot(x, y)
    if d < EPSILON:
        return 0.0, 0.0
    return x / d, y / d


def limitar(x, y, maximo):
    d = math.hypot(x, y)
    if d < EPSILON or d <= maximo:
        return x, y
    escala = maximo / d
    return x * escala, y * escala


def acotar(valor, minimo, maximo):
    return max(minimo, min(maximo, valor))
