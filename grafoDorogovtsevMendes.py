from Grafo import Grafo
#******************************************************************************
# Librerías para generar valores aleatorios
from random import seed
from random import randint
from random import random
#******************************************************************************
def grafoDorogovtsevMendes (n, dirigido=False):
    '''
    Genera grafo aleatorio con el modelo Dorogovtsev-Mendes
    :param n: número de nodos (≥ 3)
    :param dirigido: el grafo es dirigido?
    :return: grafo generado
    '''

    #Generar objeto grafo
    nombre='grafoDorogovtsevMendes_n_'+str(n)
    grafo = Grafo(nombre,dirigido)

    #si el número de nodos es menor que 3 regresar el grafo vacio
    if n<3:
        print('Error: Al menos debe haber 3 nodos')
        return grafo

    #Generar n nodos
    for i in range(n):
        grafo.agregar_nodo(i)

    #Generar 3 aristas para formar un triángulo con los primeros 3 nodos
    grafo.agregar_arista(0,1)
    grafo.agregar_arista(1,2)
    grafo.agregar_arista(2,0)


    #Si solo hay 3 nodos regresar grafo
    if n==3:
        return grafo

    nodoNuevo = 3 #Empezar por el nodo 4 (contando desde 0)
    while nodoNuevo<n: #Por cada nodo después del tercer nodo
        #Obtener lista de aristas
        aristasDisponibles = list(grafo.aristas.keys())
        #Obterner el total de aristas
        numeroAristas = grafo.totalAristas()

        #Seleccionar arista de manera aleatoria
        aleatorio = randint(0, numeroAristas-1)
        aristaSeleccionada = aristasDisponibles[aleatorio]

        #obtener los nodos extremos de la arista seleccionada
        extremo1=grafo.aristas[aristaSeleccionada].source.id
        extremo2=grafo.aristas[aristaSeleccionada].target.id

        #Crear una arista entre el nodo nuevo y los extremos de
        #la arista seleccionda
        grafo.agregar_arista(nodoNuevo,extremo1)
        grafo.agregar_arista(nodoNuevo,extremo2)

        nodoNuevo+=1

    return grafo
