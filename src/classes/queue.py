class ListNode:
    def __init__(self, value=None):
        self.value = value
        self.next = None

class Queue:
    def __init__(self):
        self.root = None   # Empty queue

    def add(self, val):
        newNode = ListNode(val)

        # If queue is empty
        if self.root is None:
            self.root = newNode # bruno
            return

        # Otherwise traverse to the last node
        current = self.root
        while current.next is not None:
            current = current.next

        current.next = newNode

    def length(self):
        result = 0
        current = self.root
        while current is not None:
            result += 1
            current = current.next
        return result

    def is_empty(self):
        return self.root is None
    
    def print(self):
        current = self.root

        while current is not None:
            print(current.value)
            current = current.next

