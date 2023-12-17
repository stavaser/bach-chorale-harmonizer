from music21 import stream, environment, clef, tempo, chord, metadata, note
from datetime import datetime
import subprocess
import os

# TODO: REPLACE WITH YOUR OWN PATH TO MUSESCORE
MUSESCORE_PATH = "/Applications/MuseScore 4.app/Contents/MacOS/mscore"
environment.set('musescoreDirectPNGPath', MUSESCORE_PATH)


def convert_to_chorale_style(score):
    # grand staff
    grand_staff = stream.Score()
    treble_staff = stream.Part()
    bass_staff = stream.Part()

    # set clefs and tempo
    treble_staff.append(clef.TrebleClef())
    bass_staff.append(clef.BassClef())
    metronome_mark = tempo.MetronomeMark(number=70)
    grand_staff.append(metronome_mark)

    soprano, alto, tenor, bass = score.parts

    for measure in soprano.getElementsByClass('Measure'):
        # create chords for treble and bass measures
        treble_chords = []
        bass_chords = []

        # assemble notes from soprano and alto for treble chords
        for s_note, a_note in zip(soprano.measure(measure.number).notes, alto.measure(measure.number).notes):
            treble_chords.append(chord.Chord([s_note, a_note]))

        # assemble notes from tenor and bass for bass chords and transpose tenor notes down an octave
        for t_note, b_note in zip(tenor.measure(measure.number).notes, bass.measure(measure.number).notes):
            t_note_transposed = t_note.transpose('P-8', inPlace=False) if isinstance(t_note, note.Note) else t_note
            bass_chords.append(chord.Chord([t_note_transposed, b_note]))

        for ch in treble_chords:
            treble_staff.append(ch)
        for ch in bass_chords:
            bass_staff.append(ch)

    score_metadata = metadata.Metadata()
    score_metadata.title = "Generated JSB Chorale"
    score_metadata.composer = "chorale-harmonizer.py"

    grand_staff.insert(0, score_metadata)

    grand_staff.append(treble_staff)
    grand_staff.append(bass_staff)

    return grand_staff


def preprocess_chorale(chorale):
    # extract the Soprano line
    original_soprano = chorale.parts[0]
    soprano = stream.Part()
    soprano.id = 'Soprano'
    soprano.clef = clef.TrebleClef()

    # create empty Alto, Tenor, and Bass parts
    alto = stream.Part(id='Alto')
    tenor = stream.Part(id='Tenor')
    bass = stream.Part(id='Bass')

    measure_number = 1 

    for measure in original_soprano.getElementsByClass('Measure'):
        # clone the measure for soprano
        measure.number = measure_number
        soprano.append(measure)
        measure_number += 1

    # create a new score and add the parts
    new_score = stream.Score()
    new_score.append(soprano)
    new_score.append(alto)
    new_score.append(tenor)
    new_score.append(bass)


    return new_score



def save_score(score):
    timestamp = datetime.now().strftime("%b-%d-%I:%M:%S")
    filename = f"JSB-chorale-{timestamp}"
    folder_name = filename

    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    pdf_path = os.path.join(folder_name, f"{filename}.pdf")
    midi_path = os.path.join(folder_name, f"{filename}.mid")
    wav_path = os.path.join(folder_name, f"{filename}.wav")

    score.write("musicxml.pdf", fp=pdf_path)
    score.write("midi", fp=midi_path)

    subprocess.run([MUSESCORE_PATH, midi_path, "-o", wav_path])
