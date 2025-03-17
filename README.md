# Rubik's Cube Solver

A Python program that solves Rubik's cube configurations using an efficient two-phase algorithm with 3D visualization capabilities.

## Prerequisites

- Python 3.x
- VPython (for visualization)

## Installation

1. Clone the repository:

```bash
git clone <repository-url>
cd rubik
```

2. Set up the environment and install dependencies:

```bash
make
```

## Usage

### Basic Usage

```bash
python3 main.py "U R2 F' D"
```

This will solve a cube that has been scrambled with the moves U, R2, F', D

### Random Scramble

```bash
python3 main.py -r 20
```

This will generate and solve a random scramble of 20 moves

### With Visualization

```bash
python3 main.py "U R2 F' D" -v
```

This will show a 3D visualization of both the scramble and solution

## Options

- `-r, --random [LENGTH]`: Generate a random scramble of specified length
- `-v, --visualizer`: Enable 3D visualization

## Output

The program provides detailed solution information including:

- Solution status (success/failure)
- Half Turn Metric (HTM) count
- Time taken to find solution
- Complete solution sequence

## Make Commands

- `make`: Create virtual environment and install dependencies
- `make clean`: Delete compiled Python files
- `make fclean`: Delete virtual environment and generated files
- `make re`: Reset everything
- `make help`: Display available commands

## Example

```bash
python3 main.py "R U R' U'"

=================================================
                    RESULTS                  
=================================================

Status: Success - Cube solved!

Metrics:
  • HTM (Half Turn Metric): 4
  • Time to solve: 0.023s

Solution:
 U R U' R'

=================================================
```
