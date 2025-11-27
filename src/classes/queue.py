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
        
    def moveNodeKtoL(self, k, l):
        if self.is_empty() or k == l:
            return
        
        prev_k = None
        curr_k = self.front
        for _ in range(k):
            if curr_k is None:
                return
            prev_k = curr_k
            curr_k = curr_k.next
        
        if curr_k is None:
            return
        
        if prev_k:
            prev_k.next = curr_k.next
        else:
            self.front = curr_k.next
        
        if curr_k == self.rear:
            self.rear = prev_k
        
        if l == 0:
            curr_k.next = self.front
            self.front = curr_k
        else:
            prev_l = None
            curr_l = self.front
            for _ in range(l):
                if curr_l is None:
                    break
                prev_l = curr_l
                curr_l = curr_l.next
            
            prev_l.next = curr_k
            curr_k.next = curr_l
            
            if curr_l is None:
                self.rear = curr_k
                
    def print(self):
        current = self.front
        values = []
        while current:
            values.append(str(current.value))
            current = current.next
        print("Queue:", " -> ".join(values))

    def length(self):
        """ Returns queue's length """
        count = 0
        current = self.front
        while current:
            count += 1
            current = current.next
        return count
