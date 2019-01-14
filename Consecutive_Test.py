from Consecutive import *
import time
import sys
import unittest

class Con_Tests(unittest.TestCase):
    '''
    a light set of tests for class Consecutive

    Testing strategy

    Partition the input as follows:
    entry       int
    N           0, 1, > 1
    con         0, 1, 2, > 2, < N, == N, > N
    t           0, > 0, inf
    rmin        < 0, 0, > 0, max(entry), > max(entry), neighboured by consecutive entries
    rmax        < 0, 0, > 0, < rmin, == rmin, > rmin, min(entry), < min(entry), neighboured by consecutive entries

    result      True, False

    Coverage: cover each part.

    N: number of entries inserted before the current one.    
    '''


    # covers    int
    #           0, 1, > 1
    #           > 2, > N
    #           inf
    #           0, max(entry)
    #           > 0, > rmin
    #           False
    def testConTooLarge(self):
        c = Consecutive()
        for i in range(9):
            self.assertFalse(c.insert(i, 10, 1000, 0, 10))

    # covers    int
    #           0, 1, > 1
    #           2, > N, == N, < N
    #           inf
    #           0, max(entry, > max(entry), neighboured by consecutive entries
    #           > 0, > rmin, neighboured by consecutive entries
    #           False
    def testNoConsecutive(self):
        c = Consecutive()
        for i in range(-19, 45):
            self.assertFalse(c.insert(i * 2, 2, 1000, 0, 40))

    # covers    int
    #           > 1
    #           == N
    #           > 0
    #           < 0
    #           > 0, > rmin
    #           False
    def testNotRecent(self):
        c = Consecutive()
        for i in range(9):
            c.insert(i, 10, 1, -10, 20)
        time.sleep(2.0)
        self.assertFalse(c.insert(9, 10, 1, -10, 20))

    # covers    int
    #           0, 1, > 1
    #           2, < N, == N, > N
    #           inf
    #           max(entry), > max(entry)
    #           > 0, < rmin, == rmin, > rmin
    #           False
    def testNotAboveRmin(self):
        c = Consecutive()
        for i in range(5):
            self.assertFalse(c.insert(i, 2, 1000, i, 9))
        for i in range(5, 10):
            self.assertFalse(c.insert(i, 2, 1000, i + 1, 9))

    # covers    int
    #           0, 1, > 1
    #           > 2, < N, == N, > N
    #           inf
    #           0
    #           < 0, 0, > 0, == rmin, > rmin, min(entry), < min(entry), neighboured by consecutive entries
    #           False
    def testNotBelowRmax(self):
        c = Consecutive()
        for i in range(5):
            self.assertFalse(c.insert(i, 3, 1000, 0, 1))
        for i in range(5, 7):
            self.assertFalse(c.insert(i, 3, 1000, 0, 0))
        for i in range(7, 9):
            self.assertFalse(c.insert(i, 3, 1000, -20, -1))

    # covers    int
    #           0, 1, > 1
    #           0, 1, > N
    #           0, inf
    #           0
    #           > 0, > rmin
    #           True
    def testConPresent(self):
        c = Consecutive()
        for i in range(10):
            self.assertTrue(c.insert(i, i, 1000, 0, 9))
        time.sleep(1.0)
        self.assertTrue(c.insert(10, 1, 0, 9, 11))

if __name__ == '__main__':
    unittest.main()