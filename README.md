
# Harmonzing JSB Chorales 
This is the code for the paper Composing Four-Part Bach Harmonies with Evolutionary Algorithms.

## Pre-reqs
In order to view the generated score, you need to have MuseScore 4 installed on your machine. 
Please refer to https://musescore.org/en/handbook/3/installation.
You also need Python 3.x+

## Installation
1. Clone the repo: `git clone https://github.com/stavaser/bach-chorale-harmonizer.git`
2. Navigate to the directory: `cd bach-chorale-harmonizer`
3. Create a virtual environment: `python3 -m venv venv`
4. Active the env on macOS/Linux: `source venv/bin/activate`
5. Install dependenices:
```
pip3 install music21
pip3 install pygame
pip3 install argparse
```
6. Set the env variable in `utils.py`:
   1. ensure `MUSESCORE_PATH` is the same as the MuseScore path on your machine


## Usage
Run 
```
python3 main.py --verbose=True --population_size=50 --generations=10 --encourage_diversity=True --use_intervalic_qualities=True --use_musescore=True
```

### Command-Line Arguments
* `xmlfile`: Path to your XML file. Use this to override the random Bach selection. If not provided, a random Bach chorale is selected.
* `verbose`: Boolean flag for verbose output. Default is True.
* `population_size`: Integer specifying the population size for the evolutionary algorithm. Default is 50.
* `generations`: Integer specifying the number of generations for the evolutionary algorithm. Default is 10.
* `encourage_diversity`: Boolean flag to encourage diversity in the evolutionary process. Default is True.
* `use_intervalic_qualities`: Boolean flag to use intervalic qualities in the fitness evaluation. Default is True.
* `use_musescore`: Boolean flag to use MuseScore for output. If False, the script will play the audio directly. Default is True.

## Examples
Run the harmonizer with default settings:

```
python3 main.py
```

Run the harmonizer with a specific XML file and custom settings:

```
python3 main.py --xmlfile=./path/to/file.xml --verbose=False --population_size=100 --generations=20 --encourage_diversity=False --use_intervalic_qualities=False --use_musescore=False
```

## Configuration
Adjust these weights to influence the style and characteristics of the generated chorale.

| Weight Key               | Default Value | Description |
|--------------------------|---------------|-------------|
| `eval_valid_progression` | 15.0          | Prioritizes the validity of chord progressions. Higher values emphasize adherence to traditional harmonic progression rules. |
| `eval_parallel_octaves`  | 1.0           | Penalizes parallel octaves. Increasing this value reduces the occurrence of parallel octaves in the harmonization. |
| `eval_parallel_fifths`   | 1.0           | Penalizes parallel fifths. A higher value discourages the use of parallel fifths. |
| `eval_parallel_unisons`  | 1.0           | Penalizes parallel unisons. Increasing this weight avoids parallel unisons in the harmonization. |
| `eval_tritones`          | 10.0          | Limits the usage of tritones, often considered dissonant. A higher weight will reduce tritones in the harmonization. |
| `eval_repeated_bass`     | 1.0           | Addresses the repetition of the bass note. Higher values discourage excessive repetition of the same bass note. |
| `eval_voice_ranges`      | 1.0           | Ensures that each voice stays within its comfortable singing range. |
| `eval_voice_closeness`   | 1.0           | Evaluates the closeness of voices. Promotes more spacing between the voices with higher values. |
| `eval_voice_crossing`    | 1.0           | Penalizes instances where voices cross each other. Higher values discourage voice crossing. |
| `eval_intervalic_quality`| 1.0           | Examines the intervalic quality between the Soprano line and a generated Bass line. The score is determined based on a probability matrix created from analyzing hundreds of Bach chorales, evaluating every possible interval between Soprano and Bass lines. |


