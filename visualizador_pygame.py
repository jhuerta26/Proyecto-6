import os
import time
import pygame
from exportador import guardar_captura
from viewport import Viewport

FONDO = (13, 16, 18)
BORDE = (170, 180, 190)
BORDE_ACTIVO = (255, 255, 255)
TEXTO = (238, 238, 238)
ARISTA = (190, 198, 208)
ARISTA_VERDE = (63, 210, 93)
NODO_ROJO = (255, 55, 30)
NODO_NARANJA = (255, 132, 0)
NODO_AMARILLO = (255, 220, 0)
NODO_VERDE = (78, 255, 86)
QUADTREE = (84, 190, 84)


class PanelLayout:
    def __init__(self, titulo, grafo, layout, mostrar_quadtree=False):
        self.titulo = titulo
        self.grafo = grafo
        self.layout = layout
        self.mostrar_quadtree = mostrar_quadtree

    def paso(self, pasos_por_frame):
        for _ in range(pasos_por_frame):
            self.layout.paso()


def _color_nodo(grado):
    if grado <= 1:
        return NODO_ROJO
    if grado <= 3:
        return NODO_NARANJA
    if grado <= 6:
        return NODO_AMARILLO
    return NODO_VERDE


def _dibujar_texto(superficie, fuente, texto, x, y, color=TEXTO):
    superficie.blit(fuente.render(texto, True, color), (x, y))


def _dibujar_quadtree(superficie, viewport, layout):
    quadtree = getattr(layout, "quadtree", None)
    if quadtree is None:
        return
    for x, y, ancho, profundidad in quadtree.rectangulos(limite_profundidad=6):
        x1, y1 = viewport.mapa(x, y)
        x2, y2 = viewport.mapa(x + ancho, y + ancho)
        rx = min(x1, x2)
        ry = min(y1, y2)
        rw = abs(x2 - x1)
        rh = abs(y2 - y1)
        if rw > 2 and rh > 2:
            intensidad = max(40, 160 - profundidad * 16)
            pygame.draw.rect(superficie, (45, intensidad, 45), (rx, ry, rw, rh), 1)


def _dibujar_panel(superficie, fuente, viewport, panel, activo=False):
    pygame.draw.rect(superficie, BORDE_ACTIVO if activo else BORDE, viewport.rect_pygame(), 1)
    if panel.mostrar_quadtree:
        _dibujar_quadtree(superficie, viewport, panel.layout)
    posiciones = panel.layout.posiciones
    for arista in panel.grafo.aristas():
        if arista.origen in posiciones and arista.destino in posiciones:
            x1, y1 = viewport.mapa(*posiciones[arista.origen])
            x2, y2 = viewport.mapa(*posiciones[arista.destino])
            color = ARISTA_VERDE if panel.mostrar_quadtree else ARISTA
            pygame.draw.line(superficie, color, (x1, y1), (x2, y2), 1)
    radio = 5 if panel.grafo.numero_nodos() <= 150 else 3
    for etiqueta, (x, y) in posiciones.items():
        sx, sy = viewport.mapa(x, y)
        color = _color_nodo(panel.grafo.grado(etiqueta))
        pygame.draw.circle(superficie, color, (sx, sy), radio)
    titulo = f"{panel.titulo} | {panel.grafo.numero_nodos()} nodos | {panel.grafo.numero_aristas()} aristas | iter {panel.layout.iteracion}"
    _dibujar_texto(superficie, fuente, titulo, viewport.x + 8, viewport.y + 6)


def crear_viewports(ancho, alto, cantidad):
    if cantidad <= 1:
        return [Viewport(24, 52, ancho - 48, alto - 76)]
    if cantidad == 2:
        mitad = (ancho - 64) // 2
        return [
            Viewport(24, 52, mitad, alto - 76),
            Viewport(40 + mitad, 52, mitad, alto - 76),
        ]
    mitad_w = (ancho - 72) // 2
    mitad_h = (alto - 92) // 2
    return [
        Viewport(24, 52, mitad_w, mitad_h),
        Viewport(48 + mitad_w, 52, mitad_w, mitad_h),
        Viewport(24, 68 + mitad_h, mitad_w, mitad_h),
        Viewport(48 + mitad_w, 68 + mitad_h, mitad_w, mitad_h),
    ][:cantidad]


def ejecutar_visualizacion(paneles, titulo="Proyecto 6", ancho=1280, alto=860, pasos_por_frame=1, fps=60, captura=None, auto_salir=False, segundos=8):
    pygame.init()
    pygame.display.set_caption(titulo)
    superficie = pygame.display.set_mode((ancho, alto))
    reloj = pygame.time.Clock()
    fuente = pygame.font.SysFont("consolas", 16)
    fuente_grande = pygame.font.SysFont("consolas", 19)
    viewports = crear_viewports(ancho, alto, len(paneles))
    activo = 0
    inicio = time.time()
    corriendo = True
    captura_guardada = False
    while corriendo:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                corriendo = False
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    corriendo = False
                elif evento.key == pygame.K_TAB and viewports:
                    activo = (activo + 1) % len(viewports)
                elif evento.key in (pygame.K_PLUS, pygame.K_EQUALS):
                    viewports[activo].cambiar_zoom(0.90)
                elif evento.key in (pygame.K_MINUS, pygame.K_UNDERSCORE):
                    viewports[activo].cambiar_zoom(1.10)
                elif evento.key == pygame.K_s and captura:
                    guardar_captura(pygame, superficie, captura)
                    captura_guardada = True
                elif evento.key == pygame.K_r:
                    viewports[activo].zoom = 1.0
                    viewports[activo].pan_x = 0.0
                    viewports[activo].pan_y = 0.0
            teclas = pygame.key.get_pressed()
            if viewports:
                paso = 0.012
                if teclas[pygame.K_LEFT]:
                    viewports[activo].mover_camara(-paso, 0.0)
                if teclas[pygame.K_RIGHT]:
                    viewports[activo].mover_camara(paso, 0.0)
                if teclas[pygame.K_UP]:
                    viewports[activo].mover_camara(0.0, -paso)
                if teclas[pygame.K_DOWN]:
                    viewports[activo].mover_camara(0.0, paso)
        for panel in paneles:
            panel.paso(pasos_por_frame)
        superficie.fill(FONDO)
        _dibujar_texto(superficie, fuente_grande, titulo, 24, 18)
        _dibujar_texto(superficie, fuente, "ESC salir | TAB cambiar viewport | flechas mover | +/- zoom | R reiniciar vista | S captura", 360, 20)
        for i, (viewport, panel) in enumerate(zip(viewports, paneles)):
            _dibujar_panel(superficie, fuente, viewport, panel, activo=(i == activo))
        pygame.display.flip()
        if captura and auto_salir and not captura_guardada and time.time() - inicio >= segundos:
            guardar_captura(pygame, superficie, captura)
            captura_guardada = True
            corriendo = False
        reloj.tick(fps)
    pygame.quit()
