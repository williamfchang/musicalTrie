// piano keyboard constants
const NUM_OCTAVES = 3;
const STARTING_OCTAVE = 3; // keyboard starts on C3
const KEY_PATTERN = [0,1,0,1,0,0,1,0,1,0,1,0];


// global (window) variables include inSearchBox and shiftHeld


/* -- KEYMAPS -- */
// 1. computer key to piano key mapping. Currently, using slice to reduce the keymapping to 3 octaves
const FULL_KEYMAP = ['ShiftLeft', 'KeyZ', 'KeyX', 'KeyC', 'KeyV', 'KeyB', 'KeyA', 'KeyS', 'KeyD', 'KeyF', 'KeyG', 'KeyH',
                     'KeyQ', 'KeyW', 'KeyE', 'KeyR', 'KeyT', 'KeyY', 'Digit1', 'Digit2', 'Digit3', 'Digit4', 'Digit5', 'Digit6',
                     'Digit7', 'Digit8', 'Digit9', 'Digit0', 'Minus', 'Equal', 'KeyU', 'KeyI', 'KeyO', 'KeyP', 'BracketLeft', 'BracketRight',
                     'KeyJ', 'KeyK', 'KeyL', 'Semicolon', 'Quote', 'Enter', 'KeyN', 'KeyM', 'Comma', 'Period', 'Slash', 'ShiftRight'].slice(6,-5);
const FULL_KEYMAP_CHAR = ['SL', 'Z', 'X', 'C', 'V', 'B', 'A', 'S', 'D', 'F', 'G', 'H',
                          'Q', 'W', 'E', 'R', 'T', 'Y', '1', '2', '3', '4', '5', '6',
                          '7', '8', '9', '0', '-', '=', 'U', 'I', 'O', 'P', '[', ']',
                          'J', 'K', 'L', ';', '"', 'EN', 'N', 'M', ',', '.', '/', 'SR'].slice(6,-5);


// 2. a more intuitive keymapping
const PARTIAL_KEYMAP = ['', '', '', '', '', '', '', '', '', '', '', '',
                        'KeyQ', 'Digit2', 'KeyW', 'Digit3', 'KeyE', 'KeyR', 'Digit5', 'KeyT', 'Digit6', 'KeyY', 'Digit7', 'KeyU',
                        'KeyI', 'Digit9', 'KeyO', 'Digit0', 'KeyP', 'BracketLeft', 'Equal', 'BracketRight', '', '', '', ''];

const PARTIAL_KEYMAP_CHAR = ['', '', '', '', '', '', '', '', '', '', '', '',
                             'Q', '2', 'W', '3', 'E', 'R', '5', 'T', '6', 'Y', '7', 'U',
                             'I', '9', 'O', '0', 'P', '[', '=', ']', '', '', '', '', ''];


// SET DEFAULT KEYMAP
window.keymap = PARTIAL_KEYMAP
window.keymapChar = PARTIAL_KEYMAP_CHAR


// var keysPressed = [];
// var intervals = [];

function renderKeyboard() {
    var keyboardHTML = "<ul class='keyboard'>\n";

    // each iteration is an octave
    for (var i = 0; i < NUM_OCTAVES; i++) {
        // each iteration is one note
        for (var j = 0; j < 12; j++) {
            const color = KEY_PATTERN[j] ? 'black' : 'white';
            keyboardHTML += "<li class='" + color + "-key'><p>" + keymapChar[i*12 + j] + "</p></li>\n";
        }
    }

    keyboardHTML += "<li class='white-key'><p>" + keymapChar[NUM_OCTAVES*12] + "</p></li>\n</ul>\n";

    return keyboardHTML;
}

// helper function for adding keymap letters to each key
function renderKeymap() {

}

function processPianoClick() {
    const keyIndex = $(this).index(); // get the pressed keyboard key
    if (keyIndex < 0 || keyIndex > NUM_OCTAVES * 12) return;
    playKeyAudio(keyIndex); // play audio

    addNote(keyIndex); // update notes history
}

