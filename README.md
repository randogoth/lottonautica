# Lottonautica

![image](https://github.com/user-attachments/assets/6a946397-fbdb-4a86-8e8b-7bf658f09fa3)

## Random Lottery Number Generator

This Python program generates lottery numbers using random entropy, statistical analysis, and Z-score-based cluster detection using [Lyagushka](https://github.com/randogoth/lyagushka). It identifies clusters in a dataset to select attractor points, which are then scaled and presented as lottery numbers.

---

## Features

- Generates random data using Randonautica's quantum random number generator.
- Identifies clusters of numbers as attractors quantified by z-scores.
- Draws main lottery numbers and a bonus ball (Mega Millions).
- Provides a progress bar and rich console output.
- Fully configurable with user inputs for lottery size and z-score thresholds.

---

## Installation

### Prerequisites

- Python 3.12
- `pipenv` for dependency management

### Setup

1. Clone the repository and navigate to its directory.
2. Install dependencies using `pipenv`:
   ```bash
   pipenv install
   ```
3. Activate the virtual environment:
   ```bash
   pipenv shell
   ```

---

## Usage

Run the program with the following command:

```bash
python main.py
```

### Configuration Prompts

- **Number of Balls to Draw**: Total numbers in the main lottery draw (default: 5).
- **Range of Lottery Numbers**: Maximum number in the main lottery (default: 70).
- **Range of Bonus Ball**: Maximum number for the bonus ball (default: 25).
- **Minimum Z-Score Threshold**: Threshold for identifying attractor clusters (default: 3.0). Below 2.0 it is statistically insignificant. Above 4.0 it is highly anomalous. Pick something between 2.0 and 4.0.
