"""
This is NOT my code. I borrowed it from here:
    http://www.evanfosmark.com/2009/11/python-markov-chains-and-how-to-use-them/
"""

import collections
import random
 
 
class DynamicDie(collections.defaultdict):
 
    def __init__(self, *args, **kwargs):
        collections.defaultdict.__init__(self, int)
 
    def add_side(self, side):
        self[side] += 1
 
    def total_sides(self):
        return sum(self.values())
 
    def roll(self):
        random_num = random.randint(0, self.total_sides())
        total_pos = 0
        for side, qty in self.items():
            total_pos += qty
            if random_num <= total_pos:
                return side
 
class Start(object): pass
class End(object): pass
class MarkovChain(collections.defaultdict):
    """ Yet another markov chain implementation.
        This one differs in the sense that it is able to better support
        huge amounts of data since the weighted randomization doesn't rely
        on duplicates.
    """
 
    # Sentinals 
    # Discussion here: http://stackoverflow.com/questions/1677726

    START = Start
    END = End

 
    def __init__(self, order=3, *args, **kwargs):
        collections.defaultdict.__init__(self, DynamicDie)
        self.order = order
 
    def add(self, iterable):
        """ Insert an iterable (pattern) item into the markov chain.
            The order of the pattern will define more of the chain.
        """
        items = []
        for i in range(self.order - 1):
            items.append(MarkovChain.START)
        for item in iterable:
            self[tuple(items)].add_side(item)
            items.insert(0, item)
            items.pop()
        self[tuple(items)].add_side(MarkovChain.END)
 
    def random_output(self, max=100):
        """ Generate a list of elements from the markov chain.
            The `max` value is in place in order to prevent excessive iteration.
        """
        output = []
        items = []
        for i in range(self.order - 1):
            items.append(MarkovChain.START)
        for i in range(max - (self.order - 1)):
            item = self[tuple(items)].roll()
            if item is MarkovChain.END:
                break
            output.append(item)
            items.insert(0, item)
            items.pop()
        return output
