
class StackNode:
    def __init__(self, data):
        self.data = data
        self.next = None

class Stack:
    def __init__(self):
        self.top = None

    def is_empty(self):
        return self.top is None

    def push(self, data):
        new_node = StackNode(data)
        new_node.next = self.top
        self.top = new_node

    def pop(self):
        if self.is_empty():
            return None
        popped_node = self.top
        self.top = self.top.next
        return popped_node.data

    def peek(self):
        if self.is_empty():
            return None
        return self.top.data
    
    # Define a way to access it with [], it must work with negative indices too
    def __getitem__(self, index):
        current = self.top
        count = 0
        while current:
            if count == index:
                return current.data
            current = current.next
            count += 1
        raise IndexError("Stack index out of range")

    def __len__(self):
        current = self.top
        length = 0
        while current:
            length += 1
            current = current.next
        return length

    def __getitem__(self, index):
        if index < 0:
            index = len(self) + index
        current = self.top
        count = 0
        while current:
            if count == index:
                return current.data
            current = current.next
            count += 1
        raise IndexError("Stack index out of range")