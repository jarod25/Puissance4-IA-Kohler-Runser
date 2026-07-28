# Connect Four AI

A Python implementation of Connect Four featuring a Tkinter interface and an AI player based on minimax search with alpha-beta pruning.

The project was developed as a two-person academic project at ENSISA. Its objective was to explore adversarial search, heuristic evaluation and performance improvements while keeping the game directly playable through a graphical interface.

## Features

- human-versus-human, human-versus-AI and AI-versus-AI games
- configurable AI search depth
- minimax search with alpha-beta pruning
- move ordering that prioritises central columns
- heuristic evaluation for offensive and defensive positions
- different heuristic weighting for early, middle and late game states
- experimental root-move parallelisation with a sequential fallback
- graphical interface built with Tkinter

## AI approach

The AI evaluates possible moves through alternating minimizing and maximizing search steps. Alpha-beta pruning avoids exploring branches that cannot affect the final decision.

When the search reaches its depth limit, the board is evaluated using several heuristics:

- positional weighting that favours central cells and useful board areas
- detection of two-piece and three-piece alignments
- stronger defensive penalties when the opponent is close to winning
- terminal scoring for winning and losing positions
- phase-dependent weighting based on the number of occupied cells

Available AI levels correspond to different search depths. Higher values increase computation time significantly because the search space grows exponentially.

## Requirements

- Python 3
- NumPy
- Tkinter, usually included with standard Python installations on Windows and macOS

On some Linux distributions, Tkinter must be installed separately through the system package manager.

## Installation

Clone the repository:

```bash
git clone https://github.com/jarod25/Puissance4-IA-Kohler-Runser.git
cd Puissance4-IA-Kohler-Runser
```

Create and activate a virtual environment:

```bash
python -m venv .venv
```

On Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

On Linux or macOS:

```bash
source .venv/bin/activate
```

Install the Python dependency:

```bash
pip install -r requirements.txt
```

## Run the game

```bash
python Puissance4_RUNSER_KOHLER.py
```

Choose the player type for each side, then start a new game. AI levels represent the search depth used for move evaluation.

## Project structure

- `Puissance4_RUNSER_KOHLER.py` contains the graphical interface, board model and alpha-beta search
- `heuristiques.py` contains the board evaluation functions
- `Puissance-4-Rapport_RUNSER_KOHLER.pdf` contains the original academic report in French

## Current limitations

- high search depths can require a very long computation time
- the parallel evaluation path depends on the operating system and multiprocessing start method
- the interface does not currently provide an in-game explanation of heuristic scores
- automated tests and benchmark results are not yet included
- the project documentation does not currently include screenshots or a video demonstration

## Authors

- [Jarod Kohler](https://github.com/jarod25)
- [Lucas Runser](https://github.com/Naegi-UHA)

## License

No license is currently specified for this project.
