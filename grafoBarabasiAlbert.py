from Grafo import Grafo
#******************************************************************************
# Librerías para generar valores aleatorios
from random import seed
from random import randint
from random import random
#******************************************************************************
def grafoBarabasiAlbert(n, d, dirigido=False, auto=False):
    '''
    Genera grafo aleatorio con el modelo Barabasi-Albert
    :param n: número de nodos (> 0)
    :param d: grado máximo esperado por cada nodo (> 1)
    :param dirigido: el grafo es dirigido?
    :param auto: permitir auto-ciclos?
    :return: grafo generado
    '''
    #Generar objeto grafo
    nombre='grafoBarabasiAlbert_n_'+str(n)+'_d_'+str(d)
    grafo = Grafo(nombre,dirigido,auto)

    #si el número de nodos es 0 regresar el grafo vacio
    if n==0:
        return grafo

    #Generar n nodos
    for i in range(n):
        grafo.agregar_nodo(i)

    #Evaluar cada pareja de nodos, crear una arista entre ellos con probabilidad p
    gradoNodoOrigen=-1
    gradoNodoDestino=-1
    for i in range(n):
        for j in range(n):
            gradoNodoOrigen = grafo.calcularGrado(i)
            gradoNodoDestino= grafo.calcularGrado(j)

            if not auto: #Si no existe autociclos
                if i == j: #Es un autociclo
                    continue; #Evitar arista si no hay autociclos

            if gradoNodoOrigen<d and gradoNodoDestino<d: #El grado de los nodos es menor a d
                aleatorio = random() #Generar un número aleatorio
                p = 1 - (gradoNodoOrigen/d)

                if not aleatorio<=p: #Evitar arista si no se cumple la probabilidad
                    continue

                if not grafo.checarSiAristaExiste(i,j): #Agregar arista si todavía no existe
                    grafo.agregar_arista(i,j)

    return grafo
