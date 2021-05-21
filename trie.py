from trieUtil import *
from node import *


class Trie:
    def __init__(self):
        self.root = Node(None, createNewNextArr(nodetype='default'))
        self.numItems = 0
        
    def __str__(self):
        return f'Trie with {self.numItems} items'
    
    def __len__(self):
        return self.numItems
    
    
    def insert(self, mw):
        currNode = self.root
        
        # go through intervals (traverse trie)
        for ivl in mw.melodyIntervals:
            # populate currNodes's next array if necesary
            if currNode.nextArr is None: currNode.nextArr = createNewNextArr(nodetype='default')
            
            # update most searched for this node, if None
            if not currNode.mostSearched: currNode.mostSearched = mw
            
            # step down
            currNode = currNode.nextArr[ivlToIdx(ivl)]
        
        # currNode now holds terminal node for this musical work
        currNode.terminalValue = mw
        self.numItems += 1 # increment number of items
        
    def search(self, melody):
        # try to find the musical work
        # TODO: for speed reasons, find out how to return the result first,
        #       and only then update mostSearched?
        mw, exact = self._find(melody)
        
        
        # Determine if any Nodes' mostSearched needs updating
        # if mw is None, don't do anything
        if not mw: pass
        # otherwise, traverse trie again, but update mostSearched as necessary
        else:
            mw.searchCount += 1
            self._updateMostSearched(mw)
        
        return mw
    
    # helper function for search to find mw based on melody
    def _find(self, melody):
        '''
        Returns a musical work, and whether it is an exact match or not
        '''
        currNode = self.root
        
        # go through intervals (traverse trie)
        for ivl in melodyToIntervals(melody):
            # this node is a dead end
            if currNode.nextArr is None: return currNode.mostSearched, False
            # if not a dead end, keep going
            currNode = currNode.nextArr[ivlToIdx(ivl)]
        
        # if we didn't reach dead end, check if node is terminal
        if currNode.terminalValue: return currNode.terminalValue, True
        else: return currNode.mostSearched, False # no exact match

    #helper function for search to update mostSearched
    def _updateMostSearched(self, mw):
        currNode = self.root
        mS, sC = currNode.mostSearched, mw.searchCount
        
        # go through the intervals (traverse trie)
        for ivl in mw.melodyIntervals:
            # update mostSearched if necessary
            if mS is not None and sC > mS.searchCount:
                currNode.mostSearched = mw
            
            # go to next (no check as we know mw exists in trie)
            currNode = currNode.nextArr[ivlToIdx(ivl)]


