import time

class Consecutive(object):
    '''
    check if there are a number of consecutive entries within an
    interval of time
    
    Consecutive: x and y are consecutive if |x - y| = 1
    '''
    def __init__(self):
        self.record = {}

    def insert(self, entry, con, t, rmin, rmax):
        '''
        check if there are 'con' number of consecutive entries within
        an interval of 'time' seconds

        params:
            entry           object to be inserted
            con             number of consecutive entries
            t               in seconds
            rmin            minimum possible value of entry
            rmax            maximum possible value of entry
        returns:
            True if there are con number of consecutive entries
            (between rmin and rmax) that were inserted within time
            seconds of the present entry being inserted, False
            otherwise
        preconditions:
            difference operator, -, must be defined on entries
            comparison operators, < and ==, must be defined on entries
            con > 0
        '''
        
        # add or update entry
        entry_time = time.time()
        self.record[entry] = entry_time

        # base case: 1 - insertion automatically means 1 con entry
        if con <= 1:
            return True

        # calculate left and right ends
        left, right = max(entry - con + 1, rmin), min(entry + con - 1, rmax)

        # base case: 2 - left and right ends should be able to contain at least con entries
        if right - left + 1 < con:
            return False

        # set up buckets and time constraint for counting
        buckets = [0] * (right - left + 1)
        max_time = entry_time - t
        
        # fill entries in the buckets
        for k, v in self.record.iteritems():
            if v >= max_time and left <= k <= right:
                buckets[k - left] = 1

        # check if we have 'con' consecutive entries
        return sum(buckets[:con]) == con or sum(buckets[-con:]) == con