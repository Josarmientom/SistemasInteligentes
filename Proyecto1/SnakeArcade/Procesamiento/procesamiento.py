'''
Dada una matriz, vamos a obtener el mejor camino para llegar a la manzana
'''
import numpy as np


def get_path(matrix):
    pass

def np_where(matrix, value):
    # Aplicamos un np where que nos devuelva una tupla
    return (np.where(matrix == value)[0][0], np.where(matrix == value)[1][0])

def manhattan_distance(a, b):
    # a y b son tuplas con puntos en la matriz
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def neighbors(matrix, node):
    # node es una tupla con la posicion en la matriz
    # matrix es la matriz de la serpiente
    # neighbors es una lista con las posiciones de los vecinos
    neighbors = []
    # Si no es la primera fila
    if node[0] != 0:
        # Si no hay pared
        if matrix[node[0] - 1][node[1]] <= 0:
            neighbors.append((node[0] - 1, node[1]))
    # Si no es la ultima fila
    if node[0] != 14:
        # Si no hay pared
        if matrix[node[0] + 1][node[1]] <= 0:
            neighbors.append((node[0] + 1, node[1]))
    # Si no es la primera columna
    if node[1] != 0:
        # Si no hay pared
        if matrix[node[0]][node[1] - 1] <= 0:
            neighbors.append((node[0], node[1] - 1))
    # Si no es la ultima columna
    if node[1] != 16:
        # Si no hay pared
        if matrix[node[0]][node[1] + 1] <= 0:
            neighbors.append((node[0], node[1] + 1))
    return neighbors

def tree_a_star(matrix, start, goal):
    # start es una tupla con la posicion de la cabeza de la serpiente
    # goal es una tupla con la posicion de la manzana
    # matrix es la matriz de la serpiente
    # tree es un diccionario con las posiciones de los nodos y sus padres
    tree = {}
    # closed_set es un conjunto con las posiciones de los nodos que ya fueron visitados
    closed_set = set()
    # open_set es un conjunto con las posiciones de los nodos que aun no han sido visitados
    open_set = set()
    # g_score es un diccionario con las posiciones de los nodos y su distancia desde el nodo inicial
    g_score = {}
    # f_score es un diccionario con las posiciones de los nodos y su distancia desde el nodo inicial + la heuristica
    f_score = {}
    # Agregamos el nodo inicial al open_set
    open_set.add(start)
    # Agregamos el nodo inicial al g_score
    g_score[start] = 0
    # Agregamos el nodo inicial al f_score
    f_score[start] = manhattan_distance(start, goal)
    # Mientras el open_set no este vacio
    while open_set:
        # Obtenemos el nodo con menor f_score
        current = min(open_set, key=lambda o: f_score[o])
        # Si el nodo actual es el nodo objetivo
        if current == goal:
            # Retornamos el arbol
            return tree
        # Agregamos el nodo actual al closed_set
        closed_set.add(current)
        # Eliminamos el nodo actual del open_set
        open_set.remove(current)
        # Obtenemos los vecinos del nodo actual
        for neighbor in neighbors(matrix, current):
            # Si el vecino esta en el closed_set
            if neighbor in closed_set:
                # Continuamos con el siguiente vecino
                continue
            # Obtenemos la distancia del nodo actual al vecino
            tentative_g_score = g_score[current] + 1
            # Si el vecino no esta en el open_set
            if neighbor not in open_set:
                # Agregamos el vecino al open_set
                open_set.add(neighbor)
            # Si la distancia del nodo actual al vecino
            elif tentative_g_score >= g_score[neighbor]:
                # Continuamos con el siguiente vecino
                continue
            # Agregamos el nodo actual como padre del vecino
            tree[neighbor] = current
            # Agregamos la distancia del nodo actual al vecino al g_score
            g_score[neighbor] = tentative_g_score
            # Agregamos la distancia del nodo actual al vecino + la heuristica al f_score
            f_score[neighbor] = g_score[neighbor] + manhattan_distance(neighbor, goal)
    # Si no hay camino
    return None

def print_path(matrix, tree, start, goal):
    # matrix es la matriz de la serpiente
    # tree es el arbol de la busqueda
    # start es una tupla con la posicion de la cabeza de la serpiente
    # goal es una tupla con la posicion de la manzana
    # path es una lista con las posiciones del camino
    path = []
    # current es una tupla con la posicion del nodo actual
    current = goal
    # Mientras el nodo actual sea diferente al nodo inicial
    while current != start:
        # Agregamos el nodo actual al camino
        path.append(current)
        # Obtenemos el nodo padre del nodo actual
        current = tree[current]
    # Agregamos el nodo inicial al camino
    path.append(start)
    # Invertimos el camino
    path.reverse()
    # Para cada posicion en el camino
    count = 1
    matrix_out = np.zeros(shape=(15,17))
    for position in path:
        # Si la posicion no es el nodo inicial ni el objetivo
        # if position != start and position != goal:
        matrix_out[position[0]][position[1]] = count
        count += 1
    # Retornamos la matriz
    return matrix_out

if __name__ == '__main__':
    # Para esta prueba supondremos que la cabeza de la serpiente es el mayor numero, o el numero de manzanas capturadas + 4
    matrix = np.zeros(shape=(15,17))
    matrix[0][4] = 4
    matrix[0][3] = 3
    matrix[0][2] = 2
    matrix[0][1] = 1

    # Manzana en la posicion [7, 12] con -1
    matrix[7][12] = -1

    # Para obtener la posicion de la cabeza de la serpiente simplemente buscaremos la ubicacion del numero de manzanas capturadas + 4

    # Manzanas = 0, Cabeza = 0 + 4
    head = np_where(matrix, 4)
    # La posicion de la manzana es la ubicacion del numero -1
    apple = np_where(matrix, -1)

    # Aplicaremos A* desde head hasta apple usando la heuristica de Manhattan y para obtener los nodos usaremos la restriccion de paredes


    print("head ", head)
    print("apple ", apple)
    print("tree", tree_a_star(matrix, head, apple))
    print("neighbors ", neighbors(matrix, head))
    print(matrix)
    print("\n\n\n\n")
    print(print_path(matrix, tree_a_star(matrix, head, apple), head, apple))
