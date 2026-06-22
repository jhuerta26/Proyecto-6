import math
import random
from grafo import Grafo


def _rng(semilla=None):
    return random.Random(semilla)


def malla(n=100, semilla=None):
    grafo = Grafo()
    columnas = max(2, int(math.sqrt(n)))
    filas = math.ceil(n / columnas)
    for i in range(n):
        grafo.agregar_nodo(i)
    for i in range(n):
        fila = i // columnas
        col = i % columnas
        derecha = i + 1
        abajo = i + columnas
        if col + 1 < columnas and derecha < n:
            grafo.agregar_arista(i, derecha)
        if fila + 1 < filas and abajo < n:
            grafo.agregar_arista(i, abajo)
    return grafo


def erdos_renyi(n=100, m=None, semilla=None):
    azar = _rng(semilla)
    grafo = Grafo()
    for i in range(n):
        grafo.agregar_nodo(i)
    if m is None:
        m = max(n - 1, min(n * 3, n * (n - 1) // 2))
    maximo = n * (n - 1) // 2
    m = max(0, min(int(m), maximo))
    intentos = 0
    while grafo.numero_aristas() < m and intentos < maximo * 8:
        u = azar.randrange(n)
        v = azar.randrange(n)
        grafo.agregar_arista(u, v)
        intentos += 1
    return grafo


def gilbert(n=100, p=None, semilla=None):
    azar = _rng(semilla)
    grafo = Grafo()
    for i in range(n):
        grafo.agregar_nodo(i)
    if p is None:
        p = 0.055 if n <= 150 else 0.012
    for i in range(n):
        for j in range(i + 1, n):
            if azar.random() <= p:
                grafo.agregar_arista(i, j)
    return grafo


def geografico(n=100, r=None, semilla=None):
    azar = _rng(semilla)
    grafo = Grafo()
    posiciones = {}
    if r is None:
        r = 0.17 if n <= 150 else 0.075
    for i in range(n):
        grafo.agregar_nodo(i)
        posiciones[str(i)] = (azar.random(), azar.random())
    for i in range(n):
        xi, yi = posiciones[str(i)]
        for j in range(i + 1, n):
            xj, yj = posiciones[str(j)]
            if math.hypot(xj - xi, yj - yi) <= r:
                grafo.agregar_arista(i, j)
    return grafo


def barabasi_albert(n=100, d=None, semilla=None):
    azar = _rng(semilla)
    grafo = Grafo()
    if n <= 0:
        return grafo
    if d is None:
        d = 3
    d = max(1, min(int(d), max(1, n - 1)))
    inicial = min(n, d + 1)
    for i in range(inicial):
        grafo.agregar_nodo(i)
    for i in range(inicial):
        for j in range(i + 1, inicial):
            grafo.agregar_arista(i, j)
    lista_preferencial = []
    for arista in grafo.aristas():
        lista_preferencial.extend([arista.origen, arista.destino])
    for nuevo in range(inicial, n):
        grafo.agregar_nodo(nuevo)
        elegidos = set()
        while len(elegidos) < min(d, nuevo):
            if lista_preferencial:
                candidato = azar.choice(lista_preferencial)
            else:
                candidato = str(azar.randrange(nuevo))
            if candidato != str(nuevo):
                elegidos.add(candidato)
        for destino in elegidos:
            grafo.agregar_arista(nuevo, destino)
            lista_preferencial.extend([str(nuevo), destino])
    return grafo


def dorogovtsev_mendes(n=100, semilla=None):
    azar = _rng(semilla)
    grafo = Grafo()
    if n <= 0:
        return grafo
    for i in range(min(n, 3)):
        grafo.agregar_nodo(i)
    if n >= 2:
        grafo.agregar_arista(0, 1)
    if n >= 3:
        grafo.agregar_arista(1, 2)
        grafo.agregar_arista(2, 0)
    for nuevo in range(3, n):
        arista = azar.choice(grafo.aristas())
        grafo.agregar_nodo(nuevo)
        grafo.agregar_arista(nuevo, arista.origen)
        grafo.agregar_arista(nuevo, arista.destino)
    return grafo


GENERADORES = {
    "malla": malla,
    "erdos_renyi": erdos_renyi,
    "gilbert": gilbert,
    "geografico": geografico,
    "barabasi_albert": barabasi_albert,
    "dorogovtsev_mendes": dorogovtsev_mendes,
}


def generar_grafo(modelo, n, semilla=None):
    if modelo not in GENERADORES:
        disponibles = ", ".join(sorted(GENERADORES))
        raise ValueError(f"Modelo no reconocido: {modelo}. Modelos: {disponibles}")
    return GENERADORES[modelo](n=n, semilla=semilla)
