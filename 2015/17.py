









import math
import time

from line_profiler import profile


class Node:
  '''
    NOTE: index is hardcoded to start with, we'll come
          back to it later.

    :param value: the value of the node
    :param index: the index of the value in the list
                  used to construct the tree
  '''
  def __init__(self, value, index=0):
    self.value = value
    self.index = index
    self.children = []

  def __str__(self):
    return f"value: {self.value}, children: {len(self.children)}"


class TreeGenerator:
  def __init__(self, all_values):
    self.all_values = all_values

    self.obj_trees = []
    self.dict_trees = {}

    self.count = 0
    self.exp = math.factorial(len(all_values))

  def generate_objects(self):
    self._generate_tree_objects(self.all_values, None)
  
  def generate_dicts(self):
    self._generate_tree_dicts(self.all_values, self.dict_trees)

  # @profile
  def _generate_tree_objects(self, values, node):
    '''
      Basic idea is to iterate through all values in
      the list, each value is made into a new node
      and every other value becomes its children, and
      the same process is then repeated for said children.

      This should allow us to find all permutations of
      the given values.

      For example if we take [1, 2, 3] and start with 1
      the children would be [2, 3] then for 2 [3] and for
      3 [2] to get a tree of:
              1
            2   3
            3   2

      We'd then repeat this same process for both 2 and 3.

      NOTE: this has been manually tested at a smaller scale,
            and we think the logic checks out, but not 100%
            as the size of the list grows.
    '''
    # TODO: come back to the index value after we have
    #       the rest of the generator imlpemented, as
    #       I feel like it could be a pain. Also we
    #       may think of a better idea as we've not
    #       thought through the pros/cons of the index
    #       idea yet.
    for i in range(len(values)):      
      new_node = Node(values[i])

      if node is None:
        # print(f"new root: {new_node}")
        self.obj_trees.append(new_node)
      else:
        node.children.append(new_node)

      self.count += 1
      # print(f"{self.count}/{self.exp}")

      child_values = values[0:i] + values[(i + 1):]
      self._generate_tree_objects(child_values, new_node)

  @profile
  def _generate_tree_dicts(self, values, node):  
    for i in range(len(values)):      
      # value = values[i]
      # node[value] = {}

      # self.count += 1
      # print(f"{self.count}/{self.exp}")

      child_values = values[0:i] + values[(i + 1):]
      # self._generate_tree_dicts(child_values, node[value])
      self._generate_tree_dicts(child_values, None)

  # def test(self):
  #   for i in range(len(self.all_values)):
  #     child_values = self.all_values[0:i] + self.all_values[(i + 1):]
  #     self._generate_tree_dicts(child_values, None)
  #     break

def print_node(node):
  print(node)

  for i in node.children:
    print_node(i)

# @profile
def test_objects(values):
  print("testing objects")

  st = time.time()
  t = TreeGenerator(values)
  t.generate_objects()
  print(time.time() - st)

# @profile
def test_dict(values):
  print(f"testing dicts - {len(values)} - {values}")

  st = time.time()
  t = TreeGenerator(values)
  t.generate_dicts()
  # t.test()
  # print(t.dict_trees)
  print(time.time() - st)