function processComputerKeydown(e) {
    // ignore keypress if not interacting with piano
    if (window.inSearchBox) return;

    // special keys: check if keydown is backspace or shift
    if (e.code == 'Backspace') {
        deleteNoteFromSearchBar();
        return;
    } else if (e.key == 'Shift') {
        window.shiftHeld = true;
    }

    // check if keycode is valid
    const keyIndex = keymap.indexOf(e.code);
    if (keyIndex < 0 || keyIndex > NUM_OCTAVES * 12) return;
    playKeyAudio(keyIndex); // play audio

    addNote(keyIndex); // update notes history

    // change style of piano key
    const pianoKey = $('.keyboard').find('li').eq(keyIndex);
    if (pianoKey.hasClass('white-key')) pianoKey.addClass('white-key-active');
    else pianoKey.addClass('black-key-active');
}

function processComputerKeyup(e) {
    // ignore keypress if not interacting with piano
    if (window.inSearchBox) return;

    // special keys: check if keyup is shift
    if (e.key == 'Shift') {
        window.shiftHeld = false;
    }

    // check if keycode is valid
    const keyIndex = keymap.indexOf(e.code);
    if (keyIndex < 0 || keyIndex > NUM_OCTAVES * 12) return;

    // change style of piano key back to default
    const pianoKey = $('.keyboard').find('li').eq(keyIndex);
    if (pianoKey.hasClass('white-key')) pianoKey.removeClass('white-key-active');
    else pianoKey.removeClass('black-key-active');
}

// Helper function to play the audio clip for the pressed key
function playKeyAudio(keyIndex) {
    const keyID = keyIndexToNote(keyIndex, flatOnly=true);

    // Play audio for the key
    var audio = new Audio('static/key_sounds/' + keyID + '.m4a');
    audio.play();
}

// Helper function to update arrays holding note history data
function addNote(keyIndex) {
    // // update interval info if more than one key has been pressed. CURRENTLY NOT IN USE
    // if (keysPressed.length > 0) {
    //     const newInterval = keyIndex - keysPressed[keysPressed.length - 1];

    //     $('#intervals-display').append(newInterval + ', ');
    //     intervals.push(newInterval);
    // }

    // // either way, update notes info. CURRENTLY NOT IN USE
    // $('#notes-display').append(keyIndexToNote(keyIndex) + ', ');
    // keysPressed.push(keyIndex);

    // also update search box
    var melodySearch = $('#melody-search')
    var extraSpace = melodySearch.val() == '' ? '' : ' ';
    melodySearch.val( melodySearch.val() + extraSpace + keyIndexToNote(keyIndex) );
}

// Helper function to get key ID (C4, Eb3, D#3, etc.)
// use flatOnly parameter to return only flat, otherwise if shift is held, sharps are returned
function keyIndexToNote(keyIndex, flatOnly = false) {
    const allKeysFlat = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B'];
    const allKeysSharp = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'];
    
    if (flatOnly || !window.shiftHeld) {
        return allKeysFlat[keyIndex % 12] + Math.floor(STARTING_OCTAVE + keyIndex / 12);
    } else {
        return allKeysSharp[keyIndex % 12] + Math.floor(STARTING_OCTAVE + keyIndex / 12);
    }
}

function semitonesToInterval(semitones) {
    return;
}



// Helper fucntion that deletes one note from the search bar
function deleteNoteFromSearchBar() {
    var inputVal = $('#melody-search').val();
    var i = inputVal.lastIndexOf(' ');
    $('#melody-search').val(inputVal.substr(0,i));
}


// Two functions that update whether the user is in the search text box or not
function isInSearchBox() {
    window.inSearchBox = true;
    $('#activate-piano-keyboard').css('background-color', 'lightgrey');
}

function notInSearchBox() {
    window.inSearchBox = false;
    $('#activate-piano-keyboard').css('background-color', 'lightgreen');
}


// Small function to switch keymaps, currently just alternates between the full and partial keymaps
function switchKeymaps() {
    // swap
    if (window.keymap == FULL_KEYMAP) {
        window.keymap = PARTIAL_KEYMAP;
        window.keymapChar = PARTIAL_KEYMAP_CHAR;
    } else {
        window.keymap = FULL_KEYMAP;
        window.keymapChar = FULL_KEYMAP_CHAR;
    }

    // re-render keyboard
    $('.keyboard-container').html(renderKeyboard());
}