class CompactTrie:
    def __init__(self):
        self.root = CompactNode(None, None)
        self.root.nextArr = createNewNextArr(self.root)
        self.numItems = 0
        
    def __str__(self):
        return f'Compact Trie with {self.numItems} items'
    
    def __len__(self):
        return self.numItems
    
    
    def insert(self, mw):
        mI = mw.melodyIntervals # shave off intervals as we process them
        currNode = self.root[mI[0]] # go to root's corresponding child node

        
        # go through intervals (traverse trie)
        while len(mI) > 0:
            print('mI:', mI, end = '\n  ')
            # update most searched mw for this node, if None
            if not currNode.mostSearched: currNode.mostSearched = mw
            
            
            # figure out how much we match with current node
            mI_len = 0 if (mI is None) else len(mI)
            cN_len = 0 if (currNode.intervals is None) else len(currNode.intervals)
            firstDiff = firstNonmatching(mI, currNode.intervals)
            print(f'mI_len = {mI_len}, cN_len = {cN_len}', end='\n  ')
            
            # - Case 1: arrays not equal somewhere in the middle
            #           = "split" the node
            if firstDiff != -1:
                print('Case 1 (unequal, split node)')
                # create parent node
                pNode = CompactNode(mI[:firstDiff], currNode.prev)
                pNode.nextArr = createNewNextArr(prev=pNode)
                
                # update currNode's prev's nextArr to point to new parent node
                currNode.prev[mI[0]] = pNode
                
                # update currNode's prev and intervals
                currNode.prev = pNode
                currNode.intervals = currNode.intervals[firstDiff:]
                
                # update parent node: insert currNode into new parent node's nextArr, update mostSearched
                pNode[currNode.intervals[0]] = currNode # link currNode as a next node
                pNode.mostSearched = currNode.mostSearched

                # *step down trie*, to corresponding child of parent node
                mI = mI[firstDiff:]
                currNode = pNode[mI[0]]
            
            # - Case 2: equal, but more remaining ivls than in this node's ivl array
            elif mI_len > cN_len:
                # Case 2a: we have next array
                #          = *step down trie*
                if currNode.nextArr is not None:
                    print('Case 2a (equal w/ longer mI, and nextArr)')
                    mI = mI[cN_len:]
                    currNode = currNode[mI[0]]

                # Case 2b: no next array, currNode not a terminal node
                #          = extend node's ivls, DONE
                elif not currNode.terminalValue:
                    print('Case 2b (equal w/ longer mI, no nextArr but not terminal)')
                    currNode.intervals = mI
                    break

                # Case 2c: no next array, currNode is a terminal node
                #          = create next array, add child node into array, DONE
                else:
                    print('Case 2c (equal w/ longer mI, no nextArr and terminal)')
                    currNode.nextArr = createNewNextArr(prev=currNode)
                    cNode = CompactNode(mI[cN_len:], currNode)
                    currNode[mI[cN_len]] = cNode
                    
                    currNode = cNode
                    break

            # - Case 3: equal, but less remaining ivls than in this nodes' ivl array
            #           = "split" the node, DONE
            elif mI_len < cN_len:
                print('Case 3 (equal w/ shorter mI)')
                # create new parent node
                pNode = CompactNode(mI, currNode.prev)
                pNode.nextArr = createNewNextArr(prev=pNode)
                
                # update currNode's prev's nextArr to point to new parent node
                currNode.prev[mI[0]] = pNode
                
                # update currNode's prev and intervals
                currNode.prev = pNode
                currNode.intervals = currNode.intervals[mI_len:]
                
                # insert currNode into new parent node's nextArr
                currNodeIdx = ivlToIdx(currNode.intervals[0])
                pNode.nextArr[currNodeIdx] = currNode # link currNode as a next node
                
                pNode.mostSearched = currNode.mostSearched
                
                # currNode is now pNode
                currNode = pNode
                break

            # - Case 4: identical in elements and size
            #           = DONE
            # TODO: change terminalValue into array?
            else:
                print('Case 4 (identical)')
                break
        
        
        # currNode now holds terminal node for this musical work
        currNode.terminalValue = mw
        self.numItems += 1 # increment number of items
    
    def search(self, melody):
        # try to find the musical work
        # TODO: for speed reasons, find out how to return the result first,
        #       and only then update mostSearched?
        mw, exact = self._find(melody)
        
        
        # Determine if any Nodes' mostSearched needs updating
        # if mw is None, don't do anything
        if not mw: pass
        # otherwise, traverse trie again, but update mostSearched as necessary
        else:
            mw.searchCount += 1
            self._updateMostSearched(mw)
        
        return mw
    
    # helper function for search to find mw based on melody
    def _find(self, melody):
        '''
        Returns a musical work, and whether it is an exact match or not
        '''
        currNode = self.root
        
        # go through intervals (traverse trie)
        for ivl in melodyToIntervals(melody):
            # this node is a dead end
            if not currNode.nextArr: return currNode.mostSearched, False
            # if not a dead end, keep going
            currNode = currNode.nextArr[ivlToIdx(ivl)]
        
        # if we didn't reach dead end, check if node is terminal
        if currNode.terminalValue: return currNode.terminalValue, True
        else: return currNode.mostSearched, False # no exact match

    #helper function for search to update mostSearched
    def _updateMostSearched(self, mw):
        currNode = self.root
        mS, sC = currNode.mostSearched, mw.searchCount
        
        # go through the intervals (traverse trie)
        for ivl in mw.melodyIntervals:
            # update mostSearched if necessary
            if mS is not None and sC > mS.searchCount:
                currNode.mostSearched = mw
            
            # go to next (no check as we know mw exists in trie)
            currNode = currNode.nextArr[ivlToIdx(ivl)]