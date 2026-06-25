#******************************************************************************
# Proyecto 6 - Disposición de grafos - parte II
# Comparación visual: Fruchterman-Reingold vs Barnes-Hut
#
# Visualización en 2 x 2:
#   - Izquierda: Fruchterman-Reingold
#   - Derecha: Barnes-Hut
#   - Arriba: 100 nodos
#   - Abajo: 500 nodos
#
# Controles:
#   - ESPACIO: iniciar / pausar / reanudar las iteraciones
#   - R: reiniciar el modelo actual desde la iteración 0
#   - ESC o cerrar ventana: salir del modelo actual
#
# Al llegar a ITERACIONES_GUARDAR:
#   - Guarda la captura PNG
#   - Guarda los archivos .gv
#   - Pausa la visualización, pero NO cierra la ventana
#******************************************************************************

import os
from datetime import datetime
from random import seed

import pygame

from grafoMalla import grafoMalla
from grafoGeografico import grafoGeografico
from grafoErdosRenyi import grafoErdosRenyi
from grafoGilbert import grafoGilbert
from grafoBarabasiAlbert import grafoBarabasiAlbert
from grafoDorogovtsevMendes import grafoDorogovtsevMendes

#******************************************************************************
# Parámetros generales
#******************************************************************************
ANCHO_VENTANA = 1200
ALTO_VENTANA = 850
FPS = 60

# Número de iteraciones donde se guardan la imagen y los .gv.
# Al llegar a este valor, la ejecución se pausa, pero no se cierra.
ITERACIONES_GUARDAR = 300

# Parámetro Barnes-Hut.
# Menor theta = más precisión, más lento.
# Mayor theta = más rápido, menos precisión.
THETA_BARNES_HUT = 0.6

# Temperatura inicial de ambos métodos.
TEMPERATURA_INICIAL = 8.0

# Factor de enfriamiento. Valores cercanos a 1 tardan más en estabilizarse.
FACTOR_ENFRIAMIENTO = 0.985
TEMPERATURA_MINIMA = 0.75

# Cambia a False si solo quieres probar un modelo.
EJECUTAR_TODOS_LOS_MODELOS = True

#******************************************************************************
# Carpeta base: se toma desde donde está este archivo, no desde donde se ejecuta
# la terminal. Así se evitan problemas con rutas en VS Code.
#******************************************************************************
CARPETA_BASE = os.path.dirname(os.path.abspath(__file__))
CARPETA_CAPTURAS = os.path.join(CARPETA_BASE, "capturas_proyecto6")
CARPETA_GV = os.path.join(CARPETA_BASE, "gv")
os.makedirs(CARPETA_CAPTURAS, exist_ok=True)
os.makedirs(CARPETA_GV, exist_ok=True)

#******************************************************************************
# Modelos de generación
#******************************************************************************
def crear_modelos():
    """Regresa una lista de modelos. Cada modelo contiene un grafo de 100 y otro de 500 nodos."""
    modelos = []

    modelos.append((
        "Geografico",
        lambda: grafoGeografico(n=100, r=0.30, dirigido=False, auto=False),
        lambda: grafoGeografico(n=500, r=0.12, dirigido=False, auto=False)
    ))

    modelos.append((
        "Malla",
        lambda: grafoMalla(10, 10, dirigido=False),
        lambda: grafoMalla(20, 25, dirigido=False)
    ))

    modelos.append((
        "Erdos_Renyi",
        lambda: grafoErdosRenyi(n=100, m=100, dirigido=False, auto=False),
        lambda: grafoErdosRenyi(n=500, m=500, dirigido=False, auto=False)
    ))

    modelos.append((
        "Gilbert",
        lambda: grafoGilbert(n=100, p=0.05, dirigido=False, auto=False),
        lambda: grafoGilbert(n=500, p=0.015, dirigido=False, auto=False)
    ))

    modelos.append((
        "Barabasi_Albert",
        lambda: grafoBarabasiAlbert(n=100, d=4, dirigido=False, auto=False),
        lambda: grafoBarabasiAlbert(n=500, d=3, dirigido=False, auto=False)
    ))

    modelos.append((
        "Dorogovtsev_Mendes",
        lambda: grafoDorogovtsevMendes(100, dirigido=False),
        lambda: grafoDorogovtsevMendes(500, dirigido=False)
    ))

    if EJECUTAR_TODOS_LOS_MODELOS:
        return modelos

    # Para probar solo un modelo, cambia el índice.
    # 0 Geografico, 1 Malla, 2 Erdos_Renyi, 3 Gilbert, 4 Barabasi_Albert, 5 Dorogovtsev_Mendes
    return [modelos[0]]

