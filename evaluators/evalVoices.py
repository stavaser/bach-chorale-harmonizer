from music21 import *


# valid ranges for each voice part
valid_ranges = {
    'Soprano': (pitch.Pitch('C4'), pitch.Pitch('g5')),
    'Alto': (pitch.Pitch('G3'), pitch.Pitch('d5')),
    'Tenor': (pitch.Pitch('C3'), pitch.Pitch('G4')),
    'Bass': (pitch.Pitch('f2'), pitch.Pitch('C4'))
}

def eval_voice_ranges(score):
    # store the count of notes within and outside the valid range
    note_counts = {'Soprano': [0, 0], 'Alto': [0, 0], 'Tenor': [0, 0], 'Bass': [0, 0]}  # [within range, outside range]

    part_names = ['Soprano', 'Alto', 'Tenor', 'Bass']

    # check each part for range violations
    for part_index, part in enumerate(score.parts):
        voice_part = part_names[part_index]
        for note in part.recurse().getElementsByClass('Note'):
            if valid_ranges[voice_part][0] <= note.pitch <= valid_ranges[voice_part][1]:
                note_counts[voice_part][0] += 1
            else:
                note_counts[voice_part][1] += 1

    # calculate the score for each voice
    scores = []
    for part, counts in note_counts.items():
        total_notes = sum(counts)
        if total_notes > 0:
            score = (counts[0] / total_notes) * 100
            scores.append(score)

    # avg score across all parts
    bachness_score = sum(scores) / len(scores) if scores else 0

    return bachness_score

def check_voice_ranges(score):
    # for storing the notes outside the valid range
    out_of_range_notes = {'Soprano': [], 'Alto': [], 'Tenor': [], 'Bass': []}

    part_names = ['Soprano', 'Alto', 'Tenor', 'Bass']

    # check each part for range violations
    for part_index, part in enumerate(score.parts):
        voice_part = part_names[part_index]
        for note in part.recurse().getElementsByClass('Note'):
            if note.pitch < valid_ranges[voice_part][0] or note.pitch > valid_ranges[voice_part][1]:
                out_of_range_notes[voice_part].append(f"{note.pitch} in measure {note.measureNumber}")

    return out_of_range_notes

def eval_voice_closeness(score):
    soprano, alto, tenor, bass = score.parts

    # count of measures with acceptable and unacceptable distances
    acceptable_distances_count = 0
    total_measures = 0

    # get maximum number of measures in any part
    max_measures = max(len(part.getElementsByClass('Measure')) for part in score.parts)

    for measure_number in range(1, max_measures + 1):
        total_measures += 1

        # find the highest note in each measure for each part
        soprano_note = soprano.measure(measure_number).pitches[-1] if soprano.measure(measure_number).pitches else None
        alto_note = alto.measure(measure_number).pitches[-1] if alto.measure(measure_number).pitches else None
        tenor_note = tenor.measure(measure_number).pitches[-1] if tenor.measure(measure_number).pitches else None
        bass_note = bass.measure(measure_number).pitches[-1] if bass.measure(measure_number).pitches else None

        # check each required distance
        distances_acceptable = True
        if soprano_note and bass_note and interval.Interval(bass_note, soprano_note).semitones > 19: # More than a 12th
            distances_acceptable = False
        if soprano_note and alto_note and interval.Interval(alto_note, soprano_note).semitones > 12: # More than an octave
            distances_acceptable = False
        if alto_note and tenor_note and interval.Interval(tenor_note, alto_note).semitones > 12: # More than an octave
            distances_acceptable = False

        if distances_acceptable:
            acceptable_distances_count += 1

    closeness_score = (acceptable_distances_count / total_measures) * 100 if total_measures > 0 else 0

    return closeness_score

