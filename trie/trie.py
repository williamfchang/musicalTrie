from trie.trieUtil import *
from trie.node import *


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
            if currNode.mostSearched is None: currNode.mostSearched = mw
            
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
        if mw is None: pass
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

    # helper function for search to update mostSearched
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
        if self.root.mostSearched is None: self.root.mostSearched = mw # for first insert

        mI = mw.melodyIntervals # shave off intervals as we process them
        currNode = self.root[mI[0]] # go to root's corresponding child node

        
        # go through intervals (traverse trie)
        while len(mI) > 0:
            # update most searched mw for this node, if None
            if currNode.mostSearched is None: currNode.mostSearched = mw
            
            
            # figure out how much we match with current node
            mI_len = 0 if (mI is None) else len(mI)
            cN_len = 0 if (currNode.intervals is None) else len(currNode.intervals)
            firstDiff = firstNonmatching(mI, currNode.intervals)
            
            # - Case 1: arrays not equal somewhere in the middle
            #           = "split" the node
            if firstDiff != -1:
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

                # STEP DOWN TRIE, to corresponding child of parent node
                mI = mI[firstDiff:]
                currNode = pNode[mI[0]]
            
            # - Case 2: equal, but more remaining ivls than in this node's ivl array
            elif mI_len > cN_len:
                # Case 2a: we have next array
                #          = STEP DOWN TRIE
                if currNode.nextArr is not None:
                    mI = mI[cN_len:]
                    currNode = currNode[mI[0]]

                # Case 2b: no next array, currNode not a terminal node
                #          = extend node's ivls, DONE
                elif not currNode.terminalValue:
                    currNode.intervals = mI
                    break

                # Case 2c: no next array, currNode is a terminal node
                #          = create next array, add child node into array, DONE
                else:
                    currNode.nextArr = createNewNextArr(prev=currNode)
                    cNode = CompactNode(mI[cN_len:], currNode)
                    cNode.mostSearched = mw
                    currNode[mI[cN_len]] = cNode
                    
                    currNode = cNode
                    break

            # - Case 3: equal, but less remaining ivls than in this nodes' ivl array
            #           = "split" the node, DONE
            elif mI_len < cN_len:
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
            else: break
        
        
        # currNode now holds terminal node for this musical work
        currNode.terminalValue = mw
        self.numItems += 1 # increment number of items
    
    def search(self, melody):
        # try to find the musical work
        # TODO: for speed reasons, find out how to return the result first,
        #       and only then update mostSearched?
        foundMW, isExact, path = self._find(melody)
        
        
        # Determine if any Nodes' mostSearched needs updating
        # if so, traverse trie again, update mostSearched as necessary
        if foundMW is not None:
            foundMW.searchCount += 1
            self._updateMostSearched(foundMW, path)
        
        return foundMW
    
    # helper function for search to find mw based on melody
    def _find(self, melody):
        '''
        Returns foundMW, isExact, path
        - foundMW: the exact matching musical work, or the mostSearched node that
            best matches the melody if no exact match exists.
        - isExact: whether the returned musical work is exact or not
        - path: the node path (as a list...does it need to be a numpy array?)
            that was taken to attempt to find musical work.
        '''
        path = [self.root]

        mI = melodyToIntervals(melody) # shave off intervals as we process them
        currNode = self.root[mI[0]] # go to root's corresponding child node

        # go through intervals (traverse trie)
        while len(mI) > 0:
            path.append(currNode) # add to path

            # figure out how much we match with current node
            mI_len = 0 if (mI is None) else len(mI)
            cN_len = 0 if (currNode.intervals is None) else len(currNode.intervals)
            firstDiff = firstNonmatching(mI, currNode.intervals)

            # - Case 1: arrays not equal somewhere in middle
            #           = this node is irrelevant, RETURN previous mostSearched
            if firstDiff != -1:
                return currNode.prev.mostSearched, False, path[:-1]
            
            # - Case 2: equal, but more reminaing ivls than in this node's ivl array
            elif mI_len > cN_len:
                # Case 2a: we have next array
                #          = *step down trie*
                if currNode.nextArr is not None:
                    mI = mI[cN_len:]
                    currNode = currNode[mI[0]]
                
                # Case 2b: no next array
                #          = BREAK and let ending logic figure it out
                else: break
            
            # - Case 3: equal, but less remaining ivls than in this nodes' ivl array
            #           = exact is not in trie, but input may be substring, RETURN mostSearched
            elif mI_len < cN_len:
                return currNode.mostSearched, False, path
            
            # - Case 4: identical in elements and size
            #           = exact match, BREAK to let end logic compute result
            else: break
        

        # if we ran out of intervals, check if node is terminal
        # (not sure if this will be ever reached)
        if currNode.terminalValue: return currNode.terminalValue, True, path
        else: return currNode.mostSearched, False, path # no exact match

    # helper function for search to update mostSearched
    def _updateMostSearched(self, mw, path):        
        # traverse trie using given path
        for currNode in path:
            # update mostSearched if foundMW is more popular than
            # currNode's previously most popular
            if mw.searchCount > currNode.mostSearched.searchCount:
                currNode.mostSearched = mw