import sys

class Node:
    def __init__(self, val):
        self.val = val
        self.next = None
        self.prev = None

class DoublyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    def add_front(self, title):
        new_node = Node(title)
        if self.size == 0:
            self.head = self.tail = new_node
        else:
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node
        self.size += 1
        return "ok"

    def add_back(self, title):
        new_node = Node(title)
        if self.size == 0:
            self.head = self.tail = new_node
        else:
            new_node.prev = self.tail
            self.tail.next = new_node
            self.tail = new_node
        self.size += 1
        return "ok"

    def erase_front(self):
        if self.size == 0:
            return "error"
        removed_val = self.head.val
        if self.size == 1:
            self.head = self.tail = None
        else:
            self.head = self.head.next
            self.head.prev = None
        self.size -= 1
        return removed_val

    def erase_back(self):
        if self.size == 0:
            return "error"
        removed_val = self.tail.val
        if self.size == 1:
            self.head = self.tail = None
        else:
            self.tail = self.tail.prev
            self.tail.next = None
        self.size -= 1
        return removed_val

    def front(self):
        if self.size == 0:
            return "error"
        return self.head.val

    def back(self):
        if self.size == 0:
            return "error"
        return self.tail.val

    def clear(self):
        self.head = None
        self.tail = None
        self.size = 0
        return "ok"


def solve():
    dll = DoublyLinkedList()
    
    # Fast I/O reading line by line
    for line in sys.stdin:
        parts = line.strip().split()
        if not parts:
            continue
        
        cmd = parts[0]
        
        if cmd == "add_front":
            print(dll.add_front(parts[1]))
        elif cmd == "add_back":
            print(dll.add_back(parts[1]))
        elif cmd == "erase_front":
            print(dll.erase_front())
        elif cmd == "erase_back":
            print(dll.erase_back())
        elif cmd == "front":
            print(dll.front())
        elif cmd == "back":
            print(dll.back())
        elif cmd == "clear":
            print(dll.clear())
        elif cmd == "exit":
            print("goodbye")
            break

if __name__ == "__main__":
    solve()