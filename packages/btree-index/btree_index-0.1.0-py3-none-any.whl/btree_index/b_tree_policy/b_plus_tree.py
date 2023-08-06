from typing import Any, Tuple, List, Optional
from btree_index.base import Node, InternalNode, LeafNode 


class BPlusTree:
    def __init__(self,  size = 4):
        self.size = size
        self.root = None
        self.max_keys = size - 1

    def search(self, key: str) -> Optional[Any]:
        if self.root is None:
            return None
        return self._search(self.root, key)

    def _search(self, node: Node, key: str) -> Optional[Any]:
        if node.is_leaf:
            for i in range(len(node.keys)):
                if node.keys[i] == key:
                    return node.values[i]
            return None
        else:
            i = 0
            while i < len(node.keys) and key > node.keys[i]:
                i += 1
            if i == 0 and key < node.keys[i]:
                return self._search(node.children[0], key)
            elif i == len(node.keys):
                return self._search(node.children[-1], key)
            else:
                return self._search(node.children[i], key)


    def insert(self, key: str, value: Any):
        if self.root is None:
            self.root = LeafNode()
            self.root.insert_key_value(key, value)
        else:
            if self.root.is_full():
                new_root = InternalNode()
                new_root.children.append(self.root)
                self.root = new_root
                self._split_child(new_root, 0)
            self._insert(self.root, key, value)

    def _insert(self, node: Node, key: str, value: Any):
        if node.is_leaf:
            node.insert_key_value(key, value)
            if node.is_full():
                self._split_leaf(node)
        else:
            i = 0
            while i < len(node.keys) and key > node.keys[i]:
                i += 1
            if node.children[i].is_full():
                self._split_child(node, i)
                if key > node.keys[i]:
                    i += 1
            self._insert(node.children[i], key, value)

    def delete(self, key: str):
        if self.root is None:
            return
        self._delete(self.root, key)
        if len(self.root.keys) == 0:
            if self.root.is_leaf:
                self.root = None
            else:
                self.root = self.root.children[0]

    def _delete(self, node: Node, key: str):
        if node.is_leaf:
            for i in range(len(node.keys)):
                if node.keys[i] == key:
                    node.keys.pop(i)
                    node.values.pop(i)
                    return
        else:
            i = 0
            while i < len(node.keys) and key > node.keys[i]:
                i += 1
            if i < len(node.keys) and node.keys[i] == key:
                if len(node.children[i].keys) >= self.t:
                    pred = self._find_predecessor(node.children[i])
                    node.keys[i] = pred
                    self._delete(node.children[i], pred)
                elif len(node.children[i + 1].keys) >= self.t:
                    succ = self._find_successor(node.children[i + 1])
                    node.keys[i] = succ
                    self._delete(node.children[i + 1], succ)
                else:
                    self._merge(node, i)
                    self._delete(node.children[i], key)
            else:
                if len(node.children[i].keys) == self.t - 1:
                    if i > 0 and len(node.children[i - 1].keys) >= self.t:
                        self._borrow_from_left(node, i)
                    elif i < len(node.keys) and len(node.children[i + 1].keys) >= self.t:
                        self._borrow_from_right(node, i)
                    else:
                        if i < len(node.keys):
                            self._merge(node, i)
                        else:
                            self._merge(node, i - 1)
                        i -= 1
                self._delete(node.children[i], key)
                
    def _split_leaf(self, node: LeafNode):
        mid = len(node.keys) // 2
        left = LeafNode()
        left.keys = node.keys[:mid]
        left.values = node.values[:mid]
        right = LeafNode()
        right.keys = node.keys[mid:]
        right.values = node.values[mid:]
        left.next = right
        right.prev = left
        if node.prev is not None:
            node.prev.next = left
        if node.next is not None:
            node.next.prev = right
        node.keys = []
        node.values = []
        node.children = [left, right]
        if node.prev is None:
            self.root = node
            
    def _split_child(self, node: InternalNode, i: int):
        child = node.children[i]
        mid = len(child.keys) // 2
        left = InternalNode()
        left.keys = child.keys[:mid]
        left.children = child.children[:mid + 1]
        right = InternalNode()
        right.keys = child.keys[mid + 1:]
        right.children = child.children[mid + 1:]
        node.keys.insert(i, child.keys[mid])
        node.children[i] = left
        node.children.insert(i + 1, right)
        
    def _find_predecessor(self, node: Node) -> str:
        while not node.is_leaf:
            node = node.children[-1]
        return node.keys[-1]
    
    def _find_successor(self, node: Node) -> str:
        while not node.is_leaf:
            node = node.children[0]
        return node.keys[0]
    
    def _merge(self, node: InternalNode, i: int):
        left = node.children[i]
        right = node.children[i + 1]
        left.keys.append(node.keys[i])
        left.keys.extend(right.keys)
        left.children.extend(right.children)
        node.keys.pop(i)
        node.children.pop(i + 1)
        
    def _borrow_from_left(self, node: InternalNode, i: int):
        child = node.children[i]
        left = node.children[i - 1]
        child.keys.insert(0, node.keys[i - 1])
        node.keys[i - 1] = left.keys.pop()
        child.children.insert(0, left.children.pop())
        
    def _borrow_from_right(self, node: InternalNode, i: int):
        child = node.children[i]
        right = node.children[i + 1]
        child.keys.append(node.keys[i])
        node.keys[i] = right.keys.pop(0)
        child.children.append(right.children.pop(0))
        
        
    def get_range(self, start: str, end: str) -> List[Tuple[str, Any]]:
        if self.root is None:
            return []
        return self._get_range(self.root, start, end)
    
    def _get_range(self, node: Node, start: str, end: str) -> List[Tuple[str, Any]]:
        if node.is_leaf:
            return self._get_range_leaf(node, start, end)
        else:
            return self._get_range_internal(node, start, end)
        

    def _get_range_leaf(self, node: LeafNode, start: str, end: str) -> List[Tuple[str, Any]]:
            result = []
            while node is not None:
                for i in range(len(node.keys)):
                    if start <= node.keys[i] <= end:
                        result.append((node.keys[i], node.values[i]))
                node = node.next
            return result
        
    def _get_range_internal(self, node: InternalNode, start: str, end: str) -> List[Tuple[str, Any]]:
        i = 0
        while i < len(node.keys) and start > node.keys[i]:
            i += 1
        if i == len(node.keys) or end < node.keys[i]:
            return self._get_range(node.children[i], start, end)
        else:
            return self._get_range(node.children[i], start, end) + self._get_range(node.children[i + 1], start, end)
        
    def get(self, key: str) -> Any:
        if self.root is None:
            return None
        return self._get(self.root, key)
    
    def _get(self, node: Node, key: str) -> Any:
        if node.is_leaf:
            return self._get_leaf(node, key)
        else:
            return self._get_internal(node, key)
        
    def _get_leaf(self, node: LeafNode, key: str) -> Any:
        for i in range(len(node.keys)):
            if key == node.keys[i]:
                return node.values[i]
        return None
    
    def _get_internal(self, node: InternalNode, key: str) -> Any:
        i = 0
        while i < len(node.keys) and key > node.keys[i]:
            i += 1
        return self._get(node.children[i], key)
    
    def __str__(self):
        if self.root is None:
            return ''
        return self._str(self.root)
        
    def _str(self, node: Node, level: int = 0) -> str:
        if node.is_leaf:
            return self._str_leaf(node, level)
        else:
            return self._str_internal(node, level)
        
    def _str_leaf(self, node: LeafNode, level: int) -> str:
        result = ' ' * level + str(node.keys) + ' ' + str(node.values) + ' ' + str(node.prev is not None) + ' ' + str(node.next is not None)
        
        if node.next is not None:
            result += '\n' + self._str_leaf(node.next, level)

        return result
    
    def _str_internal(self, node: InternalNode, level: int) -> str:
        result = ' ' * level + str(node.keys)
        for child in node.children:
            result += '\n' + self._str(child, level + 1)
        return result
    
    
    def _check(self):
        if self.root is None:
            return
        self._check_node(self.root)
        
    def _check_node(self, node: Node):
        if node.is_leaf:
            self._check_leaf(node)
        else:
            self._check_internal(node)
            
            
    def _check_leaf(self, node: LeafNode):
        if node.prev is not None:
            assert node.prev.next == node
        if node.next is not None:
            assert node.next.prev == node
        for i in range(len(node.keys) - 1):
            assert node.keys[i] < node.keys[i + 1]
            
    def _check_internal(self, node: InternalNode):      
        for i in range(len(node.keys) - 1):
            assert node.keys[i] < node.keys[i + 1]
        for i in range(len(node.keys)):
            self._check_node(node.children[i])
            assert node.keys[i] == node.children[i + 1].keys[0]
            
    def _check_order(self):
        if self.root is None:
            return
        self._check_order_node(self.root)
        
    def _check_order_node(self, node: Node):
        if node.is_leaf:
            self._check_order_leaf(node)
        else:
            self._check_order_internal(node)    
            
    def _check_order_leaf(self, node: LeafNode):
        if node.prev is not None:
            assert node.prev.keys[-1] < node.keys[0]
        if node.next is not None:
            assert node.keys[-1] < node.next.keys[0]

    def _check_order_internal(self, node: InternalNode):
        for i in range(len(node.keys)):
            self._check_order_node(node.children[i])
            assert node.keys[i] == node.children[i + 1].keys[0]
            
    def _check_size(self):
        if self.root is None:
            return
        self._check_size_node(self.root)

    def _check_size_node(self, node: Node):
        if node.is_leaf:
            self._check_size_leaf(node)
        else:
            self._check_size_internal(node)
            
    def _check_size_leaf(self, node: LeafNode):
        assert len(node.keys) <= self.max_keys
        assert len(node.values) <= self.max_keys
        
    def _check_size_internal(self, node: InternalNode):
        assert len(node.keys) <= self.max_keys
        for child in node.children:
            self._check_size_node(child)
            
    def _check_root(self):
        if self.root is None:
            return
        assert self.root.parent is None
        assert self.root.is_leaf or len(self.root.keys) >= 1
        
    def _check_all(self):
        self._check()
        self._check_order()
        self._check_size()
        self._check_root()
        
    def _check_all_leaf(self):
        self._check()
        self._check_order_leaf()
        self._check_size()
        self._check_root()
        
    def _check_all_internal(self):
        self._check()
        self._check_order_internal()
        self._check_size()
        self._check_root()  
        
    def _check_all_node(self):
        self._check()
        self._check_order_node()
        self._check_size()
        self._check_root()

