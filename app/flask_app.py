# Add trie to python path: https://stackoverflow.com/questions/16981921/relative-imports-in-python-3
import sys
import os

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))


# Imports
from flask import Flask, jsonify, render_template, request
from trie.trie import *


# -- TRIE SETUP -- #
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

print('this only executes once right?')


# -- FLASK -- #
app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def home():
    return render_template('search.html')


@app.route('/_melody_search')
def melody_search():
    melody = request.args.get('melody', '', type=str)

    line1 = "(Not found)"
    line2 = melody

    # check if input is valid, only search if valid
    wrongAtIdx = validMelody(melody)

    # Case 1 (-2): invalid, one or less notes
    if wrongAtIdx == -2:
        line1 = "Enter more than one note!"
    # Case 2 (0+): invalid at given index
    elif wrongAtIdx >= 0:
        line1 = "Fix the error(s) below:"
    # Case 3 (-1): valid
    else:
        found_mw = ct.search(melody)
        if found_mw: line1, line2 = str(found_mw).split('\n')
    
    # return
    return jsonify(title=line1, melody=line2, wrongAtIdx=wrongAtIdx)

@app.route('/_add_vote')
def add_vote():
    vote = request.args.get('vote', 0, type=int)

    # update vote, also update most searched for each node
    if ct.lastFoundMW: ct.lastFoundMW.searchCount += vote
    ct._updateMostSearched(ct.lastFoundMW, ct.lastFoundMWPath)

    # determine title to return to html
    new_title = ''
    if ct.lastFoundMW: new_title = str(ct.lastFoundMW).split('\n')[0]

    return jsonify(title=new_title)


if __name__ == '__main__':
    app.run(host='0.0.0.0')