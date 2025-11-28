import random

class ListNode:
    def __init__(self, value=None):
        self.value = value
        self.next = None

class Queue:
    def __init__(self):
        self.front = None   # primer nodo
        self.rear = None    # último nodo
        self._length = 0    # Track length

    def is_empty(self):
        return self.front is None

    def add(self, value):  # enqueue
        new_node = ListNode(value)
        if self.is_empty():
            self.front = new_node
            self.rear = new_node
        else:
            self.rear.next = new_node
            self.rear = new_node
        self._length += 1

    def remove(self):  # dequeue
        if self.is_empty():
            return None
        value = self.front.value
        self.front = self.front.next
        if self.front is None:
            self.rear = None
        self._length -= 1
        return value

    # --- ADDED FOR QUEUE PANE FUNCTIONALITY ---
    def remove_at_index(self, index):
        if self.is_empty() or index < 0: return
        
        if index == 0:
            self.remove()
            return

        current = self.front
        prev = None
        count = 0
        
        while current and count < index:
            prev = current
            current = current.next
            count += 1
            
        if current is None: return
        
        prev.next = current.next
        if current == self.rear:
            self.rear = prev
        self._length -= 1
    # ------------------------------------------

    def peek(self):
        if self.is_empty(): return None
        return self.front.value

    def clear(self):
        self.front = None
        self.rear = None
        self._length = 0

    def length(self):
        # Return tracked length for O(1) access
        return self._length
        
    def moveNodeKtoL(self, k, l):
        if self.is_empty() or k == l: return
        
        # Extract
        target_node = None
        if k == 0:
            target_node = self.front
            self.front = self.front.next
            if self.front is None: self.rear = None
        else:
            prev = self.front
            for _ in range(k - 1):
                if prev.next is None: return
                prev = prev.next
            target_node = prev.next
            if target_node is None: return
            prev.next = target_node.next
            if prev.next is None: self.rear = prev
            
        # Insert
        if l == 0:
            target_node.next = self.front
            self.front = target_node
            if self.rear is None: self.rear = target_node
        else:
            prev = self.front
            for _ in range(l - 1):
                if prev is None: break
                prev = prev.next
            if prev:
                target_node.next = prev.next
                prev.next = target_node
                if target_node.next is None: self.rear = target_node

    def print(self):
        current = self.front
        values = []
        while current:
            values.append(str(current.value))
            current = current.next
        print("Queue:", " -> ".join(values))