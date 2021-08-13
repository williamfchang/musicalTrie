from trie.musicalClasses import *
from trie.node import *

# HELPER FUNCTIONS

# checks if inputted melody is valid
# 0+ if invalid, indicating index at first invalid note
# -1 if valid
# -2 if invalid, because melody is too short
def validMelody(melody):
    note = ''
    numNotes = 0

    # go through every character, constructing a note and then checking it
    # extra space forces a check on the last note
    for i, char in enumerate(melody + ' '):
        # note construction
        if char == '/': note = ''
        elif char != ' ': note += char
        elif char == ' ' and note == '': continue
            
        # main case (a space with nonempty note): check for note, accidental, octave
        else:
            validNote = note[0] in notes
            validAccidental = (len(note) == 2) or (note[1:len(note)-1] in accidentals)
            validOctave = note[-1] in octavesStr

            # at least one is wrong
            if not (validNote and validAccidental and validOctave): return i - len(note)
            
            # otherwise, reset note
            note = ''
            numNotes += 1

    # if we got here, entire melody is valid (but need to check if only one note)
    if numNotes < 2: return -2
    else: return -1



# version of validMelody using melody.split() rather than going char by char
# def validMelody(melody):
#     currIdx = 0

#     # go through each note
#     for note in melody.split():
#         # edge case
#         if note == "/": pass

#         # main case: check for note, accidental, and octave
#         else:
#             validNote = note[0] in notes
#             validAccidental = (len(note) == 2) or (note[1:len(note)-1] in accidentals)
#             validOctave = note[-1] in octavesStr

#             # at least one is wrong
#             if not (validNote and validAccidental and validOctave): return currIdx

#         currIdx += len(note) + 1 # account for the space

#     # if we got here, entire melody was valid
#     return -1





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