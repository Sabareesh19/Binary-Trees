
# coding: utf-8

# In[10]:

class AVLTree:
    class Node:
        def __init__(self, val, left=None, right=None):
            self.val = val
            self.left = left
            self.right = right

        def rotate_right(self):
            n = self.left
            self.val, n.val = n.val, self.val
            self.left, n.left, self.right, n.right = n.left, n.right, n, self.right
            
        def rotate_left(self):
            # YOUR CODE HERE
            n = self.right
            self.val, n.val = n.val, self.val
            self.left,n.left,self.right,n.right = n, self.left,n.right,n.left
            
        
        @staticmethod
        def height(n):
            if not n:
                return 0
            else:
                return max(1+AVLTree.Node.height(n.left), 1+AVLTree.Node.height(n.right))

    def __init__(self):
        self.size = 0
        self.root = None
            
    @staticmethod
    def rebalance(t):
        if AVLTree.Node.height(t.left) > AVLTree.Node.height(t.right):
            if AVLTree.Node.height(t.left.left) >= AVLTree.Node.height(t.left.right):
                # left-left
                #print('left-left imbalance detected')
                t.rotate_right()
            else:
                # left-right
                #print('left-right imbalance detected')
                t.left.rotate_left()
                t.rotate_right()
        else:
            # right branch imbalance tests needed
            if AVLTree.Node.height(t.right.right) >= AVLTree.Node.height(t.right.left):
                #right-right
                #print('right-right imbalance detected')
                t.rotate_left()
            else:
                #right-left
                #print('right-left imbalance detected')
                t.right.rotate_right()
                t.rotate_left()
            
    def add(self, val):
        assert(val not in self)
        def add_rec(node):
            if not node:
                return AVLTree.Node(val)
            elif val < node.val:
                node.left = add_rec(node.left)
            else:
                node.right = add_rec(node.right)
            if abs(AVLTree.Node.height(node.left)-AVLTree.Node.height(node.right))>1: # detect imbalance
                AVLTree.rebalance(node)
            return node
        self.root = add_rec(self.root)
        self.size += 1
        
    def __delitem__(self, val):
        assert(val in self)
        class Stack:
            def __init__(self):
                self.data = []
            def push(self, val):
                self.data.append(val)
            def pop(self):
                assert(len(self.data) >=1)
                ret = self.data[-1]
                del self.data[-1]
                return ret
            def empty(self):
                return len(self.data) == 0
            def __bool__(self):
                return not self.empty()
        
        def delitem_rec(node):
            s = Stack()
            s.push(node)
            if val < node.val:
                s.push(node.left)
                node.left = delitem_rec(node.left)
            elif val > node.val:
                s.push(node.right)
                node.right = delitem_rec(node.right)
            else:
                if not node.left and not node.right:
                    return None
                elif node.left and not node.right:
                    return node.left
                elif node.right and not node.left:
                    return node.right
                else:
                    t = node.left
                    s.push(node.left)
                    if not t.right:
                        node.val = t.val
                        node.left = t.left                        
                    else:
                        n = t
                        while n.right.right:
                            n = n.right
                            s.push(n)
                        t = n.right
                        n.right = t.left
                        s.push(n.right)
                        node.val = t.val
                      
            while s:
                r = s.pop()
                if r is not None:
                    if abs(AVLTree.Node.height(r.left) - AVLTree.Node.height(r.right)) >= 2:
                        AVLTree.rebalance(r)
            return r
                    
        
        self.root = delitem_rec(self.root)
        self.size -= 1
        
    def __contains__(self, val):
        def contains_rec(node):
            if not node:
                return False
            elif val < node.val:
                return contains_rec(node.left)
            elif val > node.val:
                return contains_rec(node.right)
            else:
                return True
        return contains_rec(self.root)
    
    def __len__(self):
        return self.size
    
    def __iter__(self):
        def iter_rec(node):
            if node:
                yield from iter_rec(node.left)
                yield node.val
                yield from iter_rec(node.right)
        yield from iter_rec(self.root)
        
    def pprint(self, width=64):
        """Attempts to pretty-print this tree's contents."""
        height = self.height()
        nodes  = [(self.root, 0)]
        prev_level = 0
        repr_str = ''
        while nodes:
            n,level = nodes.pop(0)
            if prev_level != level:
                prev_level = level
                repr_str += '\n'
            if not n:
                if level < height-1:
                    nodes.extend([(None, level+1), (None, level+1)])
                repr_str += '{val:^{width}}'.format(val='-', width=width//2**level)
            elif n:
                if n.left or level < height-1:
                    nodes.append((n.left, level+1))
                if n.right or level < height-1:
                    nodes.append((n.right, level+1))
                repr_str += '{val:^{width}}'.format(val=n.val, width=width//2**level)
        print(repr_str)
    
    def height(self):
        """Returns the height of the longest branch of the tree."""
        def height_rec(t):
            if not t:
                return 0
            else:
                return max(1+height_rec(t.left), 1+height_rec(t.right))
        return height_rec(self.root)


# In[11]:

t = AVLTree()
for x in [10, 5, 15, 2]:
    t.add(x)
t.pprint()


# In[12]:

del t[15]
t.pprint()


# In[13]:

# LL-fix (simple) test
# 3 points

from unittest import TestCase

def height(t):
    if not t:
        return 0
    else:
        return max(1+height(t.left), 1+height(t.right))

tc = TestCase()
t = AVLTree()

for x in [3, 2, 1]:
    t.add(x)
    
tc.assertEqual(height(t.root), 2)
tc.assertEqual([t.root.left.val, t.root.val, t.root.right.val], [1, 2, 3])


# In[14]:

# RR-fix (simple) test
# 3 points

from unittest import TestCase

def height(t):
    if not t:
        return 0
    else:
        return max(1+height(t.left), 1+height(t.right))

tc = TestCase()
t = AVLTree()

for x in [1, 2, 3]:
    t.add(x)
    
tc.assertEqual(height(t.root), 2)
tc.assertEqual([t.root.left.val, t.root.val, t.root.right.val], [1, 2, 3])


# In[15]:

# LR-fix (simple) test
# 3 points

from unittest import TestCase

def height(t):
    if not t:
        return 0
    else:
        return max(1+height(t.left), 1+height(t.right))

tc = TestCase()
t = AVLTree()

for x in [3, 1, 2]:
    t.add(x)
    
tc.assertEqual(height(t.root), 2)
tc.assertEqual([t.root.left.val, t.root.val, t.root.right.val], [1, 2, 3])


# In[16]:

# RL-fix (simple) test
# 3 points

from unittest import TestCase

def height(t):
    if not t:
        return 0
    else:
        return max(1+height(t.left), 1+height(t.right))

tc = TestCase()
t = AVLTree()

for x in [1, 3, 2]:
    t.add(x)
    
tc.assertEqual(height(t.root), 2)
tc.assertEqual([t.root.left.val, t.root.val, t.root.right.val], [1, 2, 3])


# In[ ]:




# In[17]:

# ensure key order is maintained after insertions and removals
# 15 points

from unittest import TestCase
import random

tc = TestCase()
vals = list(range(0, 100000000, 333333))
random.shuffle(vals)

t = AVLTree()
for x in vals:
    t.add(x)

for _ in range(len(vals) // 3):
    to_rem = vals.pop(random.randrange(len(vals)))
    del t[to_rem]

vals.sort()

for i,val in enumerate(t):
    tc.assertEqual(val, vals[i])


# In[18]:

# stress testing
# 15 points

from unittest import TestCase
import random

tc = TestCase()

def traverse(t, fn):
    if t:
        fn(t)
        traverse(t.left, fn)
        traverse(t.right, fn)

def height(t):
    if not t:
        return 0
    else:
        return max(1+height(t.left), 1+height(t.right))
    
def check_balance(t):
    tc.assertLess(abs(height(t.left) - height(t.right)), 2, 'Tree is out of balance')

t = AVLTree()
vals = list(range(1000))
random.shuffle(vals)
for i in range(len(vals)):
    t.add(vals[i])
    for x in vals[:i+1]:
        tc.assertIn(x, t, 'Element added not in tree')
    traverse(t.root, check_balance)

random.shuffle(vals)
for i in range(len(vals)):
    del t[vals[i]]
    for x in vals[i+1:]:
        tc.assertIn(x, t, 'Incorrect element removed from tree')
    for x in vals[:i+1]:
        tc.assertNotIn(x, t, 'Element removed still in tree')
    traverse(t.root, check_balance)


# In[ ]:




# In[ ]:



