from random import randint
#******************************************************************************
sizeX=1200
sizeY=600

colors=['RED','GREEN','BLUE','PURPLE']
#******************************************************************************
#Clase Nodo
class Nodo:
  def __init__(self, id):
    self.id = id
    self.grado=0

    #Parametros algoritmo de dijkstra
    self.padre=None
    self.visitado=False
    self.distancia=float('inf')
    self.coordenadas=[randint(1,sizeX),randint(1,sizeY)] #x,y
    self.color=colors[randint(0,(len(colors)-1))] #Pick a random color
    self.vecinos=[]

  def __str__(self):
      return str(self.id)
  def __eq__(self, otroNodo):
      return self.id == otroNodo.id
  def __lt__(self, otroNodo):
      return self.distancia < otroNodo.distancia


#******************************************************************************
