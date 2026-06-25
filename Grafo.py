from Nodo import Nodo
from Arista import Arista
#******************************************************************************
import pygame
import sys
import os
import math
from queue import PriorityQueue
#*********************************************************************
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
PURPLE = (116,1,113)
FPS = 60
CIRCLE_RADIUS=3
c1=1.9 #2
c2=0.01 #1
c3=0.33 #1
c4=0.1 #0.1
MIN_DIST=30
#******************************************************************************
#Clase Grafo
class Grafo:
    def __init__(self,id="grafo",dirigido=False, auto=False):
        self.id=id
        self.nodos={}
        self.aristas={}
        self.dirigido=dirigido
        self.auto=auto
        self.parent=[]
        self.rank=[]

    def agregar_nodo(self, id):
        nuevo_nodo = Nodo(id)
        self.nodos[nuevo_nodo.id]=nuevo_nodo

    def agregar_nodoExistente(self,nodo_existente):
        self.nodos[nodo_existente.id]=nodo_existente

    def agregar_arista(self,source,target):
        try:
            nueva_arista = Arista(self.nodos[source],self.nodos[target])
            self.aristas[nueva_arista.id]=nueva_arista
            self.nodos[source].grado+=1 #aumentar el grado del nodo
            self.nodos[target].grado+=1 #aumentar el grado del nodo
            self.nodos[source].vecinos.append(target)
            self.nodos[target].vecinos.append(source)
        except:
            print('***Error - Checar que los nodos se hayan decalarado previamente!***')

    def agregar_aristaExistente(self,arista_existente):
        self.aristas[arista_existente.id]=arista_existente

    def calcularGrado(self, nodo):
        return self.nodos[nodo].grado

    def totalNodos(self):
        return len(self.nodos)

    def totalAristas(self):
        return len(self.aristas)

    def checarSiAristaExiste(self,source,target):
        nueva_arista = Arista(self.nodos[source],self.nodos[target])
        nueva_arista2 = Arista(self.nodos[target],self.nodos[source])
        if nueva_arista.id in self.aristas:
            return True
        if(not self.dirigido): #Si no es un grafo dirigido
            if nueva_arista2.id in self.aristas:
                return True
        return False

    def obtenerArista(self,source,target):
        nueva_arista = Arista(self.nodos[source],self.nodos[target])
        nueva_arista2 = Arista(self.nodos[target],self.nodos[source])
        if nueva_arista.id in self.aristas:
            return self.aristas[nueva_arista.id]
        if(not self.dirigido): #Si no es un grafo dirigido
            if nueva_arista2.id in self.aristas:
                return self.aristas[nueva_arista2.id]

    def obtenerPesoDeArista(self,source,target):
        nueva_arista = Arista(self.nodos[source],self.nodos[target])
        nueva_arista2 = Arista(self.nodos[target],self.nodos[source])
        if nueva_arista.id in self.aristas:
            return self.aristas[nueva_arista.id].weight
        if(not self.dirigido): #Si no es un grafo dirigido
            if nueva_arista2.id in self.aristas:
                return self.aristas[nueva_arista2.id].weight
        return 9999999

    def nodosConectados(self,nodo):
        nodos_conectados=[]
        for key, value in self.aristas.items():
            if(value.source == self.nodos[nodo]):
                nodos_conectados.append(int(str(value.target)))
            if(not self.dirigido): #Si no es un grafo dirigido
                if(value.target==self.nodos[nodo]):
                    nodos_conectados.append(int(str(value.source)))
        return nodos_conectados

    def rutaCarpetaGV(self):
        carpeta_base = os.path.dirname(os.path.abspath(__file__))
        carpeta_gv = os.path.join(carpeta_base, "gv")
        os.makedirs(carpeta_gv, exist_ok=True)
        return carpeta_gv

    def rutaCarpetaImagenesGraphviz(self):
        carpeta_base = os.path.dirname(os.path.abspath(__file__))
        carpeta_imagenes = os.path.join(carpeta_base, "imagenes_grafos")
        os.makedirs(carpeta_imagenes, exist_ok=True)
        return carpeta_imagenes

    def limpiarNombreArchivo(self, texto):
        texto = str(texto)
        limpio = "".join(
            c if c.isalnum() or c in (" ", "_", "-") else "_"
            for c in texto
        ).replace(" ", "_")
        return limpio if limpio else "grafo"

    def construirContenidoGraphviz(self, con_labels=False, incluir_posiciones=True):
        # Genera el texto DOT/GV del grafo actual.
        # Si incluir_posiciones=True, guarda las coordenadas actuales de pygame
        # usando pos="x,y!". Esto permite conservar el acomodo final del algoritmo.
        tipo_grafo = "digraph" if self.dirigido else "graph"
        conector = "->" if self.dirigido else "--"

        contenido = ''
        contenido += tipo_grafo + ' "' + str(self.id) + '" {\n'
        contenido += '  graph [layout=neato, overlap=false, splines=true];\n'
        contenido += '  node [shape=circle, width=0.25, height=0.25, fixedsize=false];\n'

        for key, value in self.nodos.items():
            if con_labels:
                etiqueta = 'nodo_' + str(value.id) + ' (' + str(value.distancia) + ')'
            else:
                etiqueta = str(value.id)

            atributos = ['label="' + etiqueta + '"']

            if incluir_posiciones:
                try:
                    x = float(value.coordenadas[0])
                    # Se usa -y porque pygame crece hacia abajo y Graphviz hacia arriba.
                    y = -float(value.coordenadas[1])
                    atributos.append('pos="' + str(round(x, 3)) + ',' + str(round(y, 3)) + '!"')
                except Exception:
                    pass

            contenido += '  "' + str(value.id) + '" [' + ', '.join(atributos) + '];\n'

        for key, value in self.aristas.items():
            contenido += '  "' + str(value.source.id) + '" ' + conector + ' "' + str(value.target.id) + '" '
            contenido += '[label="' + str(value.weight) + '", weight=' + str(value.weight) + '];\n'

        contenido += '}\n'
        return contenido

    def graphviz(self, title=None, usar_timestamp=False, incluir_posiciones=True, generar_png=False):
        from datetime import datetime
        import subprocess

        carpeta_gv = self.rutaCarpetaGV()

        nombre_base = self.limpiarNombreArchivo(self.id)
        if title is not None:
            nombre_base += '_' + self.limpiarNombreArchivo(title)
        if usar_timestamp:
            nombre_base += '_' + datetime.now().strftime("%Y%m%d_%H%M%S")

        nombre_gv = os.path.join(carpeta_gv, nombre_base + '.gv')
        contenido = self.construirContenidoGraphviz(
            con_labels=False,
            incluir_posiciones=incluir_posiciones
        )

        with open(nombre_gv, "w", encoding="utf-8") as f:
            f.write(contenido)

        print('Archivo .gv guardado en:', nombre_gv)

        # Opcional: también generar PNG con Graphviz/neato si está instalado.
        if generar_png:
            carpeta_imagenes = self.rutaCarpetaImagenesGraphviz()
            nombre_png = os.path.join(carpeta_imagenes, nombre_base + '.png')
            try:
                subprocess.run(["neato", "-n2", "-Tpng", nombre_gv, "-o", nombre_png], check=True)
                print('Imagen Graphviz guardada en:', nombre_png)
            except FileNotFoundError:
                print('El .gv se guardó, pero no se pudo generar PNG porque Graphviz/neato no está instalado o no está en PATH.')
            except Exception as e:
                print('El .gv se guardó, pero ocurrió un error al generar PNG:', e)

        return nombre_gv

    def graphvizWithLabels(self, title=None, usar_timestamp=False, incluir_posiciones=True):
        from datetime import datetime

        carpeta_gv = self.rutaCarpetaGV()

        nombre_base = self.limpiarNombreArchivo(self.id) + '_labels'
        if title is not None:
            nombre_base += '_' + self.limpiarNombreArchivo(title)
        if usar_timestamp:
            nombre_base += '_' + datetime.now().strftime("%Y%m%d_%H%M%S")

        nombre_gv = os.path.join(carpeta_gv, nombre_base + '.gv')
        contenido = self.construirContenidoGraphviz(
            con_labels=True,
            incluir_posiciones=incluir_posiciones
        )

        with open(nombre_gv, "w", encoding="utf-8") as f:
            f.write(contenido)

        print('Archivo .gv con etiquetas guardado en:', nombre_gv)
        return nombre_gv

    def display(self):
        print('---'+str(self.totalNodos())+' Nodos---')
        print('---'+str(self.totalAristas())+' Aristas---')

    #Funciones proyecto 2 (BFS, DFS recursivo y DFS iterativo)
    def BFS(self,s): #BFS
        nombre = self.id+ '_BFS_'+str(s)
        #Generar objeto grafo
        grafoBFS = Grafo(nombre)

        #Agregar todos los nodos del grafo como no visitados
        visited=[False] * (self.totalNodos()+ 1)

        # Crear una fila para el algoritmo BFS
        queue = []

        # Agreagr el nodo fuente a la fila y marcarlo como vistiado
        queue.append(s)
        visited[s] = True

        grafoBFS.agregar_nodo(s) #Agregar nodo inicial a grafo BFS

        while queue: #Mientras haya nodos en la fila

            # Sacar de la fila un vertice
            s = queue.pop(0)

            #obtener todos los vertices adyacentes al vertice s
            #si hay un nodo que no ha sido visitado antes, marcarlo y agregarlo a la fila
            vecinos = self.nodosConectados(s)
            for i in vecinos:
                if visited[i] == False:
                    queue.append(i)
                    visited[i] = True
                    grafoBFS.agregar_nodo(i) #Agregar nodo a grafo BFS
                    grafoBFS.agregar_arista(s,i) #Agregar arista

        return grafoBFS

    def DFS_R(self,s): #DFS recursivo
        nombre = self.id+ '_DFS_R_'+str(s)

        #Generar objeto grafo
        grafoDFS_R = Grafo(nombre)

        # Crear un set de vertices visitados
        visitados = set()

        # Llamar la funcion recursiva DFS
        self.DFS_rec(s, visitados,grafoDFS_R)

        return grafoDFS_R

    def DFS_rec(self,s,visitados,grafoDFS_R):
        # Marcar el nodo como visitado
        visitados.add(s)
        grafoDFS_R.agregar_nodo(s) #Agregar nodo inicial a grafo BFS

        #obtener todos los vertices adyacentes al vertice s
        vecinos = self.nodosConectados(s)

        #Recorrer de manera recursiva todos los vertices vecinos
        for vecino in vecinos:
            if vecino not in visitados:
                self.DFS_rec(vecino, visitados,grafoDFS_R)
                grafoDFS_R.agregar_arista(s,vecino) #Agregar arista

    def DFS_I(self,s): #DFS iterativo
        nombre = self.id+ '_DFS_I_'+str(s)

        #Generar objeto grafo
        grafoDFS_I = Grafo(nombre)

        #Agregar todos los nodos del grafo como no visitados
        visited=[False] * (self.totalNodos()+ 1)

        # Create una pila para el algoritmo DFS
        stack = []

        # Agregar el nodo raiz
        stack.append(s)

        #Guardar nodos terminales
        terminal={}
        while (len(stack)):
            # Remover un elemento de la pila
            s = stack[-1]
            stack.pop()

            grafoDFS_I.agregar_nodo(s) #Agregar nodo al grafo

            # Si no ha sido visitado marcarlo como visitado
            if (not visited[s]):
                visited[s] = True

            # Obtener todos los vecinos del vertice
            vecinos = self.nodosConectados(s)

            # Si un vecino no ha sido visitado, agregarlo a la pila
            for vecino in vecinos:
                if (not visited[vecino]):
                    stack.append(vecino)
                    terminal[vecino]=s

        for key, value in terminal.items():
            grafoDFS_I.agregar_arista(key,value) #Agregar arista

        return grafoDFS_I

    def Dijkstra(self,s): #DFS iterativo
        nombre = self.id+ '_Dijkstra__source_'+str(s)

        #Generar objeto grafo
        grafoDijkstra = Grafo(nombre)
        q = PriorityQueue() #Crear cola de prioridad

        self.nodos[s].distancia=0; #Marcar el nodo fuente que tiene una distancia de cero
        q.put(self.nodos[s]) #Agregar nodo a la cola de prioridad


        while not q.empty():
            u = q.get() #Extraer el siguiente nodo (Es una tupla, por eso solo se regresa el segundo element que contiene al nodo)
            u.visitado=True #Marcar el nodo como visitado

            # Obtener todos los vecinos del nodo
            vecinos = self.nodosConectados(u.id)
            for vecino in vecinos:
                if (not self.nodos[vecino].visitado): #si el nodo no ha sido visitado antes
                    peso_arista = self.obtenerPesoDeArista(u.id,vecino)
                    if self.nodos[vecino].distancia > u.distancia + peso_arista:
                        self.nodos[vecino].distancia = u.distancia + peso_arista
                        self.nodos[vecino].padre = u.id
                        q.put(self.nodos[vecino]) #Agregar a la cola de prioridad (en base a distancia)


        #Crear arbol dijkstra
        for key, value in self.nodos.items():
            grafoDijkstra.agregar_nodoExistente(self.nodos[value.id]) #Agregar nodo inicial a grafo Dijkstra
            if value.padre!=None:
                if self.checarSiAristaExiste(value.id,value.padre): #Agregar arista si existe en el grafo original
                    nueva_arista = self.obtenerArista(value.id,value.padre)
                    grafoDijkstra.agregar_aristaExistente(nueva_arista)

        return grafoDijkstra

    def findParent(self,nodo):
        if self.parent[nodo] == nodo:
            return nodo
        return self.findParent(self.parent[nodo])

    def KruskalD(self): 
        nombre = self.id+ '_KruskalD'
        #Generar objeto grafo
        grafoKruskalD = Grafo(nombre)

        q = PriorityQueue() #Crear cola de prioridad

        self.parent = [None] * (self.totalNodos()+1)
        self.rank   = [None] * (self.totalNodos()+1)

        for key, value in self.nodos.items():
            self.parent[value.id] = value.id # Cada nodo es su propio padre al comienzo
            self.rank[value.id] = 0   # Rango de cado nodo es 0 al prinicipio


        for arista in self.aristas:
            q.put(self.aristas[arista]) #Agregar arista a la cola de prioridad (En la cola se ordenaran por peso)

        mst_costo=0

        #Agregar todos los nodos al grafo kruskal inverso
        for key, value in self.nodos.items():
            grafoKruskalD.agregar_nodoExistente(self.nodos[value.id])

        while not q.empty():
            u = q.get() #Extraer la siguiente arista
            root1 = self.findParent(u.source.id)
            root2 = self.findParent(u.target.id)

            #  Si los padres de los nodos no estan en el mismo conjunto
            # Agregar la arista al MST
            if root1 != root2 :
                grafoKruskalD.agregar_aristaExistente(u)
                mst_costo+=u.weight
                if self.rank[root1] < self.rank[root2] :
                  self.parent[root1] = root2
                  self.rank[root2] += 1
                else :
                  self.parent[root2] = root1
                  self.rank[root1] += 1

        print('KruskalD - MST costo:',mst_costo)
        return grafoKruskalD

    def KruskalI(self):
        nombre = self.id+ '_KruskalI'
        #Generar objeto grafo
        grafoKruskalI = Grafo(nombre)

        q = PriorityQueue() #Crear cola de prioridad

        mst_costo=0

         #Agregar todos los nodos al grafo kruskal inverso
        for key, value in self.nodos.items():
            grafoKruskalI.agregar_nodoExistente(self.nodos[value.id])

         #Agregar todas los aristas al grafo kruskal inverso
        for key, value in self.aristas.items():
            grafoKruskalI.agregar_aristaExistente(self.aristas[value.id])
            q.put((-value.weight,value.id))  #Agregar arista a la cola de prioridad  (Valor negativo para invertir la cola de prioridad)

        #Obtener el total de nodos inicial
        totalNodos=grafoKruskalI.totalNodos()

        while not q.empty():
            weight,arista = q.get() #Extraer la siguiente arista (con el mayor peso)

            del grafoKruskalI.aristas[arista] #Remover arista del grafo

            #Revisar si el grafo queda desconectado (El total de nodos disminuyo)
            grafoDFS=grafoKruskalI.DFS_R(1) #Llamar DFS recursivo
            totalNodosDFS = grafoDFS.totalNodos() #Obtener el total de nodos en el nuevo grafo

            if totalNodosDFS<totalNodos: #Si el nuevo grafo tiene menos nodos entonces el grafo se desconecto
                grafoKruskalI.agregar_aristaExistente(self.aristas[arista]) #Regresar la arista al grafo
                mst_costo+=weight #Sumar costo al mst

        mst_costo*=-1 #Convertir el costo negativo a positivo
        print('KruskalI - MST costo:',mst_costo)
        return grafoKruskalI

    def Prim(self):
        nombre = self.id+ '_Prim'
        #Generar objeto grafo
        grafoPrim = Grafo(nombre)

        mst_costo=0 #Incializar costo del MST

        visited=[False] * (self.totalNodos()+ 1)
        key=[float('inf')] * (self.totalNodos()+ 1)

        q = PriorityQueue() #Crear cola de prioridad
        q.put((0,1))  #Agregar nodo a la cola de prioridad con distancia de cero  // (distancia, nodo)
    

        while not q.empty():
            weight,nodo = q.get() #Extraer el siguiente nodo (con la distancia más pequeña)
            if visited[nodo]: #Si el nodo ya se visito antes, entonces evitarlo
                continue
            mst_costo+=weight #Sumar el costo al MST
            visited[nodo] =True #Marcar el nodo como visitado
            # Obtener todos los vecinos del nodo
            vecinos = self.nodosConectados(nodo)
            for vecino in vecinos:
                peso_arista = self.obtenerPesoDeArista(nodo,vecino)
                if (not visited[vecino]) and (key[vecino] > peso_arista):
                    q.put((peso_arista,vecino))
                    key[vecino]= peso_arista
                    self.nodos[vecino].padre = nodo

        #Crear arbol prim
        for key, value in self.nodos.items():
            grafoPrim.agregar_nodoExistente(self.nodos[value.id]) #Agregar nodo inicial a grafo prim
            if value.padre!=None:
                if self.checarSiAristaExiste(value.id,value.padre): #Agregar arista si existe en el grafo original
                    nueva_arista = self.obtenerArista(value.id,value.padre)
                    grafoPrim.agregar_aristaExistente(nueva_arista)

        print('Prim - MST costo:',mst_costo)
        return grafoPrim

    #pygame
    def grid(self,window,sizeX,sizeY,rows,cols):
        y=0
        x=0

        pygame.draw.line(window,WHITE,(0,y),(sizeX,y)) #Draw upper border

        distanceBtwRows = sizeY //rows #Distance between rows or size
        for j in range(rows):
            y+=distanceBtwRows #Increase y by distanceBtwRows
            pygame.draw.line(window,WHITE,(0,y),(sizeX,y)) #Draw horizontal lines

        distanceBtwCols = sizeX //cols #Distance between rows or size
        for i in range(cols):
            x+=distanceBtwCols #Increase x by distanceBtwCols
            pygame.draw.line(window,WHITE,(x,0),(x,sizeY)) #Draw vertical lines

    def obtenerLimitesGrafo(self):
        # Calcula el rectángulo que contiene a todos los nodos del grafo.
        # Esto permite ajustar automáticamente el dibujo a la ventana.
        if len(self.nodos) == 0:
            return 0, 0, 1, 1

        xs = [value.coordenadas[0] for key, value in self.nodos.items()]
        ys = [value.coordenadas[1] for key, value in self.nodos.items()]

        min_x = min(xs)
        max_x = max(xs)
        min_y = min(ys)
        max_y = max(ys)

        # Evita divisiones entre cero si todos los nodos quedan muy juntos.
        if max_x - min_x < 1:
            max_x = min_x + 1
        if max_y - min_y < 1:
            max_y = min_y + 1

        return min_x, min_y, max_x, max_y

    def calcularTransformacionAutoZoom(self, ancho, alto, margen=40, max_zoom=10):
        # Regresa una transformación para que el grafo ocupe mejor la imagen:
        # x_pantalla = x_original * escala + offset_x
        # y_pantalla = y_original * escala + offset_y
        min_x, min_y, max_x, max_y = self.obtenerLimitesGrafo()

        ancho_grafo = max_x - min_x
        alto_grafo = max_y - min_y

        ancho_util = max(1, ancho - 2 * margen)
        alto_util = max(1, alto - 2 * margen)

        escala_x = ancho_util / ancho_grafo
        escala_y = alto_util / alto_grafo
        escala = min(escala_x, escala_y)

        # Limita el acercamiento para que no se vea exageradamente grande
        # cuando los nodos estén demasiado juntos.
        escala = min(escala, max_zoom)

        offset_x = (ancho - ancho_grafo * escala) / 2 - min_x * escala
        offset_y = (alto - alto_grafo * escala) / 2 - min_y * escala

        return escala, offset_x, offset_y

    def transformarPunto(self, punto, transformacion):
        if transformacion is None:
            return int(punto[0]), int(punto[1])

        escala, offset_x, offset_y = transformacion
        x = int(punto[0] * escala + offset_x)
        y = int(punto[1] * escala + offset_y)
        return x, y

    def drawVertex(self, window, transformacion=None):
        radio = CIRCLE_RADIUS
        if transformacion is not None:
            escala = transformacion[0]
            radio = max(CIRCLE_RADIUS, min(8, int(CIRCLE_RADIUS * escala)))

        for key, value in self.nodos.items():
            x, y = self.transformarPunto(value.coordenadas, transformacion)
            pygame.draw.circle(window, value.color, (x, y), radio)

    def drawEdges(self, window, transformacion=None):
        for key, value in self.aristas.items():
            x1, y1 = self.transformarPunto(value.source.coordenadas, transformacion)
            x2, y2 = self.transformarPunto(value.target.coordenadas, transformacion)
            pygame.draw.line(window, WHITE, (x1, y1), (x2, y2))


    def redraw(self, window, auto_zoom=True, margen_zoom=40):
        global sizeX, sizeY, rows, cols, count, lines, totalLines

        window.fill(BLACK)

        transformacion = None
        if auto_zoom:
            ancho, alto = window.get_size()
            transformacion = self.calcularTransformacionAutoZoom(ancho, alto, margen=margen_zoom)

        self.drawEdges(window, transformacion)
        self.drawVertex(window, transformacion)
        pygame.display.update()
        self.calculateSprings()

    def calculateSprings(self):
        for key, value in self.nodos.items():

            vecinos = self.nodos[value.id].vecinos
            fx=0
            fy=0


            for key2, value2 in self.nodos.items():
                if value.id==value2.id:
                    continue
                if value2.id in vecinos:
                    d=math.sqrt((value2.coordenadas[0]-value.coordenadas[0])**2+(value2.coordenadas[1]-value.coordenadas[1])**2)
                    if d<MIN_DIST: #30
                        continue

                    force= c1*math.log(d/c2)
                    radians = math.atan2(value2.coordenadas[1]-value.coordenadas[1], value2.coordenadas[0]-value.coordenadas[0])
                    fx+= force*math.cos(radians)
                    fy+=force*math.sin(radians)
                else:
                    d=math.sqrt((value2.coordenadas[0]-value.coordenadas[0])**2+(value2.coordenadas[1]-value.coordenadas[1])**2)
                    if d==0:
                        continue
                    force= c3/math.sqrt(d)
                    radians = math.atan2(value2.coordenadas[1]-value.coordenadas[1], value2.coordenadas[0]-value.coordenadas[0])
                    fx-= force*math.cos(radians)
                    fy-=force*math.sin(radians)


            value.coordenadas[0]+=c4*fx
            value.coordenadas[1]+=c4*fy

            '''
            #Limit X and Y coordinates
            value.coordenadas[0]=max(value.coordenadas[0],0)
            value.coordenadas[1]=max(value.coordenadas[1],0)
            value.coordenadas[0]=min(value.coordenadas[0],sizeX)
            value.coordenadas[1]=min(value.coordenadas[1],sizeY)
            '''



    def rutaCarpetaCapturas(self):
        carpeta_base = os.path.dirname(os.path.abspath(__file__))
        carpeta_capturas = os.path.join(carpeta_base, "capturas_pygame")
        os.makedirs(carpeta_capturas, exist_ok=True)
        return carpeta_capturas

    def guardarCapturaPygame(self, window, title="captura"):
        from datetime import datetime

        carpeta = self.rutaCarpetaCapturas()

        titulo_limpio = "".join(
            c if c.isalnum() or c in (" ", "_", "-") else "_"
            for c in title
        ).replace(" ", "_")

        fecha = datetime.now().strftime("%Y%m%d_%H%M%S")
        nombre_archivo = self.id + "_" + titulo_limpio + "_" + fecha + ".png"
        ruta = os.path.join(carpeta, nombre_archivo)

        pygame.image.save(window, ruta)
        print("Captura guardada en:", ruta)

        return ruta

    def playSpringAnimation(self, title, guardar_imagen=True, iteraciones_guardar=120, cerrar_al_guardar=False, auto_zoom=True, margen_zoom=40, guardar_gv=True, **kwargs):
        global sizeX, sizeY, rows, cols, count, totalLines
        sizeX=1200 #750
        sizeY=600 #500
        rows=20
        cols=30
        window = pygame.display.set_mode((sizeX,sizeY))
        pygame.display.set_caption("Spring - "+title)
        clock = pygame.time.Clock()

        play = True
        paused = False
        iteracion = 0
        imagen_guardada = False

        if guardar_imagen:
            carpeta = self.rutaCarpetaCapturas()
            print("Las capturas se guardarán en:", carpeta)
            if auto_zoom:
                print("Auto zoom activado para ajustar el grafo a la imagen.")
        if guardar_gv:
            print("Los archivos .gv se guardarán en:", self.rutaCarpetaGV())

        #Main loop
        while play:
            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    if guardar_imagen and not imagen_guardada:
                        self.redraw(window, auto_zoom=auto_zoom, margen_zoom=margen_zoom)
                        self.guardarCapturaPygame(window, title)
                        if guardar_gv:
                            self.graphviz(title=title, usar_timestamp=True, incluir_posiciones=True)
                        imagen_guardada = True
                    play = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE: 
                        paused = not paused
            if not paused and play:
                self.redraw(window, auto_zoom=auto_zoom, margen_zoom=margen_zoom)
                iteracion += 1

                if guardar_imagen and not imagen_guardada and iteracion >= iteraciones_guardar:
                    self.guardarCapturaPygame(window, title)
                    if guardar_gv:
                        self.graphviz(title=title, usar_timestamp=True, incluir_posiciones=True)
                    imagen_guardada = True

                    if cerrar_al_guardar:
                        play = False

    #**************************************************************************
    # Funciones agregadas para Proyecto 6:
    # Comparación Fruchterman-Reingold vs Barnes-Hut.
    #**************************************************************************
    def clonar(self, nuevo_id=None):
        """Crea una copia del grafo conservando estructura, pesos y coordenadas."""
        copia = Grafo(nuevo_id if nuevo_id is not None else self.id + "_copia", self.dirigido, self.auto)

        for key, nodo in self.nodos.items():
            copia.agregar_nodo(nodo.id)
            copia.nodos[nodo.id].coordenadas = [float(nodo.coordenadas[0]), float(nodo.coordenadas[1])]
            copia.nodos[nodo.id].color = nodo.color
            copia.nodos[nodo.id].distancia = nodo.distancia

        for key, arista in self.aristas.items():
            copia.agregar_arista(arista.source.id, arista.target.id)
            nueva = copia.obtenerArista(arista.source.id, arista.target.id)
            if nueva is not None:
                nueva.weight = arista.weight

        return copia

    def calcular_k_fr(self, ancho=1200, alto=600):
        n = max(1, self.totalNodos())
        area = max(1, ancho * alto)
        return math.sqrt(area / n)

    def limitar_desplazamiento(self, dx, dy, temperatura):
        magnitud = math.sqrt(dx * dx + dy * dy)
        if magnitud == 0:
            return 0.0, 0.0
        limite = min(magnitud, temperatura)
        return (dx / magnitud) * limite, (dy / magnitud) * limite

    def calculateFruchtermanReingoldStep(self, ancho=1200, alto=600, temperatura=8.0):
        """Un paso del algoritmo Fruchterman-Reingold clásico.

        Usa fuerzas repulsivas entre todos los pares de vértices y fuerzas
        atractivas en las aristas. Complejidad aproximada: O(|V|^2 + |E|).
        """
        nodos_lista = list(self.nodos.values())
        if len(nodos_lista) == 0:
            return

        k = self.calcular_k_fr(ancho, alto)
        desplazamientos = {nodo.id: [0.0, 0.0] for nodo in nodos_lista}

        # Fuerzas repulsivas entre todos los pares de nodos.
        for i in range(len(nodos_lista)):
            v = nodos_lista[i]
            for j in range(i + 1, len(nodos_lista)):
                u = nodos_lista[j]
                dx = v.coordenadas[0] - u.coordenadas[0]
                dy = v.coordenadas[1] - u.coordenadas[1]
                distancia = math.sqrt(dx * dx + dy * dy) + 0.01
                fuerza = (k * k) / distancia
                fx = (dx / distancia) * fuerza
                fy = (dy / distancia) * fuerza
                desplazamientos[v.id][0] += fx
                desplazamientos[v.id][1] += fy
                desplazamientos[u.id][0] -= fx
                desplazamientos[u.id][1] -= fy

        # Fuerzas atractivas solamente en las aristas.
        for key, arista in self.aristas.items():
            v = arista.source
            u = arista.target
            dx = v.coordenadas[0] - u.coordenadas[0]
            dy = v.coordenadas[1] - u.coordenadas[1]
            distancia = math.sqrt(dx * dx + dy * dy) + 0.01
            fuerza = (distancia * distancia) / k
            fx = (dx / distancia) * fuerza
            fy = (dy / distancia) * fuerza
            desplazamientos[v.id][0] -= fx
            desplazamientos[v.id][1] -= fy
            desplazamientos[u.id][0] += fx
            desplazamientos[u.id][1] += fy

        # Aplicar desplazamientos limitados por temperatura.
        for nodo in nodos_lista:
            dx, dy = desplazamientos[nodo.id]
            mov_x, mov_y = self.limitar_desplazamiento(dx, dy, temperatura)
            nodo.coordenadas[0] += mov_x
            nodo.coordenadas[1] += mov_y

    def calculateBarnesHutStep(self, ancho=1200, alto=600, temperatura=8.0, theta=0.6):
        """Un paso de Fruchterman-Reingold con Barnes-Hut para repulsión.

        Las fuerzas atractivas de las aristas se calculan de forma exacta, pero
        las fuerzas repulsivas se aproximan con un QuadTree. Esto evita comparar
        cada nodo contra todos los demás cuando el grafo es grande.
        """
        nodos_lista = list(self.nodos.values())
        if len(nodos_lista) == 0:
            return

        k = self.calcular_k_fr(ancho, alto)
        desplazamientos = {nodo.id: [0.0, 0.0] for nodo in nodos_lista}

        min_x, min_y, max_x, max_y = self.obtenerLimitesGrafo()
        lado = max(max_x - min_x, max_y - min_y, 1.0)
        margen = lado * 0.05 + 1.0
        centro_x = (min_x + max_x) / 2
        centro_y = (min_y + max_y) / 2
        lado_total = lado + 2 * margen

        arbol = _QuadTreeBarnesHut(centro_x, centro_y, lado_total)
        for nodo in nodos_lista:
            arbol.insertar(nodo)

        for nodo in nodos_lista:
            fx, fy = arbol.calcular_fuerza_repulsiva(nodo, k, theta)
            desplazamientos[nodo.id][0] += fx
            desplazamientos[nodo.id][1] += fy

        # Fuerzas atractivas exactas en las aristas.
        for key, arista in self.aristas.items():
            v = arista.source
            u = arista.target
            dx = v.coordenadas[0] - u.coordenadas[0]
            dy = v.coordenadas[1] - u.coordenadas[1]
            distancia = math.sqrt(dx * dx + dy * dy) + 0.01
            fuerza = (distancia * distancia) / k
            fx = (dx / distancia) * fuerza
            fy = (dy / distancia) * fuerza
            desplazamientos[v.id][0] -= fx
            desplazamientos[v.id][1] -= fy
            desplazamientos[u.id][0] += fx
            desplazamientos[u.id][1] += fy

        for nodo in nodos_lista:
            dx, dy = desplazamientos[nodo.id]
            mov_x, mov_y = self.limitar_desplazamiento(dx, dy, temperatura)
            nodo.coordenadas[0] += mov_x
            nodo.coordenadas[1] += mov_y

    def calcularTransformacionRect(self, rect, margen=25, max_zoom=10):
        """Transformación de coordenadas para dibujar el grafo dentro de un rectángulo."""
        x0, y0, ancho, alto = rect
        min_x, min_y, max_x, max_y = self.obtenerLimitesGrafo()
        ancho_grafo = max(max_x - min_x, 1)
        alto_grafo = max(max_y - min_y, 1)

        ancho_util = max(1, ancho - 2 * margen)
        alto_util = max(1, alto - 2 * margen)
        escala = min(ancho_util / ancho_grafo, alto_util / alto_grafo)
        escala = min(escala, max_zoom)

        offset_x = x0 + (ancho - ancho_grafo * escala) / 2 - min_x * escala
        offset_y = y0 + (alto - alto_grafo * escala) / 2 - min_y * escala
        return escala, offset_x, offset_y

    def drawPanel(self, window, rect, titulo="", margen=25, color_borde=(120, 120, 120)):
        """Dibuja el grafo dentro de un panel rectangular."""
        fuente = pygame.font.Font(None, 18)
        pygame.draw.rect(window, color_borde, rect, 1)

        transformacion = self.calcularTransformacionRect(rect, margen=margen)

        for key, value in self.aristas.items():
            x1, y1 = self.transformarPunto(value.source.coordenadas, transformacion)
            x2, y2 = self.transformarPunto(value.target.coordenadas, transformacion)
            pygame.draw.line(window, (190, 190, 190), (x1, y1), (x2, y2), 1)

        radio = CIRCLE_RADIUS
        if transformacion is not None:
            radio = max(CIRCLE_RADIUS, min(6, int(CIRCLE_RADIUS * transformacion[0])))

        for key, value in self.nodos.items():
            x, y = self.transformarPunto(value.coordenadas, transformacion)
            pygame.draw.circle(window, value.color, (x, y), radio)

        if titulo:
            texto = fuente.render(titulo, True, WHITE)
            window.blit(texto, (rect[0] + 8, rect[1] + 6))
