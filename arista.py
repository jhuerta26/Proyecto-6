class Arista:
    def __init__(self, origen, destino, peso=1.0):
        self.origen = str(origen)
        self.destino = str(destino)
        self.peso = float(peso)

    def como_tupla(self):
        return self.origen, self.destino

    def __str__(self):
        return f"{self.origen} -- {self.destino} ({self.peso:g})"

    def __repr__(self):
        return f"Arista({self.origen!r}, {self.destino!r}, peso={self.peso!r})"

    def __eq__(self, otra):
        if not isinstance(otra, Arista):
            return False
        return frozenset((self.origen, self.destino)) == frozenset((otra.origen, otra.destino))

    def __hash__(self):
        return hash(frozenset((self.origen, self.destino)))
