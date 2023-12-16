from music21 import *


def create_chord_from_notes(notes):
    """
    create a chord from a list of notes.
    """
    return chord.Chord(notes) if notes else None

def eval_valid_progression(score, key_signature="C"):
    k = key.Key(key_signature)

    valid_progressions = {
        'V': ['IV6', 'vi'],
        'viio6': ['I'],
        'IV': ['I'],
        'vi': ['I', 'I6']
    }
    rightward_progression = ['I', 'vi', 'IV', 'ii', 'viio6', 'V']
    accepted_chords = ['I', 'i', 'ii', 'II', 'iii', 'III', 'iv' 'IV', 'v', "V", "vi", 'VI', 'viio', 'viio6', 'I6', 'IV6']

    valid_progressions_count = 0
    total_progressions = 0

    soprano, alto, tenor, bass = score.parts

    for measure_number in range(1, max(len(part.getElementsByClass('Measure')) for part in score.parts) + 1):
        measure_chords = []
        measure_notes = [p.measure(measure_number).flatten().notes for p in [soprano, alto, tenor, bass]]

        # create chords for each beat in the measure
        for i in range(max(len(notes) for notes in measure_notes)):
            current_notes = [notes[i] if i < len(notes) else None for notes in measure_notes]
            chord_assembled = create_chord_from_notes([n for n in current_notes if n is not None])
            if chord_assembled:
                measure_chords.append(chord_assembled)
        
        # analyze chord the progressions in this measure
        for i in range(len(measure_chords) - 1):
            try:
                current_chord = harmony.chordSymbolFromChord(measure_chords[i])
                next_chord = harmony.chordSymbolFromChord(measure_chords[i + 1])
                current_roman = current_chord.romanNumeral.figure
                next_roman = next_chord.romanNumeral.figure
            except pitch.AccidentalException:
                continue

            total_progressions += 1
            is_valid_progression = True
            
            # check if the progression is valid
            if current_roman not in accepted_chords:
                is_valid_progression = False

            if current_roman in valid_progressions and next_roman not in valid_progressions[current_roman]:
                is_valid_progression = False

            if current_roman in rightward_progression and next_roman not in rightward_progression[rightward_progression.index(current_roman):]:
                is_valid_progression = False

            if is_valid_progression:
                valid_progressions_count += 1

    # calculate the valid progression score
    valid_progression_score = (valid_progressions_count / total_progressions) * 100 if total_progressions > 0 else 0
    return valid_progression_score