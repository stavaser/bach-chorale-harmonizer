import random
from evaluators.evalParallels import *
from evaluators.evalVoiceLeading import *
from evaluators.evalVoices import *
from evaluators.evalHarmony import *

import music21

class EvolutionaryChoraleHarmonizer:

    def __init__(
        self,
        soprano_part,
        population_size,
        mutation_rate,
        fitness_evaluator,
        verbose = True,
        encourage_diversity = True,
    ):
        print(f"[🌀] Initializing the Evolutionary Chorale Harmonizer...")
        # flags
        self.verbose = verbose
        self.encourage_diversity = encourage_diversity

        # evolutionary params
        self.soprano_part = soprano_part
        self.mutation_rate = mutation_rate
        self.population_size = population_size
        self.fitness_evaluator = fitness_evaluator
        self._population = []
        
        # voice ranges
        self.alto_range = (pitch.Pitch('G3'), pitch.Pitch('d5'))
        self.tenor_range = (pitch.Pitch('C3'), pitch.Pitch('G4'))
        self.bass_range = (pitch.Pitch('f2'), pitch.Pitch('C4'))
        
        # computed data
        self.note_duration = 0
        self.number_of_notes = 0
        self.number_of_bars = 0
        self.harmony_dict = {}
        self.__post_init__()

    def _create_harmony_dict(self):
        notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        harmony_dict = {}

        for note_name in notes:
            current_note = music21.note.Note(note_name)

            # generate chords where the current note is the root, third, fifth, or seventh
            chords = self._generate_triads(current_note)

            # flatten the list of notes and get their names, remove duplicates
            compatible_notes = list(set([n.nameWithOctave for chord in chords for n in chord]))

            harmony_dict[note_name] = compatible_notes

        return harmony_dict

    def _generate_triads(self, note):
        chords = []

        # generate chords where the note is the root
        chords.append(self._generate_chord(note, ['P1', 'M3', 'P5']))  # Major triad
        chords.append(self._generate_chord(note, ['P1', 'm3', 'P5']))  # Minor triad

        # TODO
        # calculate the possible chords where the note is the third, fifth, or seventh
        # for interval_str in ['m3', 'M3', 'P5']:
        #     inverted_interval = music21.interval.Interval(interval_str).complement
        #     root_of_chord = note.transpose(inverted_interval, inPlace=False)
        #     chords.extend([
        #         self._generate_chord(root_of_chord, ['P1', 'M3', 'P5']),
        #         self._generate_chord(root_of_chord, ['P1', 'm3', 'P5']),
        #         # self._generate_chord(root_of_chord, ['P1', 'M3', 'P5', 'M7']),
        #         # self._generate_chord(root_of_chord, ['P1', 'm3', 'P5', 'm7']),
        #         # self._generate_chord(root_of_chord, ['P1', 'M3', 'P5', 'm7']),
        #         # self._generate_chord(root_of_chord, ['P1', 'm3', 'd5', 'm7']),
        #         # self._generate_chord(root_of_chord, ['P1', 'm3', 'd5', 'd7'])
        #     ])

        return chords

    def _generate_chord(self, root_note, intervals):
        return [root_note.transpose(music21.interval.Interval(interval_str), inPlace=False) for interval_str in intervals]

    def __post_init__(self):
        total_duration = 0
        note_count = 0
        nonempty_bar_count = 0

        for element in self.soprano_part.parts[0]:
            if isinstance(element, stream.Measure):
                if element.notes: 
                    nonempty_bar_count += 1
                    for note in element.notes:
                        total_duration += note.duration.quarterLength
                        note_count += 1

        self.note_duration = total_duration
        self.number_of_notes = note_count
        self.number_of_bars = nonempty_bar_count
        self.harmony_dict = self._create_harmony_dict()
        # print(self.harmony_dict)

        print(f"[✅] Initialized a soprano line with a total of {note_count} notes with the duration of {total_duration} time units and a non-empty measure count of {nonempty_bar_count}.")

    def harmonize(self, generations=1000):

        self._population = self._initialize_population()
        print(f"[✅] Initialized a random population with {self.population_size} entities.")
        print(f"[🌀] Going to start evolution for {generations} generations.")

        for i in range(generations):
            print(f"[Generation {i}]")
            parents = self._select_parents()
            new_population = self._create_new_population(parents)
            self._population = new_population

        print(f"[🔥] The evolution has concluded. Presenting the final harmony...")

        best_harmony = (
            self.fitness_evaluator.get_best_harmony(
                self._population,
                self.verbose
            )
        )
        return best_harmony
    

    def _initialize_population(self):
        return [
            self._generate_random_chorale()
            for _ in range(self.population_size)
        ]

    # def _generate_random_line(self, part_range):
    #     part = stream.Part()
    #     measure_number = 1

    #     for element in self.soprano_part.parts[0].getElementsByClass(stream.Measure):
    #         new_measure = stream.Measure(number=measure_number)
    #         measure_number += 1

    #         for n in element.notes:
    #             random_pitch = pitch.Pitch(random.randint(part_range[0].midi, part_range[1].midi))
    #             new_note = note.Note(random_pitch,
    #                                  quarterLength=n.duration.quarterLength)
    #             new_measure.append(new_note)

    #         part.append(new_measure)

    #     return part


    def _generate_random_line(self, part_range):
        part = stream.Part()
        measure_number = 1

        for element in self.soprano_part.parts[0].getElementsByClass(stream.Measure):
            new_measure = stream.Measure(number=measure_number)
            measure_number += 1

            for note in element.notes:
                # get harmonically compatible notes from the dictionary

                note_name = None
                if note.name not in self.harmony_dict:
                    note_name = note.pitch.getEnharmonic().name
                else:
                    note_name = note.name
                compatible_notes = self.harmony_dict[note_name]

                # choose a random pitch from the compatible notes
                random_pitch_name = random.choice(compatible_notes)
                random_pitch = pitch.Pitch(random_pitch_name)

                # transpose the chosen note into the part range
                random_pitch = self._transpose_to_range(random_pitch, part_range)
                new_note = music21.note.Note(random_pitch, quarterLength=note.duration.quarterLength)
                new_measure.append(new_note)

            part.append(new_measure)

        return part

    def _transpose_to_range(self, pitch_name, part_range):
        initial_octave = 4
        p = pitch.Pitch(f"{pitch_name}{initial_octave}")

        # transpose the pitch to the correct range
        while p.midi < part_range[0].midi:
            p.octave += 1
        while p.midi > part_range[1].midi:
            p.octave -= 1
        return p
        
    def _generate_random_chorale(self):
        alto_part = self._generate_random_line(self.alto_range)
        tenor_part = self._generate_random_line(self.tenor_range)
        bass_part = self._generate_random_line(self.bass_range)

        # set part names and clefs
        self.soprano_part.parts[0].clef = clef.TrebleClef()
        self.soprano_part.parts[0].id = 'Soprano'

        alto_part.clef = clef.TrebleClef()
        alto_part.id = 'Alto'

        tenor_part.clef = clef.Treble8vbClef()
        tenor_part.id = 'Tenor'

        bass_part.clef = clef.BassClef()
        bass_part.id = 'Bass'


        # create a score and add the parts
        score = stream.Score()

        score_metadata = metadata.Metadata()
        score_metadata.title = "initial population"
        score.insert(0, score_metadata)

        score.append(self.soprano_part.parts[0])
        score.append(alto_part)
        score.append(tenor_part)
        score.append(bass_part)

        return score

    def _diverse_parent_selection_strategy(self):
        initial_fitness_values = [
            self.fitness_evaluator.evaluate(seq) for seq in self._population
        ]

        max_fitness = max(initial_fitness_values)
        if self.verbose:
            max_index = initial_fitness_values.index(max_fitness)
            highest_scoring_entity = self._population[max_index]

            self.fitness_evaluator._print_scores(highest_scoring_entity)
        else:
            print(f"Total Score: {max_fitness:.2f}")

        parents = []
        available_indices = list(range(len(self._population)))
        current_fitness_values = initial_fitness_values.copy()

        while len(parents) < self.population_size and available_indices:
            chosen_index = random.choices(available_indices, weights=current_fitness_values, k=1)[0]
            parents.append(self._population[chosen_index])

            # find the index in available_indices and remove it and its corresponding fitness value
            index_in_available = available_indices.index(chosen_index)
            available_indices.pop(index_in_available)
            current_fitness_values.pop(index_in_available)

        return parents

    def _fittest_parent_selection_strategy(self):
            fitness_values = [
                self.fitness_evaluator.evaluate(seq) for seq in self._population
            ]

            max_fitness = max(fitness_values)
            if self.verbose:
                max_index = fitness_values.index(max_fitness)
                highest_scoring_entity = self._population[max_index]

                self.fitness_evaluator._print_scores(highest_scoring_entity)
            else:
                print(f"Total Score: {max_fitness:.2f}")

            parents = random.choices(
                self._population, weights=fitness_values, k=self.population_size
            )

            return parents

    def _select_parents(self):
        if self.encourage_diversity:
            return self._diverse_parent_selection_strategy()
        else:
            return self._fittest_parent_selection_strategy()

    def _create_new_population(self, parents):
        new_population = []
        for i in range(0, self.population_size, 2):
            child1 = self._crossover(parents[i], parents[i + 1])
            child2 = self._crossover(parents[i + 1], parents[i])
            # TODO
            # child1 = self._mutate(child1)
            # child2 = self._mutate(child2)
            new_population.extend([child1, child2])
        return new_population

    def _crossover(self, parent1, parent2):
        child = stream.Score()

        for partIndex in range(len(parent1.parts)):
            parent1Part = parent1.parts[partIndex]
            parent2Part = parent2.parts[partIndex]
            
            childPart = stream.Part()
            childPart.clef = parent1Part.clef

            pivotChordIndex = random.randint(1, self.number_of_notes - 1)
            currentChordIndex = 0
            switchToParent2 = False

            for measureIndex, (m1, m2) in enumerate(zip(parent1Part.getElementsByClass(stream.Measure), parent2Part.getElementsByClass(stream.Measure))):
                childMeasure = stream.Measure(number=measureIndex + 1)
                sourceMeasure = m2 if switchToParent2 else m1

                for el in sourceMeasure:
                    currentChordIndex += 1
                    if currentChordIndex == pivotChordIndex:
                        switchToParent2 = True

                    childMeasure.append(el)

                childPart.append(childMeasure)

            child.append(childPart)
        
        return child

    
    # TODO
    def _mutate(self, chorale):
        return chorale

