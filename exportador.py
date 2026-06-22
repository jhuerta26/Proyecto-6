import os


def asegurar_carpeta(ruta):
    if ruta:
        os.makedirs(ruta, exist_ok=True)


def guardar_captura(pygame, superficie, ruta):
    carpeta = os.path.dirname(ruta)
    asegurar_carpeta(carpeta)
    pygame.image.save(superficie, ruta)
