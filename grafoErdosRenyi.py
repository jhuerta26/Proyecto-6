from Grafo import Grafo
#******************************************************************************
# Librerías para generar valores aleatorios
from random import seed
from random import randint
from random import random
#******************************************************************************
def grafoErdosRenyi(n, m, dirigido=False, auto=False):
  '''
  Genera grafo aleatorio con el modelo Erdos-Renyi
  :param n: número de nodos (> 0)
  :param m: número de aristas (>= n-1)
  :param dirigido: el grafo es dirigido?
  :param auto: permitir auto-ciclos?
  :return: grafo generado
  '''
  #Generar objeto grafo
  nombre='grafoErdosRenyi_n_'+str(n)+'_m_'+str(m)
  grafo = Grafo(nombre,dirigido,auto)

  #si el número de nodos es 0 regresar el grafo vacio
  if n==0:
      return grafo

  #Generar n nodos
  for i in range(n):
    grafo.agregar_nodo(i)

  #Elegir dos nodos de manera aleatoria y crear una arista entre los nodos, evitar si ya existe la arista, repetir m veces
  count=0
  while(count<m):
    nodo1 = randint(0, n-1)
    nodo2 = randint(0, n-1)
    if not auto: #Si no existe autociclos
      if nodo1 == nodo2: #Es un autociclo
        continue; #Genera una nueva iteración
    if not grafo.checarSiAristaExiste(nodo1,nodo2): #Agregar arista si todavía no existe
      grafo.agregar_arista(nodo1,nodo2)
      count+=1

  return grafo
#******************************************************************************