class FitnessEvaluator:
    def __init__(
        self, 
        weights,
        use_intervalic_qualities=False,
    ):
        print(f"[🌀] Initializing the Fitness Evaluator...")
        self.weights = weights
        self.use_intervalic_qualities = use_intervalic_qualities

        # initialize empty matrix with shape (25,25,25)
        self.probability_matrix = {v_dist: {s_dist: {b_dist: 0.0 for b_dist in range(-12, 13)}
                                    for s_dist in range(-12, 13)}
                            for v_dist in range(-12, 13)}

        if use_intervalic_qualities:
            self._populate_prob_matrix()

            self.probability_matrix[0][0][0] = 100
            self.probability_matrix[4][-1][7] = 100

    def _calculate_distances(self, soprano, bass, idx):
        soprano_note = soprano[idx]
        bass_note = bass[idx]
        next_bass_note = bass[idx + 1] if idx + 1 < len(bass) else bass[idx]
        next_soprano_note = soprano[idx + 1] if idx + 1 < len(soprano) else soprano[idx]

        # extract pitches guarding against chords
        soprano_pitch = soprano_note.pitches[0] if isinstance(soprano_note, music21.chord.Chord) else soprano_note.pitch
        bass_pitch = bass_note.pitches[0] if isinstance(bass_note, music21.chord.Chord) else bass_note.pitch
        next_bass_pitch = next_bass_note.pitches[0] if isinstance(next_bass_note, music21.chord.Chord) else next_bass_note.pitch
        next_soprano_pitch = next_soprano_note.pitches[0] if isinstance(next_soprano_note, music21.chord.Chord) else next_soprano_note.pitch

        # now calculate the intervals
        soprano_to_bass = interval.Interval(noteStart=soprano_pitch, noteEnd=bass_pitch)
        bass_to_next_bass = interval.Interval(noteStart=bass_pitch, noteEnd=next_bass_pitch)
        soprano_to_next_soprano = interval.Interval(noteStart=soprano_pitch, noteEnd=next_soprano_pitch)


        x0_val = soprano_to_bass.semitones
        z0_val = bass_to_next_bass.semitones
        w0_val = soprano_to_next_soprano.semitones

        x0_dir = -1 if x0_val < 0 else 1
        z0_dir = -1 if z0_val < 0 else 1
        w0_dir = -1 if w0_val < 0 else 1

        x0 = x0_dir * (abs(x0_val) % 12)
        z0 = z0_dir * (abs(z0_val) % 12)
        w0 = w0_dir * (abs(w0_val) % 12)
        return x0, w0, z0

    def _populate_prob_matrix(self):
        print(f"[🌀] Creating a probability matrix of intervals...")

        # load all Bach chorales from the music21 corpus
        bach_chorales = corpus.getComposer('bach')

        for chorale_path in bach_chorales:
            chorale = corpus.parse(chorale_path)
            n = min(len(chorale.parts[0].flatten().notes), len(chorale.parts[-1].flatten().notes))
            for i in range(n-1):
                v_dist, s_dist, b_dist = self._calculate_distances(chorale.parts[0].flatten().notes, chorale.parts[-1].flatten().notes, i)
                if v_dist in self.probability_matrix:
                    if s_dist in self.probability_matrix[v_dist]:
                        if b_dist in self.probability_matrix[v_dist][s_dist]:
                            self.probability_matrix[v_dist][s_dist][b_dist] += 1

        # non_zero_items = []
        # for v_dist in range(-12, 13):
        #     for s_dist in range(-12, 13):
        #         for b_dist in range(-12, 13):
        #             probability = self.probability_matrix[v_dist][s_dist][b_dist]
        #             if probability > 0:
        #                 non_zero_items.append((v_dist, s_dist, b_dist, probability))


        print(f"[✅] Probability matrix created!")

    def get_best_harmony(self, chorales, verbose):
        # create (chorale, fitness) tuple
        chorales_with_fitness = [(seq, self.evaluate(seq)) for seq in chorales]

        best_chorale, max_fitness = max(chorales_with_fitness, key=lambda item: item[1])

        if verbose:
            self._print_scores(best_chorale)
        else:
            print(f"Total Score: {max_fitness:.2f}")

        return best_chorale

    
    def evaluate(self, chorale):
        return sum(
            self.weights[func] * getattr(self, f"_{func}")(chorale)
            for func in self.weights
        )

    def _print_scores(self, chorale):
        print("Score Breakdown:")
        print("{:<20} {:<10} {:<10} {:<15}".format("Function", "Weight", "Score", "Weighted Score"))
        print("-" * 55)

        total_score = 0
        for func in self.weights:
            weight = self.weights[func]
            function_score = getattr(self, f"_{func}")(chorale)
            weighted_score = weight * function_score
            total_score += weighted_score
            print("{:<20} {:<10} {:<10} {:<15}".format(func, f"{weight:.2f}", f"{function_score:.2f}", f"{weighted_score:.2f}"))

        print("-" * 55)
        print(f"Total Score: {total_score:.2f}")

        
    _eval_valid_progression = staticmethod(eval_valid_progression)
    _eval_parallel_octaves = staticmethod(eval_parallel_octaves)
    _eval_parallel_fifths = staticmethod(eval_parallel_fifths)
    _eval_parallel_unisons = staticmethod(eval_parallel_unisons)
    _eval_tritones = staticmethod(eval_tritones)
    _eval_repeated_bass = staticmethod(eval_repeated_bass)
    _eval_voice_ranges = staticmethod(eval_voice_ranges)
    _eval_voice_closeness = staticmethod(eval_voice_closeness)
    _eval_voice_crossing = staticmethod(eval_voice_crossing)

    def _eval_intervalic_quality(self, chorale):
        score = 0.0
        soprano = chorale.parts[0].flatten().notes
        bass = chorale.parts[-1].flatten().notes

        N = min(len(soprano), len(bass))

        for i in range(N-1):
            soprano_to_bass = interval.Interval(noteStart=soprano[i], noteEnd=bass[i])
            soprano_interval = interval.Interval(noteStart=soprano[i], noteEnd=soprano[i+1])
            bass_interval = interval.Interval(noteStart=bass[i], noteEnd=bass[i+1])

            x0_val = soprano_to_bass.semitones
            z0_val = bass_interval.semitones
            w0_val = soprano_interval.semitones

            x0_dir = -1 if x0_val < 0 else 1
            z0_dir = -1 if z0_val < 0 else 1
            w0_dir = -1 if w0_val < 0 else 1

            x0 = x0_dir * (abs(x0_val) % 12)
            z0 = z0_dir * (abs(z0_val) % 12)
            w0 = w0_dir * (abs(w0_val) % 12)

            if x0 in self.probability_matrix:
                if w0 in self.probability_matrix[x0]:
                    if z0 in self.probability_matrix[x0][w0]:
                        if self.probability_matrix[x0][w0][z0] > 0:
                            score += self.probability_matrix[x0][w0][z0]

        return score