def check_voice_closeness(score):
    soprano, alto, tenor, bass = score.parts
    distance_issues = []

    for i, measure in enumerate(score.measures(1, None)):
        measure_number = i + 1

        # get the highest note in each measure for each part
        soprano_note = soprano.measure(measure_number).pitches[-1] if soprano.measure(measure_number).pitches else None
        alto_note = alto.measure(measure_number).pitches[-1] if alto.measure(measure_number).pitches else None
        tenor_note = tenor.measure(measure_number).pitches[-1] if tenor.measure(measure_number).pitches else None
        bass_note = bass.measure(measure_number).pitches[-1] if bass.measure(measure_number).pitches else None

        # check each required distance
        if soprano_note and bass_note and interval.Interval(bass_note, soprano_note).semitones > 19: # More than a 12th
            distance_issues.append(f"Distance between Bass and Soprano too large in measure {measure_number}")

        if soprano_note and alto_note and interval.Interval(alto_note, soprano_note).semitones > 12: # More than an octave
            distance_issues.append(f"Distance between Alto and Soprano too large in measure {measure_number}")

        if alto_note and tenor_note and interval.Interval(tenor_note, alto_note).semitones > 12: # More than an octave
            distance_issues.append(f"Distance between Tenor and Alto too large in measure {measure_number}")

    return distance_issues

def eval_voice_crossing(score):
    soprano, alto, tenor, bass = score.parts

    measures_without_crossing = 0
    total_measures = 0

    # get maximum number of measures in any part
    max_measures = max(len(part.getElementsByClass('Measure')) for part in score.parts)

    for measure_number in range(1, max_measures + 1):
        total_measures += 1

        # get notes for each part in the measure
        soprano_notes = soprano.measure(measure_number).pitches if soprano.measure(measure_number) else []
        alto_notes = alto.measure(measure_number).pitches if alto.measure(measure_number) else []
        tenor_notes = tenor.measure(measure_number).pitches if tenor.measure(measure_number) else []
        bass_notes = bass.measure(measure_number).pitches if bass.measure(measure_number) else []

        # check for voice crossing
        voice_crossing = False
        if soprano_notes and alto_notes and soprano_notes[-1] < alto_notes[-1]:
            voice_crossing = True
        if alto_notes and tenor_notes and alto_notes[-1] < tenor_notes[-1]:
            voice_crossing = True
        if tenor_notes and bass_notes and tenor_notes[-1] < bass_notes[-1]:
            voice_crossing = True

        if not voice_crossing:
            measures_without_crossing += 1

    voice_crossing_score = (measures_without_crossing / total_measures) * 100 if total_measures > 0 else 0

    return voice_crossing_score

def check_voice_crossing(score):
    soprano, alto, tenor, bass = score.parts

    voice_crossing_issues = []

    for i, measure in enumerate(score.measures(1, None)):
        measure_number = i + 1

        # get notes for each part in the measure
        soprano_notes = soprano.measure(measure_number).pitches
        alto_notes = alto.measure(measure_number).pitches
        tenor_notes = tenor.measure(measure_number).pitches
        bass_notes = bass.measure(measure_number).pitches

        # check for voice crossing
        if soprano_notes and alto_notes and soprano_notes[-1] < alto_notes[-1]:
            voice_crossing_issues.append(f"Soprano and Alto crossing in measure {measure_number}")

        if alto_notes and tenor_notes and alto_notes[-1] < tenor_notes[-1]:
            voice_crossing_issues.append(f"Alto and Tenor crossing in measure {measure_number}")

        if tenor_notes and bass_notes and tenor_notes[-1] < bass_notes[-1]:
            voice_crossing_issues.append(f"Tenor and Bass crossing in measure {measure_number}")

    return voice_crossing_issues


def eval_voices(chorale):
    out = []

    ranges = eval_voice_ranges(chorale)
    close = eval_voice_closeness(chorale)
    cross = eval_voice_crossing(chorale)
    out.append(ranges)
    out.append(close)
    out.append(cross)
    
    return out
