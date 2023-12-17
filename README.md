
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

You can modify several parameters in the main() function:

- `population_size`: number of harmonizations in each generation.
- `generation`s: number of evolutionary cycles.
- `weights`: dictates the importance of different musical aspects in fitness evaluation.
- `encourage_diversity`: switches to tournament parent selection
- `use_intervalic_qualities`: use the probability matrix generated from hundreds of Bach chorales in evaluation process

