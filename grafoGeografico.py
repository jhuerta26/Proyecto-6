from Grafo import Grafo
#******************************************************************************
# Librerías para generar valores aleatorios
from random import seed
from random import randint
from random import random
#******************************************************************************
def grafoGeografico(n, r, dirigido=False, auto=False):
  '''
  Genera grafo aleatorio con el modelo geográfico simple
  :param n: número de nodos (> 0)
  :param r: distancia máxima para crear un nodo (0, 1)
  :param dirigido: el grafo es dirigido?
  :param auto: permitir auto-ciclos?
  :return: grafo generado
  '''
  #Generar objeto grafo
  nombre='grafoGeografico_n_'+str(n)+'_r_'+str(int(r*10))
  grafo = Grafo(nombre,dirigido,auto)

  #si el número de nodos es 0 regresar el grafo vacio
  if n==0:
      return grafo

  coordenadas={} #Diccionario para almacenar coordenadas de los nodos
  #Generar n nodos
  for i in range(n):
    grafo.agregar_nodo(i)
    coordenadas[i]=[random(),random()]

  #Evaluar cada pareja de nodos, crear una arista entre ellos si la distancia euclidiana es menor a r
  for i in range(n):
    origen=coordenadas[i] #Obtener coordenadas del nodo origen
    for j in range(n):
      destino=coordenadas[j] #Obtener coordenadas del nodo destino
      #Calcular la distancia euclidiana entre los nodos origen y destino
      distancia=((destino[0]-origen[0])**2+(destino[1]-origen[1])**2)**0.5

      if not distancia<=r: #Evitar arista si la distancia es mayor que r
        continue

      if not auto: #Si no existe autociclos
        if i == j: #Es un autociclo
          continue; #Evitar arista si no hay autociclos

      if not grafo.checarSiAristaExiste(i,j): #Agregar arista si todavía no existe
        grafo.agregar_arista(i,j)

  return grafo
