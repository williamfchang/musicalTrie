// audio delay fix for Safari on Mac: https://stackoverflow.com/questions/9811429/html5-audio-tag-on-safari-has-a-delay
const AudioContext = window.AudioContext || window.webkitAudioContext;
const audioCtx = new AudioContext();


// piano keyboard constants (ground truths)
const KEY_PATTERN = [0,1,0,1,0,0,1,0,1,0,1,0];
const KEYS_PER_OCTAVE = 12;

// piano keyboard constants that can be changed
const NUM_OCTAVES = 3;
const STARTING_OCTAVE = 3; // keyboard starts on C3


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
window.keymap = PARTIAL_KEYMAP;
window.keymapChar = PARTIAL_KEYMAP_CHAR;


// variables
var lastWrongIdx = -1;

// var keysPressed = [];
// var intervals = [];

function renderKeyboard() {
    // open keyboard list
    var keyboardHTML = "<ul class='keyboard'>\n";

    // each iteration is an octave
    for (var i = 0; i < NUM_OCTAVES; i++) {
        // start octave
        keyboardHTML += "<span class='octave'>\n";

        // each iteration is one note
        for (var j = 0; j < KEYS_PER_OCTAVE; j++) {
            const color = KEY_PATTERN[j] ? 'black' : 'white';
            keyboardHTML += "<li class='" + color + "-key'><p>" + keymapChar[i*KEYS_PER_OCTAVE + j] + "</p></li>\n";
        }

        // add high C if last iteration
        if (i == NUM_OCTAVES-1) {
            keyboardHTML += "<li class='white-key'><p>" + keymapChar[NUM_OCTAVES*KEYS_PER_OCTAVE] + "</p></li>\n";
        }

        // close octave. Use no newlines after spans: https://stackoverflow.com/questions/5078239/how-do-i-remove-the-space-between-inline-inline-block-elements
        keyboardHTML += "</span>";
    }

    // close keyboard list
    keyboardHTML += "</ul>\n";


    return keyboardHTML;
}



// function for searching for melody (AJAX) and updating HTML
function searchMelodyAndUpdate() {
    // RESET ELEMENTS:
    $("#results-title").css('background-color', ''); // reset results jumbotron to grey
    $("#upvote-button").removeClass('btn-primary').addClass('btn-light'); // reset upvote button

    // use AJAX to get answer from python
    $.getJSON($SCRIPT_ROOT + '/_melody_search', {
        melody: $("#melody-search").val()
    }, function(data) {
        // keep track of last wrongAtIdx
        lastWrongIdx = data.wrongAtIdx;

        // update title
        $("#results-title").html(data.title);

        // update melody subtitle: start by setting a default value for melody HTML
        var melodyHTML = data.melody;

        // check if wrong at an index
        if (data.wrongAtIdx >= 0) {
            melodyHTML = data.melody.substr(0, data.wrongAtIdx);
            melodyHTML += "<span class='red-highlight'>";
            melodyHTML += data.melody.substr(data.wrongAtIdx);
            melodyHTML += "</span>";
        }

        // assign to HTML element
        $("#results-melody").html(melodyHTML);
    });
}


// GENERAL FUNCTION that processes when a piano key is activated
// (whether by click or keyboard shortcut)
function processPianoKeyActivated(keyIndex) {
    // check if keycode is valid
    if (keyIndex < 0 || keyIndex > NUM_OCTAVES * KEYS_PER_OCTAVE) return false;
    playKeyAudio(keyIndex); // play audio

    addNote(keyIndex); // update notes history and input box
    searchMelodyAndUpdate(); // update result box

    return true;
}


// function that runs when user clicks on a piano key
function processPianoClick() {
    // get the pressed keyboard key, then pass to key activated function
    const keyIndex = $(this).parent().index() * KEYS_PER_OCTAVE + $(this).index();
    processPianoKeyActivated(keyIndex);
}

// function that is called when a button on computer keyboard is pressed
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
    if (!processPianoKeyActivated(keyIndex)) return;

    // change style of piano key
    const pianoKey = $('.keyboard').find('li').eq(keyIndex);
    if (pianoKey.hasClass('white-key')) pianoKey.addClass('white-key-active');
    else pianoKey.addClass('black-key-active');
}

// function that is called when a button on computer keyboard is released
function processComputerKeyup(e) {
    // ignore keypress if not interacting with piano
    if (window.inSearchBox) return;

    // special keys: check if keyup is shift
    if (e.key == 'Shift') {
        window.shiftHeld = false;
    }

    // check if keycode is valid
    const keyIndex = keymap.indexOf(e.code);
    if (keyIndex < 0 || keyIndex > NUM_OCTAVES * KEYS_PER_OCTAVE) return;

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
        return allKeysFlat[keyIndex % KEYS_PER_OCTAVE] + Math.floor(STARTING_OCTAVE + keyIndex / KEYS_PER_OCTAVE);
    } else {
        return allKeysSharp[keyIndex % KEYS_PER_OCTAVE] + Math.floor(STARTING_OCTAVE + keyIndex / KEYS_PER_OCTAVE);
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
    searchMelodyAndUpdate();
}


// Two functions that update whether the user is in the search text box or not
function isInSearchBox() {
    window.inSearchBox = true;
    $('#activate-piano-keyboard').css('background-color', 'lightgrey');
    $('#activate-piano-keyboard').text('Keyboard shortcuts for piano keyboard are OFF');
}

function notInSearchBox() {
    window.inSearchBox = false;
    $('#activate-piano-keyboard').css('background-color', 'lightgreen');
    $('#activate-piano-keyboard').text('Keyboard shortcuts for piano keyboard are ON');
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

// Function to update background color of the results jumbotron when search is pressed
function highlightResult() {
    var color = (lastWrongIdx == -1) ? "lightgreen" : "lightcoral";
    $("#results-title").css('background-color', color);
}

// processes an upvote
function processUpvote() {
    const upBtn = $('#upvote-button');

    // toggle appearance
    upBtn.toggleClass('btn-light').toggleClass('btn-primary');
    
    // determine if we are upvoting or removing upvote
    const voteToAdd = (upBtn.hasClass('btn-primary')) ? 1 : -1;

    $.getJSON($SCRIPT_ROOT + '/_add_vote', {
        vote: voteToAdd
    }, function(data) {
        if (data.title.length > 0) $("#results-title").html(data.title);
    });
}