from arista import Arista
from nodo import Nodo


class Grafo:
    def __init__(self):
        self.nodos = {}
        self._aristas = {}
        self._adyacencia = {}

    def agregar_nodo(self, etiqueta):
        etiqueta = str(etiqueta)
        if etiqueta not in self.nodos:
            self.nodos[etiqueta] = Nodo(etiqueta)
            self._adyacencia[etiqueta] = set()
        return self.nodos[etiqueta]

    def agregar_arista(self, origen, destino, peso=1.0):
        origen = str(origen)
        destino = str(destino)
        if origen == destino:
            return None
        self.agregar_nodo(origen)
        self.agregar_nodo(destino)
        llave = frozenset((origen, destino))
        if llave in self._aristas:
            return self._aristas[llave]
        arista = Arista(origen, destino, peso)
        self._aristas[llave] = arista
        self._adyacencia[origen].add(destino)
        self._adyacencia[destino].add(origen)
        return arista

    def etiquetas(self):
        return list(self.nodos.keys())

    def aristas(self):
        return list(self._aristas.values())

    def vecinos(self, etiqueta):
        return set(self._adyacencia.get(str(etiqueta), set()))

    def grado(self, etiqueta):
        return len(self._adyacencia.get(str(etiqueta), set()))

    def numero_nodos(self):
        return len(self.nodos)

    def numero_aristas(self):
        return len(self._aristas)

    def limpiar(self):
        self.nodos.clear()
        self._aristas.clear()
        self._adyacencia.clear()

    def __str__(self):
        return f"Grafo(nodos={self.numero_nodos()}, aristas={self.numero_aristas()})"
