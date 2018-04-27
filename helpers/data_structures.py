"""
Collection of data structures
"""


class TrieNode:
    def __init__(self, val):
        self.value = val
        self.children = {}


class Trie:
    def __init__(self):
        self.root = TrieNode(None)
        self.items_count = 0

    def insert(self, iterable, value=None, parent=None):
        if len(iterable) == 0:
            # TODO: do something clever
            raise Exception("can't send empty item")
        if parent is None:
            parent = self.root
        if len(iterable) == 1:
            parent.children[iterable[0]] = TrieNode(value)
            return
        if parent.children.get(iterable[0]) is None:
            parent.children[iterable[0]] = TrieNode(None)
        self.insert(iterable[1:], value, parent.children[iterable[0]])

    def preorder(self, node):
        lst = []
        if node is None:
            return []
        lst.append(node.value)
        children = node.children
        childkeys = list(children.keys())
        if len(childkeys) == 0:
            rightmost = None
            leftones = []
        elif len(childkeys) == 1:
            rightmost = None
            leftones = childkeys[0]
        else:
            rightmost = children[childkeys[-1]]
            leftones = childkeys[:-1]
        print(leftones)
        for each in leftones:
            lst.append(self.preorder(node.children[each]))
        lst.extend(self.preorder(rightmost))
        return lst

    def __str__(self):
        return "Not yet implemented"


class DictWithCounter(dict):
    def __init__(self, *args, **kwargs):
        self.__count = 0
        super().__init__(*args, **kwargs)

    def __setitem__(self, key, value):
        if not self.get(key):
            self.__count += 1
        super().__setitem__(key, value)

    @property
    def count(self):
        return self.__count
    # TODO: implement __delitem__ to reduce count


class Node:
    def __init__(self, val):
        self.value = val
        self.left = None
        self.right = None


class TreeWithNodeCounts:
    def __init__(self):
        self.nodes_count = 0
        self.root = None

    def _insert_right(self, value, compareNode):
        if compareNode.right is None:
            compareNode.right = Node((value, self.nodes_count))
            self.nodes_count += 1
            return
        else:
            return self.insert(value, compareNode.right)

    def _insert_left(self, value, compareNode):
        if compareNode.left is None:
            compareNode.left = Node((value, self.nodes_count))
            self.nodes_count += 1
            return
        else:
            return self.insert(value, compareNode.left)

    def insert(self, value, compareNode=None):
        if not compareNode and self.root is None:
            self.root = Node((value, self.nodes_count))
            self.nodes_count += 1
            return
        elif not compareNode and self.root:
            return self.insert(value, self.root)
        else:  # compareNode present
            if value >= compareNode.value[0]:
                return self._insert_right(value, compareNode)
            else:
                return self._insert_left(value, compareNode)
