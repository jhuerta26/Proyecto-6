from Grafo import Grafo
#******************************************************************************
def grafoMalla(m, n, dirigido=False):
    '''
    Genera grafo de malla
    :param m: número de columnas (> 1)
    :param n: número de filas (> 1)
    :param dirigido: el grafo es dirigido?
    :return: grafo generado
    '''

    #Generar objeto grafo
    nombre='grafoMalla_m_'+str(m)+'_n_'+str(n)
    grafo = Grafo(nombre,dirigido)

    totalNodos= m*n

    #si el número de nodos es 0 regresar el grafo vacio
    if totalNodos==0:
        return grafo
        
    #Generar n nodos
    for i in range(1,totalNodos+1):
        grafo.agregar_nodo(i)

    #conectar nodos
    for i in range(1,totalNodos):
        if not i%m==0:
            grafo.agregar_arista(i,i+1)
        if i+m<=totalNodos:
            grafo.agregar_arista(i,i+m)

    return grafo
#******************************************************************************
