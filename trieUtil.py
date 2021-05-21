from musicalClasses import *
from node import *

# HELPER FUNCTIONS

# creates new nextArr
def createNewNextArr(prev=None, nodetype='compact'):
    if nodetype == 'compact':
        return np.array([CompactNode(i, prev) for i in range(-maxRange, maxRange+1)])
    else: # regular trie node
        return np.array([Node(i) for i in range(-maxRange, maxRange+1)])

# finds first nonmatching index
def firstNonmatching(base, test):
    '''
    Input: arrays base, test
    Output: first index at which the arrays differ, or
            -1 if all matching up to index min(len(base), len(test))
    '''
    # if either's length is 0 (i.e. None), return -1
    if base is None or test is None: return -1
    
    # go through each element, up to last element in smallest array
    for i in range(min(len(base), len(test))):
        if base[i] != test[i]: return i

    # if we got here, all were equal
    return -1