from Grafo import Grafo
#******************************************************************************
# Librerías para generar valores aleatorios
from random import seed
from random import randint
from random import random
#******************************************************************************
def grafoGilbert(n, p, dirigido=False, auto=False):
  '''
  Genera grafo aleatorio con el modelo Gilbert
  :param n: número de nodos (> 0)
  :param p: probabilidad de crear una arista (0, 1)
  :param dirigido: el grafo es dirigido?
  :param auto: permitir auto-ciclos?
  :return: grafo generado
  '''
  #Generar objeto grafo
  nombre='grafoGilbert_n_'+str(n)+'_p_'+str(int(p*100))
  grafo = Grafo(nombre,dirigido,auto)

  #si el número de nodos es 0 regresar el grafo vacio
  if n==0:
      return grafo

  #Generar n nodos
  for i in range(n):
    grafo.agregar_nodo(i)

  #Evaluar cada pareja de nodos, crear una arista entre ellos con probabilidad p
  for i in range(n):
    for j in range(n):
      aleatorio = random() #Generar un número aleatorio
      if not aleatorio<=p: #Evitar arista si no se cumple la probabilidad
        continue
      if not auto: #Si no existe autociclos
        if i == j: #Es un autociclo
          continue; #Evitar arista si no hay autociclos
      if not grafo.checarSiAristaExiste(i,j): #Agregar arista si todavía no existe
        grafo.agregar_arista(i,j)

  return grafo
