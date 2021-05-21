# Musical Trie

*Data structure for familiar music finder project. See https://github.com/williamfchang/melody*

## Note/melody representations

Two representations of a single note:
1. note: string of the note name (`'E5'`)
2. value: the note value (`64`)

Three representations of a melody (string of notes):
1. melody: string of actual note names (`'E5 D#5 E5 D#5 E5'`)
2. values: list of note values (`[64, 63, 64, 63, 64]`)
3. intervals: list of the intervals between values (`[-1, 1, -1, 1]`)