#******************************************************************************


class _QuadTreeBarnesHut:
    """QuadTree sencillo para aproximar fuerzas repulsivas con Barnes-Hut."""
    def __init__(self, cx, cy, lado, nivel=0, max_nivel=25):
        self.cx = float(cx)
        self.cy = float(cy)
        self.lado = float(max(lado, 1.0))
        self.nivel = nivel
        self.max_nivel = max_nivel
        self.nodo = None
        self.hijos = []
        self.masa = 0
        self.cm_x = 0.0
        self.cm_y = 0.0

    def contiene(self, nodo):
        mitad = self.lado / 2
        x = nodo.coordenadas[0]
        y = nodo.coordenadas[1]
        return (self.cx - mitad <= x <= self.cx + mitad and
                self.cy - mitad <= y <= self.cy + mitad)

    def es_hoja(self):
        return len(self.hijos) == 0

    def subdividir(self):
        cuarto = self.lado / 4
        nuevo_lado = self.lado / 2
        self.hijos = [
            _QuadTreeBarnesHut(self.cx - cuarto, self.cy - cuarto, nuevo_lado, self.nivel + 1, self.max_nivel),
            _QuadTreeBarnesHut(self.cx + cuarto, self.cy - cuarto, nuevo_lado, self.nivel + 1, self.max_nivel),
            _QuadTreeBarnesHut(self.cx - cuarto, self.cy + cuarto, nuevo_lado, self.nivel + 1, self.max_nivel),
            _QuadTreeBarnesHut(self.cx + cuarto, self.cy + cuarto, nuevo_lado, self.nivel + 1, self.max_nivel),
        ]

    def actualizar_centro_masa(self, nodo):
        nueva_masa = self.masa + 1
        self.cm_x = (self.cm_x * self.masa + nodo.coordenadas[0]) / nueva_masa
        self.cm_y = (self.cm_y * self.masa + nodo.coordenadas[1]) / nueva_masa
        self.masa = nueva_masa

    def insertar(self, nodo):
        if not self.contiene(nodo):
            return False

        self.actualizar_centro_masa(nodo)

        if self.nodo is None and self.es_hoja():
            self.nodo = nodo
            return True

        if self.es_hoja():
            if self.nivel >= self.max_nivel:
                return True
            nodo_anterior = self.nodo
            self.nodo = None
            self.subdividir()
            for hijo in self.hijos:
                if hijo.insertar(nodo_anterior):
                    break

        for hijo in self.hijos:
            if hijo.insertar(nodo):
                return True
        return False

    def calcular_fuerza_repulsiva(self, nodo, k, theta):
        if self.masa == 0:
            return 0.0, 0.0

        if self.es_hoja() and self.nodo is nodo:
            return 0.0, 0.0

        dx = nodo.coordenadas[0] - self.cm_x
        dy = nodo.coordenadas[1] - self.cm_y
        distancia = math.sqrt(dx * dx + dy * dy) + 0.01

        # Criterio Barnes-Hut: si la región es pequeña respecto a la distancia,
        # se usa una pseudopartícula en el centro de masa.
        if self.es_hoja() or (self.lado / distancia) < theta:
            fuerza = (self.masa * k * k) / distancia
            return (dx / distancia) * fuerza, (dy / distancia) * fuerza

        fx = 0.0
        fy = 0.0
        for hijo in self.hijos:
            hfx, hfy = hijo.calcular_fuerza_repulsiva(nodo, k, theta)
            fx += hfx
            fy += hfy
        return fx, fy
