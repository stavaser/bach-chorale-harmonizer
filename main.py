import argparse
import random
import music21
from chorale_harmonizer import FitnessEvaluator, EvolutionaryChoraleHarmonizer
from utils import preprocess_chorale, convert_to_chorale_style, save_score

def parse_arguments():
    parser = argparse.ArgumentParser(description="Chorale Harmonizer")
    parser.add_argument("--xmlfile", help="Path to your XML file, use this to override random Bach selection", default="")
    parser.add_argument("--verbose", type=bool, default=True, help="Verbose output (default: True)")
    parser.add_argument("--population_size", type=int, default=50, help="Population size (default: 50)")
    parser.add_argument("--generations", type=int, default=10, help="Number of generations (default: 10)")
    parser.add_argument("--encourage_diversity", type=bool, default=True, help="Encourage diversity (default: True)")
    parser.add_argument("--use_intervalic_qualities", type=bool, default=True, help="Use intervalic qualities (default: True)")
    parser.add_argument("--use_musescore", type=bool, default=True, help="Use MuseScore for output (default: True)")
    return parser.parse_args()

def load_data(xmlfile):
    if xmlfile:
        return music21.converter.parse(xmlfile)
    else:
        bach_chorales = music21.corpus.getComposer('bach')
        random_chorale = random.choice(bach_chorales)
        chorale = music21.converter.parse(random_chorale)
        return preprocess_chorale(chorale)

def create_harmonizer(data, args):
    # tweak weights here
    weights = {
        "eval_valid_progression": 15.0,
        "eval_parallel_octaves": 1.0,
        "eval_parallel_fifths": 1.0,
        "eval_parallel_unisons": 1.0,
        "eval_tritones": 10.0,
        "eval_repeated_bass": 1.0,
        "eval_voice_ranges": 1.0,
        "eval_voice_closeness": 1.0,
        "eval_voice_crossing": 1.0,
        "eval_intervalic_quality": 1.0,
    }

    fitness_evaluator = FitnessEvaluator(weights=weights, use_intervalic_qualities=args.use_intervalic_qualities)

    return EvolutionaryChoraleHarmonizer(
        soprano_part=data,
        population_size=args.population_size,
        mutation_rate=0.05,
        fitness_evaluator=fitness_evaluator,
        verbose=args.verbose,
        encourage_diversity=args.encourage_diversity
    )


def main():
    args = parse_arguments()
    melody = load_data(args.xmlfile)
    harmonizer = create_harmonizer(melody, args)
    generated_chorale = harmonizer.harmonize(generations=args.generations)
    score = convert_to_chorale_style(generated_chorale)

    if args.use_musescore:
        save_score(score)
    sp = music21.midi.realtime.StreamPlayer(score)
    sp.play()


if __name__ == "__main__":
    main()
