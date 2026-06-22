class Viewport:
    def __init__(self, x, y, ancho, alto, margen=12):
        self.x = int(x)
        self.y = int(y)
        self.ancho = int(ancho)
        self.alto = int(alto)
        self.margen = int(margen)
        self.zoom = 1.0
        self.pan_x = 0.0
        self.pan_y = 0.0

    def mapa(self, px, py):
        cx = 0.5 + (px - 0.5) * self.zoom + self.pan_x
        cy = 0.5 + (py - 0.5) * self.zoom + self.pan_y
        sx = self.x + self.margen + cx * (self.ancho - 2 * self.margen)
        sy = self.y + self.margen + cy * (self.alto - 2 * self.margen)
        return int(sx), int(sy)

    def contiene(self, punto):
        px, py = punto
        return self.x <= px <= self.x + self.ancho and self.y <= py <= self.y + self.alto

    def mover_camara(self, dx, dy):
        self.pan_x += dx
        self.pan_y += dy

    def cambiar_zoom(self, factor):
        self.zoom = max(0.25, min(3.0, self.zoom * factor))

    def rect_pygame(self):
        return self.x, self.y, self.ancho, self.alto
