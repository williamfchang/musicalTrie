
from musicalClasses import ivlToIdx

class Node:
    def __init__(self, interval, nextArr=None):
        self.interval = interval
        self.nextArr = nextArr
        
        # for if there is an item that terminates at this node
        # TODO: may need to make this an array
        self.terminalValue = None
        
        # to keep track of most searched item
        # also used for matching with searches that are only first half of the melody, etc.
        self.mostSearched = None
    
    def __str__(self):
        hasNext = 'no' if self.nextArr is None else 'a'
        tV_msg = 'None' if self.terminalValue is None else self.terminalValue.title
        mS = self.mostSearched
        
        if self.mostSearched: mS_msg = f'{mS.title} with {mS.searchCount} searches'
        else: mS_msg = 'None'
        
        out = f'Interval {self.interval}, with {hasNext} nextArr\n'
        out += f'Terminal value of {tV_msg}\n'
        out += f'Most searched is {mS_msg}'
        return out


class CompactNode:
    '''
    Changes from Node:
    - self.intervals instead of interval (it's an array)
    - self.prev keeps track of previous/parent node
    - override [] notation to access next array, such that CompactNode[-1] returns
      corresponding node for the interval -1 (automatic ivlToIdx conversion)
    '''
    def __init__(self, ivls, prev, nextArr=None):
        '''
        ivls can be either an int (one interval) or an array (1+ intervals)
        '''
        if type(ivls) is int: self.intervals = [ivls]
        else: self.intervals = ivls
        
        self.prev = prev
        self.nextArr = nextArr
        
        # for if there is an item that terminates at this node
        # TODO: may need to make this an array
        self.terminalValue = None
        
        # to keep track of most searched item
        # also used for matching with searches that are only first half of the melody, etc.
        self.mostSearched = None
    
    def __str__(self):
        hasNext = 'no' if self.nextArr is None else 'a'
        tV_msg = 'None' if self.terminalValue is None else self.terminalValue.title
        mS = self.mostSearched
        
        if self.mostSearched: mS_msg = f'{mS.title} with {mS.searchCount} searches'
        else: mS_msg = 'None'
        
        out = f'Intervals {self.intervals}, with {hasNext} nextArr\n'
        out += f'Terminal value of {tV_msg}\n'
        out += f'Most searched is {mS_msg}'
        return out

    def __getitem__(self, ivl):
        # edge case of list/tuple
        if type(ivl) is list or type(ivl) is tuple:
            currNode = self
            for i in ivl: currNode = currNode.nextArr[ivlToIdx(i)]

            return currNode
    
        # main case of single int as index
        return self.nextArr[ivlToIdx(ivl)]
    
    def __setitem__(self, ivl, node):
        self.nextArr[ivlToIdx(ivl)] = node