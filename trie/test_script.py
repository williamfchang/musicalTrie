from trie import *


# Create compact trie
ct = CompactTrie()

# insert works into compact trie
ct.insert(ClassicalPiece('Fur Elise', 'Ludwig van Beethoven', 1810, 'Classical Period', 'a minor',
                            'E5 D#5 E5 D#5 E5 B4 D5 C5 A4 / C4 E4 A4 B4 / E4 G#4 B4 C5',
                            None, None))

ct.insert(Song('Happy Birthday!', None, None, None, None, 'C4 C4 D4 C4 F4 E4'))
ct.insert(Song('Twinkle Twinkle Little Star', None, None, None, None, 'C4 C4 G4 G4 A4 A4 G4'))

ct.insert(Song('Avatar\'s Love', None, 2003, 'TV Show Music', 'C major', 'C5 B4 G4 E4'))
ct.insert(Song('Jurrasic Park Theme', 'John Williams', 1993, 'Movie Score', 'C major',
                  'C5 B4 C5 G4 F4 C5 B4 C5 G4 F4 C5 B4 C5 D5 D5 F5 F5 / E5 C5 D5 B4 G4 E5 C5 D5 / ' + 
                  'G5 C5 F5 E5 E5 D5 D5'))
# ct.insert(Song('Jurrasic Park Theme', 'John Williams', 1993, 'Movie Score', 'C major',
#                   'C5 B4 C5 G4 F4 C5 B4 C5 G4 F4 C5 B4 C5 D5 D5 F5 F5'))
ct.insert(Song('Le Festin', 'Ratatouille', 2000, 'Movie Score', 'Bb major',
                  'Bb3 G4 F4 Eb4 G4 F4 Eb4 G4 F4 Eb4 Bb4'))
ct.insert(Song('Jazz Lick', None, None, 'Jazz', 'C major', 'C3 E2 F2 F#2 G2 A2 B2 C2'))

ct.insert(MusicalWork('custom', 'bruh', 2021, 'yerp', 'C major', 'C5 B4 C5'))

ct.insert(MusicalWork('random1', 'me', 2021, None, None, 'A4 B4 C5'))
ct.insert(MusicalWork('random2', 'me', 2021, None, None, 'C4 D4 E4'))
ct.insert(MusicalWork('random3', 'me', 2021, None, None, 'D4 D4 A4 A4 D5 A4 D4'))
ct.insert(MusicalWork('random4', 'me', 2021, None, None, 'Gb6 Bb6 Db7'))
ct.insert(MusicalWork('random5', 'me', 2021, None, None, 'F6 C6 A5 F5'))



# test
test_queries = ['E6 D#6 E6 D#6 E6', 'G2 G2 D3 D3', 'G3 G3 A3 G3', 'Bb5 G6 F6 Eb6', 'G4 F#4 G4 D4 C4', 'Gd3 G3']

for query in test_queries:
    print('\nLooking for:', query)
    print(ct.search(query))
    