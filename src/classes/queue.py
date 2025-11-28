import random

class ListNode:
    def __init__(self, value=None):
        self.value = value
        self.next = None

class Queue:
    def __init__(self):
        self.front = None   # First node
        self.rear = None    # Last node
        self._size = 0      # Track size for O(1) length access

    def is_empty(self):
        return self.front is None

    def add(self, value):
        new_node = ListNode(value)
        if self.is_empty():
            self.front = new_node
            self.rear = new_node
        else:
            self.rear.next = new_node
            self.rear = new_node
        self._size += 1

    def remove(self):  # Dequeue (remove first)
        if self.is_empty():
            return None
        
        value = self.front.value
        self.front = self.front.next
        self._size -= 1
        
        if self.front is None:
            self.rear = None
            
        return value

    def remove_at_index(self, index):
        """Removes a node at a specific index."""
        if index < 0 or index >= self._size or self.is_empty():
            return

        if index == 0:
            self.remove()
            return

        current = self.front
        # Stop at the node BEFORE the one we want to remove
        for _ in range(index - 1):
            current = current.next
        
        # current is now the node before the target
        node_to_remove = current.next
        current.next = node_to_remove.next
        
        # If we removed the last node, update rear
        if current.next is None:
            self.rear = current
            
        self._size -= 1

    def move_node(self, from_index, to_index):
        """Moves a node from index K to index L."""
        if from_index == to_index or from_index < 0 or to_index < 0:
            return
        if from_index >= self._size or to_index >= self._size:
            return

        # 1. Extract the node
        target_node = None
        
        # Special case: Remove head
        if from_index == 0:
            target_node = self.front
            self.front = self.front.next
            if self.front is None: self.rear = None
        else:
            prev = self.front
            for _ in range(from_index - 1):
                prev = prev.next
            target_node = prev.next
            prev.next = target_node.next
            if prev.next is None: self.rear = prev
            
        # 2. Insert the node at to_index
        if to_index == 0:
            target_node.next = self.front
            self.front = target_node
            if self.rear is None: self.rear = target_node
        else:
            prev = self.front
            for _ in range(to_index - 1):
                prev = prev.next
            
            target_node.next = prev.next
            prev.next = target_node
            if target_node.next is None: self.rear = target_node

    def clear(self):
        self.front = None
        self.rear = None
        self._size = 0

    def get_all(self):
        """Returns a standard list of all values (for debug/display)"""
        items = []
        current = self.front
        while current:
            items.append(current.value)
            current = current.next
        return items

    def length(self):
        return self._size