#******************************************************************************
# Funciones auxiliares de visualización y guardado
#******************************************************************************
def paneles_2x2():
    margen = 10
    separacion = 14
    ancho_panel = (ANCHO_VENTANA - 2 * margen - separacion) // 2
    alto_panel = (ALTO_VENTANA - 2 * margen - separacion) // 2

    return {
        "fr_100": (margen, margen, ancho_panel, alto_panel),
        "bh_100": (margen + ancho_panel + separacion, margen, ancho_panel, alto_panel),
        "fr_500": (margen, margen + alto_panel + separacion, ancho_panel, alto_panel),
        "bh_500": (margen + ancho_panel + separacion, margen + alto_panel + separacion, ancho_panel, alto_panel),
    }


def guardar_captura(window, nombre_modelo):
    fecha = datetime.now().strftime("%Y%m%d_%H%M%S")
    nombre = f"proyecto6_{nombre_modelo}_comparacion_{fecha}.png"
    ruta = os.path.join(CARPETA_CAPTURAS, nombre)
    pygame.image.save(window, ruta)
    print("Captura guardada en:", ruta)
    return ruta


def guardar_gv_finales(nombre_modelo, grafos):
    fecha = datetime.now().strftime("%Y%m%d_%H%M%S")
    for etiqueta, grafo in grafos.items():
        titulo = f"Proyecto6_{nombre_modelo}_{etiqueta}_{fecha}"
        grafo.graphviz(title=titulo, usar_timestamp=False, incluir_posiciones=True)


def dibujar_escena(window, nombre_modelo, grafos, iteracion, temperaturas, pausado=True, mensaje_extra=""):
    window.fill((0, 0, 0))
    rects = paneles_2x2()

    grafos["fr_100"].drawPanel(
        window,
        rects["fr_100"],
        f"{nombre_modelo} | Fruchterman-Reingold | 100 nodos | {grafos['fr_100'].totalAristas()} aristas"
    )
    grafos["bh_100"].drawPanel(
        window,
        rects["bh_100"],
        f"{nombre_modelo} | Barnes-Hut | 100 nodos | {grafos['bh_100'].totalAristas()} aristas"
    )
    grafos["fr_500"].drawPanel(
        window,
        rects["fr_500"],
        f"{nombre_modelo} | Fruchterman-Reingold | 500 nodos | {grafos['fr_500'].totalAristas()} aristas"
    )
    grafos["bh_500"].drawPanel(
        window,
        rects["bh_500"],
        f"{nombre_modelo} | Barnes-Hut | 500 nodos | {grafos['bh_500'].totalAristas()} aristas"
    )

    fuente = pygame.font.Font(None, 20)
    estado = "PAUSADO" if pausado else "EJECUTANDO"
    info = (
        f"Proyecto 6 | {estado} | Iteracion: {iteracion}/{ITERACIONES_GUARDAR} | "
        "ESPACIO iniciar/pausar | R reiniciar | ESC salir"
    )
    texto = fuente.render(info, True, (255, 255, 255))
    window.blit(texto, (12, ALTO_VENTANA - 42))

    if mensaje_extra:
        texto_extra = fuente.render(mensaje_extra, True, (255, 255, 0))
        window.blit(texto_extra, (12, ALTO_VENTANA - 22))
    else:
        texto_extra = fuente.render("FR izquierda | Barnes-Hut derecha | 100 arriba | 500 abajo", True, (180, 180, 180))
        window.blit(texto_extra, (12, ALTO_VENTANA - 22))

    pygame.display.update()


def aplicar_paso_layout(grafos, temperaturas):
    # Fruchterman-Reingold clásico: repulsión entre todos los pares de nodos.
    grafos["fr_100"].calculateFruchtermanReingoldStep(
        ancho=ANCHO_VENTANA // 2,
        alto=ALTO_VENTANA // 2,
        temperatura=temperaturas["fr_100"]
    )
    grafos["fr_500"].calculateFruchtermanReingoldStep(
        ancho=ANCHO_VENTANA // 2,
        alto=ALTO_VENTANA // 2,
        temperatura=temperaturas["fr_500"]
    )

    # Barnes-Hut: misma base de fuerzas, pero con aproximación mediante QuadTree.
    grafos["bh_100"].calculateBarnesHutStep(
        ancho=ANCHO_VENTANA // 2,
        alto=ALTO_VENTANA // 2,
        temperatura=temperaturas["bh_100"],
        theta=THETA_BARNES_HUT
    )
    grafos["bh_500"].calculateBarnesHutStep(
        ancho=ANCHO_VENTANA // 2,
        alto=ALTO_VENTANA // 2,
        temperatura=temperaturas["bh_500"],
        theta=THETA_BARNES_HUT
    )

    for key in temperaturas:
        temperaturas[key] = max(TEMPERATURA_MINIMA, temperaturas[key] * FACTOR_ENFRIAMIENTO)


def crear_temperaturas_iniciales():
    return {
        "fr_100": TEMPERATURA_INICIAL,
        "bh_100": TEMPERATURA_INICIAL,
        "fr_500": TEMPERATURA_INICIAL,
        "bh_500": TEMPERATURA_INICIAL,
    }


