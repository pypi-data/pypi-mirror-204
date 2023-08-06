from btree_index.base import Node


class BTreePrinter:
    def __init__(self, root: Node):
        self.root = root
    
    def _print(self, node: Node, level: int):
        if node is None:
            return
        print(' ' * level, node.keys, node.values)
        if not node.is_leaf:
            for child in node.children:
                self._print(child, level + 1)
        else:
            print(' ' * (level + 1), "Leaf node")
    
    def print(self):
        self._print(self.root, 0)

    def print(self):
        self._print(self.root, 0)
        
    def _print_leaf(self, node: Node, level: int):
        if node is None:
            return
        print(' ' * level, node.keys)
        if not node.is_leaf:
            for child in node.children:
                self._print_leaf(child, level + 1)
                
    def print_leaf(self):
        self._print_leaf(self.root, 0)
        
    def _print_internal(self, node: Node, level: int):
        if node is None:
            return
        print(' ' * level, node.keys)
        if not node.is_leaf:
            for child in node.children:
                self._print_internal(child, level + 1)
                
    def print_internal(self):
        self._print_internal(self.root, 0)
        
    def _print_values(self, node: Node, level: int):
        if node is None:
            return
        print(' ' * level, node.values)
        if not node.is_leaf:
            for child in node.children:
                self._print_values(child, level + 1)
                
    def print_values(self):
        self._print_values(self.root, 0)
        
    def _print_keys(self, node: Node, level: int):
        if node is None:
            return
        print(' ' * level, node.keys)
        if not node.is_leaf:
            for child in node.children:
                self._print_keys(child, level + 1)
                
    def print_keys(self):
        self._print_keys(self.root, 0)
        
    def _print_children(self, node: Node, level: int):
        if node is None:
            return
        print(' ' * level, node.children)
        if not node.is_leaf:
            for child in node.children:
                self._print_children(child, level + 1)
                
    def print_children(self):
        self._print_children(self.root, 0)

