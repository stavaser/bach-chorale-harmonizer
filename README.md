
# Harmonzing JSB Chorales 
This is the code for the paper Composing Four-Part Bach Harmonies with Evolutionary Algorithms.

## Pre-reqs
In order to view the generated score, you need to have MuseScore 4 installed on your machine. 
Please refer to https://musescore.org/en/handbook/3/installation.
You also need Python3.x+

## Installation
1. Clone the repo: `git clone https://github.com/stavaser/bach-chorale-harmonizer.git`
2. Navigate to the directory: `cd bach-chorale-harmonizer`
3. Create a virtual environment: `python3 -m venv venv`
4. Active the env on macOS/Linux: `source venv/bin/activate`
5. Install dependenices: `pip3 install music21`


## Usage
run 
```
python3 chorale-harmonizer.py
```

The program will randomly select a soprano line from Bach's chorales and generate harmonizations for it.
You can customize the parameters (population size, mutation rate, etc.) in the main() function.
The final output will be displayed in MuseScore.

## Configuration

You can modify several parameters in the main() function:

- `population_size`: number of harmonizations in each generation.
- `generation`s: number of evolutionary cycles.
- `weights`: dictates the importance of different musical aspects in fitness evaluation.
- `encourage_diversity`: switches to tournament parent selection
- `use_intervalic_qualities`: use the probability matrix generated from hundreds of Bach chorales in evaluation process

