class BST(object):
    #inner Node objects
    class Node(object):
        def __init__(self, data, left=None, right=None):
            self.left = left
            self.right = right
            self.data = data
        #allow iteration through data like
        #for i in tree: ...
        def __iter__(self):
            if self.left != None:
                #call __iter__ on left subtree
                for i in self.left:
                    yield i
            yield self.data
            if self.right != None:
                #call __iter__ on right subtree
                for i in self.right:
                    yield i
                
    def __init__(self, root=None):
        self.root = root
    def add(self, item):
        self.root = BST._add(self.root, item)
    def _add(root, item):
        if root == None:
            #make a new node to get inserted
            return BST.Node(item)
        #add to left for smaller data
        if item < root.data:
            root.left = BST._add(root.left, item)
        #add to right for bigger or equal data
        else:
            root.right = BST._add(root.right, item)
        return root
    #iterate through values in tree
    def __iter__(self):
        if self.root != None:
            return iter(self.root)
        else:
            return iter([])
    #quick check for item presence in tree
    def contains(self, item):
        return BST._contains(self.root, item)
    def _contains(root, item):
        if root == None:
            return False
        elif item < root.data:
            return BST._contains(root.left, item)
        elif item > root.data:
            return BST._contains(root.right, item)
        else:
            return True