def preparar_grafos_para_modelo(nombre_modelo, crear_100, crear_500):
    print("\n" + "=" * 70)
    print("Modelo:", nombre_modelo)
    print("=" * 70)

    # Semillas fijas para que los resultados sean reproducibles.
    seed(100)
    base_100 = crear_100()
    seed(500)
    base_500 = crear_500()

    base_100.display()
    base_500.display()

    # Se clona cada grafo para que FR y Barnes-Hut empiecen con la misma estructura
    # y con las mismas coordenadas iniciales. Así la comparación es justa.
    grafos = {
        "fr_100": base_100.clonar(f"{nombre_modelo}_FR_100"),
        "bh_100": base_100.clonar(f"{nombre_modelo}_BH_100"),
        "fr_500": base_500.clonar(f"{nombre_modelo}_FR_500"),
        "bh_500": base_500.clonar(f"{nombre_modelo}_BH_500"),
    }
    return grafos


def reiniciar_estado(nombre_modelo, crear_100, crear_500):
    grafos = preparar_grafos_para_modelo(nombre_modelo, crear_100, crear_500)
    temperaturas = crear_temperaturas_iniciales()
    iteracion = 0
    guardado = False
    pausado = True
    mensaje_extra = "Presiona ESPACIO para iniciar las iteraciones."
    return grafos, temperaturas, iteracion, guardado, pausado, mensaje_extra


def ejecutar_comparacion(nombre_modelo, crear_100, crear_500):
    grafos, temperaturas, iteracion, guardado, pausado, mensaje_extra = reiniciar_estado(
        nombre_modelo,
        crear_100,
        crear_500
    )

    pygame.init()
    pygame.font.init()
    window = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
    pygame.display.set_caption(f"Proyecto 6 - {nombre_modelo} - FR vs Barnes-Hut")
    clock = pygame.time.Clock()

    ejecutando = True

    print("Capturas en:", CARPETA_CAPTURAS)
    print("Archivos .gv en:", CARPETA_GV)
    print("Controles:")
    print("  ESPACIO: iniciar / pausar / reanudar")
    print("  R: reiniciar el modelo actual desde iteración 0")
    print("  ESC o cerrar ventana: salir del modelo actual")

    # Dibuja la escena inicial sin avanzar iteraciones.
    dibujar_escena(window, nombre_modelo, grafos, iteracion, temperaturas, pausado, mensaje_extra)

    while ejecutando:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if not guardado:
                    dibujar_escena(window, nombre_modelo, grafos, iteracion, temperaturas, True, "Salida solicitada. Guardando estado actual...")
                    guardar_captura(window, nombre_modelo)
                    guardar_gv_finales(nombre_modelo, grafos)
                    guardado = True
                ejecutando = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if not guardado:
                        dibujar_escena(window, nombre_modelo, grafos, iteracion, temperaturas, True, "Salida solicitada. Guardando estado actual...")
                        guardar_captura(window, nombre_modelo)
                        guardar_gv_finales(nombre_modelo, grafos)
                        guardado = True
                    ejecutando = False

                elif event.key == pygame.K_SPACE:
                    pausado = not pausado
                    if pausado:
                        mensaje_extra = "Pausado. Presiona ESPACIO para continuar o R para reiniciar."
                    else:
                        mensaje_extra = "Ejecutando iteraciones..."
                    dibujar_escena(window, nombre_modelo, grafos, iteracion, temperaturas, pausado, mensaje_extra)

                elif event.key == pygame.K_r:
                    print("Reiniciando modelo actual desde iteración 0...")
                    grafos, temperaturas, iteracion, guardado, pausado, mensaje_extra = reiniciar_estado(
                        nombre_modelo,
                        crear_100,
                        crear_500
                    )
                    dibujar_escena(window, nombre_modelo, grafos, iteracion, temperaturas, pausado, mensaje_extra)

        if not pausado and ejecutando:
            aplicar_paso_layout(grafos, temperaturas)
            iteracion += 1

            if not guardado and iteracion >= ITERACIONES_GUARDAR:
                mensaje_extra = "Límite alcanzado. Imagen y .gv guardados. Presiona R para reiniciar o ESPACIO para continuar."
                dibujar_escena(window, nombre_modelo, grafos, iteracion, temperaturas, True, mensaje_extra)
                guardar_captura(window, nombre_modelo)
                guardar_gv_finales(nombre_modelo, grafos)
                guardado = True
                pausado = True
            else:
                dibujar_escena(window, nombre_modelo, grafos, iteracion, temperaturas, pausado, mensaje_extra)

        elif pausado and ejecutando:
            # Mantiene visible la ventana aunque esté pausada.
            pygame.time.wait(20)

    pygame.quit()


def main():
    for nombre_modelo, crear_100, crear_500 in crear_modelos():
        ejecutar_comparacion(nombre_modelo, crear_100, crear_500)

    print("\nProyecto 6 terminado.")
    print("Revisa las capturas en:", CARPETA_CAPTURAS)
    print("Revisa los .gv en:", CARPETA_GV)


if __name__ == "__main__":
    main()
#******************************************************************************
