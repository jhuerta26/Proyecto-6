class Nodo:
    def __init__(self, etiqueta):
        self.etiqueta = str(etiqueta)

    def __str__(self):
        return self.etiqueta

    def __repr__(self):
        return f"Nodo({self.etiqueta!r})"

    def __eq__(self, otro):
        return isinstance(otro, Nodo) and self.etiqueta == otro.etiqueta

    def __hash__(self):
        return hash(self.etiqueta)
