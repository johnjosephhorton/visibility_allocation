# John Horton                 Jan 5, 2011
# Panagiotis Papadimitriou    Feb 5, 2011

import math, random
from collections import defaultdict

about = """
The basic idea is that if we store the merits in binary tree, we can generate random
weighted samples in ~ log_2 n time. And we don't have to re-normalize merits & we don't have to store floats.

The basic algorithm is this:

1) Take the merits & sort them from greatest to least
2) Place them in a binary tree
3) Give each node the sum of all it's children. Let that number be S.

To draw a value:
1) Start at the parent node
2) Draw a random number r between [0,1]
3) Take the node visibilities S_l and S_r
4) If r < S_l / (S_l + S_r), then go to the left child; otherwise go to the right child
5) If the child is a terminal node, stop and report the agent stored at that terminal node. Fix the tree by subtracting the agent's budget
from all the parent nodes. If the child node landed on is not terminal, repeat from step 2.


Need web scale
return results in real time, in needed order (not possible w/ the matrix decomposition method) 
"""

# code steps

# 1. Construct the binary tree


# 2. 

class Node(object):
  def __init__(self, value=None, terminal=None, index=None, left=None, right=None):
    self.terminal = terminal
    self.value = value                    
    self.index = index                 # used only in terminal nodes
    self.left = left
    self.right = right
    self.to_remove = False
    
  def add_values(self, visibilities, indexes):
    '''Populates the sub-tree rooted at self, so that all visibilities
    are in the leaves
    '''
    assert(len(visibilities) == len(indexes))
    num_values = len(visibilities)
    assert(num_values) > 0
    if num_values == 1:
      # Terminal node
      self.terminal = True
      self.left = self.right = None
      self.value = visibilities[0]
      self.index = indexes[0]
    else:
      # Non-terminal node
      self.terminal = False
      self.left = Node()
      self.right = Node()
      half = num_values / 2
      self.left.add_values(visibilities[:half], indexes[:half])
      self.right.add_values(visibilities[half:], indexes[half:])
      self.value = self.left.value + self.right.value
    
  def get_sample(self):
    assert(self.value != 0)
    if self.terminal:
      index = self.index
      self.value = 0
      self.to_remove = True
    else:
      assert(not(self.left is None and self.right is None))
      def is_empty_node(node):
        return node.terminal and node.to_remove or \
          not node.terminal and node.left is None and node.right is None
         
      left = self.left.value if self.left is not None else -1 
      right = self.right.value if self.right is not None else -1
      rho = self.value * random.random()
      if rho < left:
        index = self.left.get_sample()
        #if self.right is not None:
        #  self.value = self.right.value
        #else:
        #  self.value = 0
        self.value -= left - self.left.value
        if is_empty_node(self.left):
          self.left = None
      else:
        index = self.right.get_sample()
        #if self.left is not None:
        #  self.value = self.left.value
        #else:
        #  self.value = 0 
        self.value -= right - self.right.value
        if is_empty_node(self.right): 
          self.right = None
    return index
  
  def __str__(self):
    if self.terminal:
      return '%.2f' % self.value
    else:
      return '%.2f ( %s | %s )' % (self.value,
                                  '-' if self.left is None else self.left.__str__(),
                                  '-' if self.right is None else self.right.__str__())


class TreeBasedRandomGenerator:
  def __init__(self, visibilities, indexes=None):
    assert(len(visibilities) > 0)
    self.root = Node(terminal=False, value=0)
    self.values = visibilities
    self.indexes = indexes if indexes is not None else range(len(self.values))
    self.reset_weights()
    
  def reset_weights(self):
    self.root.add_values(self.values, self.indexes)

  def get_sample(self):
    assert self.root.value != 0, str(self)
    return self.root.get_sample()
  
  def __str__(self):
    return str(self.root)

def efficient_gen_rank(names, merits, verbose=False):
  assert(len(names)==len(merits))
  generator = TreeBasedRandomGenerator(merits, names)
  assignment = defaultdict(lambda : None)
  for p in range(len(names)):
    name = generator.get_sample()
    assignment[name] = p
  return assignment
 

if __name__ == '__main__':
  visibilities = [0.4, 0.2, 1, 0.1, 10]
  generator = TreeBasedRandomGenerator(visibilities)
  print generator
  for i in range(len(visibilities)):
    index = generator.get_sample()
    print '%d (%.2f)' % (index, visibilities[index])
    print generator

  