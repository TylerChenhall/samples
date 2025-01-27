from collections import deque

class SplitQueue:
    '''A queue supporting efficient removal of the center element.

       Originally inspired by a problem on https://adventofcode.com/'''
    # TODO: maybe make this a valid iterable?
    # maybe make this initializable
    # Write some tests

    def __init__(self):
        self._left = deque()
        self._right = deque()

    def pop(self):
        # Generally, we pop from self._right. However, if only
        # one element remains, it will be stored in self._left
        el = self._right.pop() if len(self._right) > 0 else self._left.pop()
        self._rebalance()
        return el

    def append(self, el):
        self._right.append(el)
        self._rebalance()

    def popleft(self):
        el = self._left.popleft()
        self._rebalance()
        return el

    def appendleft(self, el):
        self._left.appendleft(el)
        self._rebalance()

    def popmiddle(self):
        el = self._left.pop()
        self._rebalance()
        return el

    def __len__(self):
        return len(self._left) + len(self._right)

    def _rebalance(self):
        '''Rebalance so the left and right queues share elements equally.

           When len is odd, the extra element is stored in the left queue.'''
        shift = (len(self._left) + len(self._right)) % 2
        while len(self._left) > shift + len(self._right):
            self._right.appendleft(self._left.pop())
        while len(self._left) < shift + len(self._right):
            self._left.append(self._right.popleft())
    
