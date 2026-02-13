class Node:
    def __init__(self, val, next = None):
        self.val = val
        self.next = next
        
class Stack:
    def __init__(self):
        self.head = None

    def push(self, item):
        new = Node(item)
        new.next = self.head
        self.head = new

    def pop(self):
        if self.head is None:
            return None
        value = self.head.val
        self.head = self.head.next
        return value
    
    def is_empty(self):
        return self.head is None

class Queue:
    def __init__(self):
        self.front = None
        self.back = None

    def push(self, val):
        new = Node(val)
        if self.back is None:
            self.front = self.back = new
            return
        self.back.next = new
        self.back = new

    def pop_left(self):
        if self.front is None:
            return None
        value = self.front.val
        self.front = self.front.next
        if self.front is None:
            self.back = None
        return value

    def is_empty(self):
        return self.front is None