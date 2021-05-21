

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
        hasNext = 'a' if self.nextArr is not None else 'no'
        tV_msg = self.terminalValue.title if self.terminalValue is not None else 'None'
        mS = self.mostSearched
        
        if self.mostSearched: mS_msg = f'{mS.title} with {mS.searchCount} searches'
        else: mS_msg = 'None'
        
        out = f'Interval {self.interval}, with {hasNext} nextArr\n'
        out += f'Terminal value of {tV_msg}\n'
        out += f'Most searched is {mS_msg}'
        return out


class CompactNode:
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
        hasNext = 'a' if self.nextArr is not None else 'no'
        tV_msg = self.terminalValue.title if self.terminalValue is not None else 'None'
        mS = self.mostSearched
        
        if self.mostSearched: mS_msg = f'{mS.title} with {mS.searchCount} searches'
        else: mS_msg = 'None'
        
        out = f'Intervals {self.intervals}, with {hasNext} nextArr\n'
        out += f'Terminal value of {tV_msg}\n'
        out += f'Most searched is {mS_msg}'
        return out