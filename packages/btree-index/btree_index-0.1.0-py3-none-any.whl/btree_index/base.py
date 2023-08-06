from typing import Any, List


class BaseNode:
    def __init__(self, value):
        self.value = value
        self.left_child = None
        self.right_child = None
        self.parent = None

    def add_left_child(self, value):
        self.left_child = BaseNode(value)
        self.left_child.parent = self

    def add_right_child(self, value):
        self.right_child = BaseNode(value)
        self.right_child.parent = self

    def is_leaf(self):
        return (self.left_child is None) and (self.right_child is None)

    def get_sibling(self):
        if self.parent is None:
            return None

        if self.parent.left_child == self:
            return self.parent.right_child

        if self.parent.right_child == self:
            return self.parent.left_child

        return None

    def remove(self):
        if self.parent is None:
            return None

        if self.parent.left_child == self:
            self.parent.left_child = None

        if self.parent.right_child == self:
            self.parent.right_child = None

        self.parent = None
        return self

    def replace_with(self, node):
        if self.parent is None:
            return None

        if self.parent.left_child == self:
            self.parent.left_child = node

        if self.parent.right_child == self:
            self.parent.right_child = node

        node.parent = self.parent
        self.parent = None
        return self

    def connect_to_parent(self, parent):
        self.parent = parent

    def connect_to_left_child(self, left_child):
        if not isinstance(left_child, Node):
            raise TypeError("Expected Node object as left child.")
        self.left_child = left_child
        self.left_child.parent = self

    def connect_to_right_child(self, right_child):
        if not isinstance(right_child, Node):
            raise TypeError("Expected Node object as right child.")
        self.right_child = right_child
        self.right_child.parent = self



class Node(BaseNode):
    def __init__(self, is_leaf: bool):
        self.is_leaf = is_leaf
        self.keys: List[str] = []
        self.values: List[Any] = []
        self.children: List[Node] = []

    def insert_key_value(self, key: str, value: Any):
        raise NotImplementedError

    def insert_child(self, child):
        raise NotImplementedError

    def split(self):
        raise NotImplementedError

    def merge(self):
        raise NotImplementedError

    def __str__(self):
        return f"Node(keys={self.keys}, values={self.values}, children={self.children})"

    def __repr__(self):
        return f"Node(keys={self.keys}, values={self.values}, children={self.children})"


class InternalNode(Node):
    def __init__(self):
        super().__init__(is_leaf=False)

    def insert_key_value(self, key: str, value: Any):
        i = len(self.keys) - 1
        while i >= 0 and key < self.keys[i]:
            i -= 1
        self.keys.insert(i + 1, key)
        self.values.insert(i + 1, value)

    def insert_child(self, child):
        i = len(self.children) - 1
        while i >= 0 and self.children[i].keys[-1] > child.keys[-1]:
            i -= 1
        self.children.insert(i + 1, child)
        
    def is_full(self):
        return len(self.keys) == 100
    
    def split(self):
        new_node = InternalNode()
        new_node.keys = self.keys[50:]
        new_node.values = self.values[50:]
        new_node.children = self.children[50:]
        self.keys = self.keys[:50]
        self.values = self.values[:50]
        self.children = self.children[:50]
        return new_node


class LeafNode(Node):
    def __init__(self):
        super().__init__(is_leaf=True)
        self.prev = None
        self.next = None

    def insert_key_value(self, key: str, value: Any):
        i = len(self.keys) - 1
        while i >= 0 and key < self.keys[i]:
            i -= 1
        self.keys.insert(i + 1, key)
        self.values.insert(i + 1, value)

    def is_full(self):
        return len(self.keys) == 100

    def split(self):
        new_node = LeafNode()
        new_node.keys = self.keys[50:]
        new_node.values = self.values[50:]
        new_node.prev = self
        new_node.next = self.next
        self.keys = self.keys[:50]
        self.values = self.values[:50]
        self.next = new_node
        return new_node
    
    def merge(self):
        if self.next is None:
            return None
        self.keys.extend(self.next.keys)
        self.values.extend(self.next.values)
        self.next = self.next.next
        return self.next
    
    def __repr__(self):
        return f'LeafNode({self.keys}, {self.values})'
    
    
    