from music21 import *

def eval_repeated_bass(score):
    bass_part = score.parts[-1]

    total_transitions = 0
    repeated_notes_count = 0

    prev_note = None

    for measure in bass_part.getElementsByClass('Measure'):
        for note in measure.notes:
            if prev_note is not None:
                total_transitions += 1
                if note.name == prev_note.name:
                    repeated_notes_count += 1

            prev_note = note

    repeated_note_avoidance_score = 100 - (repeated_notes_count / total_transitions * 100) if total_transitions > 0 else 100

    return repeated_note_avoidance_score


def eval_tritones(score):
    total_intervals = 0
    tritone_count = 0

    # iterate through all parts and measures
    for part in score.parts:
        for measure in part.getElementsByClass('Measure'):
            notes = measure.notes

            # check each pair of notes for tritones
            for i in range(len(notes) - 1):
                for j in range(i + 1, len(notes)):
                    total_intervals += 1
                    intvl = interval.Interval(noteStart=notes[i], noteEnd=notes[j])
                    if intvl.simpleName == 'A4' or intvl.simpleName == 'd5':
                        tritone_count += 1

    tritone_avoidance_score = 100 - (tritone_count / total_intervals * 100) if total_intervals > 0 else 100

    return tritone_avoidance_score