def test():
  '''
    from testing using dicts is way faster,
    for a list of 10:
      - objects: 77-seconds
      - dicts: 6-seconds

    makes sense, creating objects is expensive and from
    profiling are the creating of Node() is taking up 
    27.3-seconds of the time. The other main factor
    is creating the child list, which takes up 29.3-seconds.
    
    we tried cProfile to start but didn't get a line by line
    breakdown, so we're using this instead: https://stackoverflow.com/a/62382967

    what's interesting, and annoying, is that if we time using time()
    then for a list of 9 we have ~0.8s but that jumps upto ~9s for a
    list of 10...

    we also can't go upto 11, since we had a hard-crash...no response
    at all, we had to turn off and on again...

    re-running at 11, the issue seems to be memory we can see memory
    not so slowing creeping up.

    technically we could work out applicible combinations/permuations
    as we're building the tree up. Lets run again without storing
    values.

    okay so re-running without storing in memory 11 goes upto 37,
    we stopped running 12 after a while as it was taking for to
    long to finish.

    what this technically means though is if we stay under 10 well
    under a second (drops to 0.35s without storing) so I wonder if
    we could use mulitple-procs for this?

    for multi-proces every child we encountered we'd split up
    so that it's always under 10 items, then we'd submit those
    to a manager that would kick off a process.

    The issue is right now we're recurssive, so we'd have a single
    entry point hogging everything.

    can we change the struct? what if we return a list of all new nodes
    and their children? then we have the option to manually recall
    with those. Not sure, it feels inheiorntly recusrsive since if
    we return the children then we'd also want to get there children
    and then their children etc. etc.

    also, I don't think we can split up the list as we'd end up
    missining permuations as the whole idea is that the child
    values are EVERY other item at that level.

    what we potentially could do is process every entry point at
    once. So for the intial values work out the original children
    and then put each of those into it's own thread.

    how long does a single value tree take to generate? we need
    to be able to go upto 20 for the challenge input.

    working out the tree for a single item when theres 12 overall
    takes 37s, which is an increase from 3s at 11 overall items
    so def not going to work for 20 overall items.

    ahh fuck, okay, so this approach isn't going to work unless
    we can somehow split the list up - which we don't think we
    can do right now without missing permuations.

    could we parallelize creating the child values? so:
      - have a loop that for each value creates a new proc that creates the child values
      - then another loop th actually iterate over the children 

    possibly, how long does it take to create the children?
    it takes ~24% of the time. So a decent chunk I don't think
    enough to make the approach workable.

    TODO: add a prefix instead of a previous node so that we can
          track the previous values.
  '''
  # values = []

  # NOTE: from test
  # test_objects(values)


  for i in range(10, 11):
    values = [j for j in range(1, i + 1)]
    test_dict(values)


if __name__ == "__main__":
  test()









def find_combos(values, target):
  '''
    Disregarding all the christmas stuff, what we're trying
    todo here is find all possible combinations with the given
    values that add up to exactly the target value.

    We could just brute-force this, but there's def a maths
    approach to this. I'm 90% sure this is a combinatorics so
    lets do some research on that.

    From what we've seen this this only tells us the number
    of possible combinations. We could work backwards from
    this and remove all combinations that dont add up to
    exactly the target, but that doesn't feel any better since
    we'd still have to search through all combos.

    TODO: implement tree idea

    TODO: implement tree

    TODO: walk tree to find permuations

    TODO: filter tree for combinations
      - see notes below

    TODO: document solution, i.e. copy notes and graphs
          over into this repo so we can look back and
          understand what we've implemented
  '''
  pass


def main():
  # TODO: for testing start small with the example they give,
  #       so that we can know if it's working.
  # 
  # NOTE: idea for allowing duplicates, like [5, 5, 20] produces
  #       [5, 20] twice so we can't just eliminate based on values
  #       within, at the same time we don't want to allow [20, 5]
  #       as I don't think the order matters.
  # 
  #       instead of doing it just based on value we could also
  #       include the index, and then check if it's the same combo
  #       that way, i.e. [(5, 0), (20, 2)] vs [(5, 1), (20, 2)]
  #       are different combinations. Then if we were to sort them
  #       we could eliminate any dupliactes that way, e.g.
  #         unsorted: [(5, 1), (20, 2)] and [(20, 2), (5, 1)]
  #         sorted:   [(5, 1), (20, 2)] and [(5, 1), (20, 2)]
  #       
  #       as we can see, sorting would allow us to see different
  #       permuations of the same indexes, which we don't want.
  #       we want unique combinations across different indexes.
  # 
  # NOTE: the above would be after we've implemented the tree, and 
  #       after we've walked through and found all permuations, it
  #       would be a filtering stage at the end.
  containers = [
    43, 3, 4, 10, 21, 44, 4, 6, 47, 41, 34, 17, 17, 44, 36, 31, 46, 9, 27, 38
  ]
  target = 150


# if __name__ == "__main__":
#   main()