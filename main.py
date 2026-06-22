import argparse
import os
from generadores import GENERADORES, generar_grafo
from layouts import BarnesHutLayout, FruchtermanReingoldLayout
from visualizador_pygame import PanelLayout, ejecutar_visualizacion


def crear_layout(algoritmo, grafo, semilla=None, theta=0.55):
    if algoritmo == "fruchterman_reingold":
        return FruchtermanReingoldLayout(grafo, semilla=semilla)
    if algoritmo == "barnes_hut":
        return BarnesHutLayout(grafo, semilla=semilla, theta=theta)
    raise ValueError(f"Algoritmo no reconocido: {algoritmo}")


def nombre_corto_algoritmo(algoritmo):
    return "FR" if algoritmo == "fruchterman_reingold" else "Barnes-Hut"


def crear_panel(modelo, n, algoritmo, semilla, theta):
    grafo = generar_grafo(modelo, n=n, semilla=semilla)
    layout = crear_layout(algoritmo, grafo, semilla=semilla, theta=theta)
    titulo = f"{nombre_corto_algoritmo(algoritmo)} / {modelo} / n={n}"
    return PanelLayout(titulo, grafo, layout, mostrar_quadtree=(algoritmo == "barnes_hut"))


def ejecutar_individual(args):
    panel = crear_panel(args.modelo, args.n, args.algoritmo, args.semilla, args.theta)
    titulo = f"Proyecto 6 - {nombre_corto_algoritmo(args.algoritmo)} - {args.modelo}"
    ejecutar_visualizacion(
        [panel],
        titulo=titulo,
        ancho=args.ancho,
        alto=args.alto,
        pasos_por_frame=args.pasos,
        fps=args.fps,
        captura=args.captura,
        auto_salir=args.auto_salir,
        segundos=args.segundos,
    )


def ejecutar_comparacion(args):
    paneles = [
        crear_panel(args.modelo, 100, "fruchterman_reingold", args.semilla, args.theta),
        crear_panel(args.modelo, 100, "barnes_hut", args.semilla, args.theta),
        crear_panel(args.modelo, 500, "fruchterman_reingold", args.semilla, args.theta),
        crear_panel(args.modelo, 500, "barnes_hut", args.semilla, args.theta),
    ]
    titulo = f"Proyecto 6 - Comparacion por viewport - {args.modelo}"
    ejecutar_visualizacion(
        paneles,
        titulo=titulo,
        ancho=args.ancho,
        alto=args.alto,
        pasos_por_frame=args.pasos,
        fps=args.fps,
        captura=args.captura,
        auto_salir=args.auto_salir,
        segundos=args.segundos,
    )


def ejecutar_batch(args):
    os.makedirs(args.salida, exist_ok=True)
    for modelo in sorted(GENERADORES):
        captura = os.path.join(args.salida, f"{modelo}_viewport_FR_BH_100_500.png")
        paneles = [
            crear_panel(modelo, 100, "fruchterman_reingold", args.semilla, args.theta),
            crear_panel(modelo, 100, "barnes_hut", args.semilla, args.theta),
            crear_panel(modelo, 500, "fruchterman_reingold", args.semilla, args.theta),
            crear_panel(modelo, 500, "barnes_hut", args.semilla, args.theta),
        ]
        ejecutar_visualizacion(
            paneles,
            titulo=f"Proyecto 6 - {modelo}",
            ancho=args.ancho,
            alto=args.alto,
            pasos_por_frame=args.pasos,
            fps=args.fps,
            captura=captura,
            auto_salir=True,
            segundos=args.segundos,
        )


def construir_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("--modelo", default="barabasi_albert", choices=sorted(GENERADORES.keys()))
    parser.add_argument("--n", type=int, default=100)
    parser.add_argument("--algoritmo", default="fruchterman_reingold", choices=["fruchterman_reingold", "barnes_hut"])
    parser.add_argument("--semilla", type=int, default=7)
    parser.add_argument("--theta", type=float, default=0.55)
    parser.add_argument("--pasos", type=int, default=1)
    parser.add_argument("--fps", type=int, default=60)
    parser.add_argument("--ancho", type=int, default=1280)
    parser.add_argument("--alto", type=int, default=860)
    parser.add_argument("--captura", default=None)
    parser.add_argument("--auto-salir", action="store_true")
    parser.add_argument("--segundos", type=float, default=8.0)
    parser.add_argument("--comparar", action="store_true")
    parser.add_argument("--batch", action="store_true")
    parser.add_argument("--salida", default="salidas")
    return parser


def main():
    parser = construir_parser()
    args = parser.parse_args()
    if args.batch:
        ejecutar_batch(args)
    elif args.comparar:
        ejecutar_comparacion(args)
    else:
        ejecutar_individual(args)


if __name__ == "__main__":
    main()
