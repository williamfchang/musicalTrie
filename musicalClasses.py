import numpy as np

# -- Basic definitions - #
notes = {'C': 0, 'D': 2, 'E': 4, 'F': 5, 'G': 7, 'A': 9, 'B': 11}
accidentals = {'bb': -2, 'd': -2, 'b': -1, 'n': 0, '#': 1, '##': 2, 'x': 2}

maxRange = 96 - 9 # =87, the range from A0 to C8


# -- Util functions -- #
def noteToValue(note):
    # get note, accidental, octave
    n = note[0]
    a = 'n' if len(note) == 2 else note[1:len(note)-1]
    o = int(note[-1])
    
    return notes[n] + accidentals[a] + o*12

def valuesToIntervals(vals):
    intervals = np.array([vals[i+1]-vals[i] for i in range(len(vals)-1)])
    return intervals

def melodyToValues(melody):
    # currently ignoring the slashes that indicate a rest/breath/phrase
    values = np.array([noteToValue(note) for note in melody.split() if note != '/'])
    return values

# shortcut function
def melodyToIntervals(melody):
    return valuesToIntervals(melodyToValues(melody))


# Used mostly in node.py and trie.py
# helper function to convert an interval to the correct index in nextArr
def ivlToIdx(ivl):
    return ivl + maxRange


# -- Classes -- #
class MusicalWork:
    def __init__(self, title, artist, date, genre, key, melody):
        self.title = title
        self.artist = artist
        self.date = date
        self.genre = genre
        
        self.melody = melody
        self.melodyValues = melodyToValues(melody)
        self.melodyIntervals = valuesToIntervals(self.melodyValues)
        self.key = key # key signature
        
        self.searchCount = 0
    
    def __str__(self):
        out =  f'[+{self.searchCount}] {self.title} | by {self.artist} ({self.date}, {self.genre})\n'
        out += f'Melody [{self.key}]: {self.melody}'
        return out

class ClassicalPiece(MusicalWork):
    def __init__(self, t, a, d, g, k, m, op=None, no=None, mv=None):
        MusicalWork.__init__(self, t, a, d, g, k, m)
        
        self.opus = op
        self.number = no
        self.movement = mv

        
class Song(MusicalWork):
    def __init__(self, t, a, d, g, k, m, aN=None):
        MusicalWork.__init__(self, t, a, d, g, k, m)
        
        self.albumName = aN