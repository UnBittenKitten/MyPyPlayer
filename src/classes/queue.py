''' nata
Requerimientos

* Crear clase lista nodo
* Crear clase cola 

Como resolver

# 
Teoría necesaria

0.1 - 1 Que es un puntero 
    Es una variable que almacena la direccion de memoria de cualquier otra variable

0.1 - 2 Como funcionan los punteros en Python
    No existen los punteros como tal, pero sí existen las referencias.
    
0.1 - 3 Que es un diccionario en Python
0.1 Ver como funcionan los punteros en Python
0.2 Ver qué es una lista enlazada
0.3 Ver como se crea una lista enlazada en python
0.4 Que parametros lleva una lista enlazada
0.5 Que es la recursión en Python
0.6 Como practicar la recursión en Python

Clase cola

1.0.9 Ver si ya tenemos una clase cola hecha y que metodos utilizamos
1.1 Ver un video para entender que es una clase cola
1.2 Definir que parametros vamos a utilizar en la clase y como vamos a interactuar con los parametros definidos, variables, tipos...
1.3 - 1 Qué metodos se suelen incluir para que sea funcional?
1.3 Añadir primero metodos de entrada
1.4 Añadir metodos de salida
1.5 Añadir metodos especiales como str
1.6 Comentarizar y formatear todo

Clase lista nodo

2.0 Ver si ya tenemos una clase nodo creada
2.1 Ver teoria sobre como funciona una clase nodo
2.2 Ver practicas estandar sobre las lista nodo
2.3 Qué metodos se suelen incluir o son necesarios para que la clase sea funcional?
2.4 Metodos de entrada de datos (si es necesario mediante el uso de otra clase)
2.5 Metodos de salida de datos
2.6 Metodos especiales (si son necesarios)
2.7 Comentarizar y formatear

'''
import random

#--------------------------------------------------------------------------------
# Clase lista nodo
#--------------------------------------------------------------------------------
'Guarda un valor y una referencia (puntero) a otro nodo'

class ListNode:
    def __init__(self, value=None):
        self.value = value
        self.next = None

#--------------------------------------------------------------------------------
# Clase cola
#--------------------------------------------------------------------------------
'Çontrola el flujo de trabajo, en este caso para controlar las pistas'

class Queue:
    def __init__(self):
        self.front = None   # primer nodo
        self.rear = None    # último nodo

    def is_empty(self):
        return self.front is None

    def add(self, value):  # enqueue
        new_node = ListNode(value)

        if self.is_empty():
            self.front = new_node
            self.rear = new_node
        else:
            self.rear.next = new_node  # enlazar
            self.rear = new_node       # actualizar cola

    def remove(self):  # dequeue
        if self.is_empty():
            raise Exception("Queue is empty")

        value = self.front.value
        self.front = self.front.next

        if self.front is None:  # si sacaste el último
            self.rear = None

        return value

    def peek(self):
        if self.is_empty():
            raise Exception("Queue is empty")
        return self.front.value

    def skip(self):
        return self.remove()

    def clear(self):
        self.front = None
        self.rear = None

    def add_next(self, value):
        if self.is_empty():
            self.add(value)
            return
        
        new_node = ListNode(value)
        new_node.next = self.front.next
        self.front.next = new_node

        if self.rear is self.front:
            self.rear = new_node

    def shuffle(self):
        if self.is_empty() or self.front.next is None:
            return
        
        # extraer nodos a lista
        songs = []
        current = self.front
        while current:
            songs.append(current.value)
            current = current.next

        random.shuffle(songs)

        # reconstruir cola
        self.clear()
        for s in songs:
            self.add(s)

    def repeat(self):
        if self.is_empty():
            return
        
        current_song = self.front.value
        self.add(current_song)
