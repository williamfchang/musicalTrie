from flask import Flask, request, render_template
from trie import *

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
    # no info yet
    if request.method == 'GET':
        return render_template('search.html')
    
    # user has now submitted info
    else:
        # search trie for user inputted melody
        melody = request.form["melody"]
        found_mw = ct.search(melody)
        
        line1, line2 = str(found_mw).split('\n')

        return render_template('search_post.html', found_mw_title=line1, found_mw_melody=line2)





if __name__ == '__main__':
    app.run(debug=True)