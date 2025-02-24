import unittest

def merge(l1, l2):
    '''Merge two sorted lists and return the new merged list.'''
    l3 = []
    i1, i2 = 0, 0
    while i1 < len(l1) and i2 < len(l2):
        if l1[i1] < l2[i2]:
            l3.append(l1[i1])
            i1 += 1
        else:
            l3.append(l2[i2])
            i2 += 1

    while i1 < len(l1):
        l3.append(l1[i1])
        i1 += 1

    while i2 < len(l2):
        l3.append(l2[i2])
        i2 += 1

    return l3


def in_place_merge(l1, l2):
    '''Given two sorted lists, do an in-place merge into l1.

       Assumes l1 has None after the comparable elements,
       which can be replaced. The number of None == len(l2)

       Runtime: O(n := len(l1) + len(l2))
    '''
    n = len(l1)
    n2 = len(l2)
    n1 = n - n2 # The number of non-None elements in l1

    # First, just move all the non-None elements of l1 to the end
    # rather than the beginning. This greatly simplifies the 
    # algorithm, since we don't need to worry about shuffling
    # l1 elements out of the way while merging.
    #
    # This is O(n1). 
    #
    # Don't clear old positions, because if n2 == 0, that 
    # would delete elements.
    for i in range(1, n1 + 1):
        l1[-i] = l1[n1 - i]

    # Now merge into the beginning of list l1
    #
    # Combined, the last two loops are O(n) = O(n1 + n2)
    i, i1, i2 = 0, n2, 0
    while i1 < n and i2 < n2:
        if l1[i1] < l2[i2]:
            l1[i] = l1[i1]
            i1 += 1
        else:
            l1[i] = l2[i2]
            i2 += 1
        i += 1

    # Copy any remaining elements of l2, if there are any.
    # Unlike the new-list merge, we don't have to move
    # anything originally in l1.
    while i2 < n2:
        l1[i] = l2[i2]
        i2 += 1
        i += 1


class TestInPlaceMerge(unittest.TestCase):
    def test_empty_merge(self):
        l1 = []
        l2 = []
        in_place_merge(l1, l2)
        self.assertEqual(l1, [])

    def test_right_half_empty_merge(self):
        l1 = [1,2,3,4]
        l2 = []
        in_place_merge(l1, l2)
        self.assertEqual(l1, [1,2,3,4])

    def test_left_half_empty_merge(self):
        l1 = [None, None, None, None]
        l2 = [1,2,3,4]
        in_place_merge(l1, l2)
        self.assertEqual(l1, [1,2,3,4])

    def test_merge(self):
        l1 = [1,3,5,6,10]
        l2 = [1,2,7,8]
        l3 = list(l1) + [None] * len(l2)
        in_place_merge(l3, l2)
        self.assertEqual(l3, merge(l1, l2))


if __name__ == '__main__':
    unittest.main()
