from lyagushka import Lyagushka
from randonautentropy import rndo
import json
import questionary
from rich.console import Console
from rich.text import Text
from rich.progress import Progress, TextColumn, BarColumn

# Validate if a string can be converted to a float
def can_be_float(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

# Generate random data with a specified size and maximum value
def generate_random_data(size=1024, max_value=100):
    random_data = []
    # Calculate the number of bytes required to represent the max value
    max_value_bytes = (max_value.bit_length() + 7) // 8
    max_int_for_bytes = 2**(max_value_bytes * 8) - 1
    # Define the cutoff to ensure uniform distribution
    mod_cutoff = max_int_for_bytes - (max_int_for_bytes % max_value) - 1

    while len(random_data) < size:
        # Generate random hexadecimal data
        hex_data = rndo.get(length=max_value_bytes * size)
        # Process the hex data in chunks
        for i in (hex_data[j:j + 2 * max_value_bytes] for j in range(0, len(hex_data), 2 * max_value_bytes)):
            num = int(i, 16)  # Convert hex chunk to integer
            if num <= mod_cutoff:
                # Add the value to random_data if within the cutoff
                random_data.append(num % (max_value + 1))
                # Break early if enough data is collected
                if len(random_data) >= size:
                    break
    return random_data

# Analyze and select numbers based on Z-score
def pull_number(numbers: set, top: int, amount: int, z_score: float):
    
    # Generate and sort a dataset of random numbers
    dataset = generate_random_data(3000, 999)
    dataset.sort()
    
    # Analyze the dataset using Lyagushka
    zhaba = Lyagushka(dataset)
    analysis_results = json.loads(zhaba.search(4.0, 30))

    # Filter results for valid Z-scores
    results = [obj for obj in analysis_results if obj['z_score'] is not None]
    max_z_score = max(obj['z_score'] for obj in results)

    for obj in results:
        # Check if the object has the maximum Z-score and meets the threshold
        if obj['z_score'] == max_z_score and obj['z_score'] >= z_score:
            # Ensure the centroid is not an x.5 and add the scaled value
            if len(numbers) < amount and (obj['centroid'] % 1 != 0.5):
                numbers.add(int((obj['centroid'] / 999) * top) + 1)
    return numbers

# Main function to drive the lottery draw process
def main():
    console = Console()
    # Display an introduction to the lottery process
    console.print("\nEach lottery ball is selected by analyzing random values.\n", style="italic green")

    # Get the number of lottery balls to draw
    num_lotto_balls = int(questionary.text(
        "Amount of balls to draw? (default: 5)",
        validate=lambda val: val.isdigit() or "Please enter a valid integer.",
        default="5"
    ).ask())

    # Get the highest possible number in the lottery
    highest_number = int(questionary.text(
        "Amount of balls in the lottery? (default: 70)",
        validate=lambda val: val.isdigit() or "Please enter a valid integer.",
        default="70"
    ).ask())

    # Get the highest number for the extra draw
    highest_extra_ball = int(questionary.text(
        "Amount of balls in the extra draw? (default: 25)",
        validate=lambda val: val.isdigit() or "Please enter a valid integer.",
        default="25"
    ).ask())

    # Get the Z-score threshold for anomaly detection
    z_score_threshold = float(questionary.text(
        "Minimum Z-Score Threshold? (default: 4.0)",
        validate=lambda val: can_be_float(val) or "Please enter a valid value (1.0 - 5.0).",
        default="4.0"
    ).ask())

    numbers = set()
    megaball = set()

    # Show a progress bar during the number drawing process
    with Progress(TextColumn("[progress.description]{task.description}"), BarColumn(), transient=True) as progress:
        task = progress.add_task("Drawing numbers...", total=num_lotto_balls + 1)
        # Draw main lottery numbers
        while len(numbers) < num_lotto_balls:
            numbers = pull_number(numbers, highest_number, num_lotto_balls, z_score_threshold)
            progress.update(task, completed=len(numbers))
        # Draw the extra ball
        while len(megaball) < 1:
            megaball = pull_number(megaball, highest_extra_ball, 1, z_score_threshold)

    # Display the results
    console.print("\nLottery numbers:\n", style="bold green")
    lottery_balls = [Text(f" {n} ", style="bold black on white") for n in sorted(numbers)]
    bonus_ball = Text(f" {list(megaball)[0]} ", style="bold black on yellow")
    console.print(*lottery_balls, bonus_ball, sep=" ")

if __name__ == "__main__":
    main()
