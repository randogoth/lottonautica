from lyagushka import Lyagushka
from randonautentropy import rndo
import json
import questionary
from rich.console import Console
from rich.text import Text
from rich.progress import Progress, TextColumn, BarColumn
from pprint import pprint

def generate_random_data(size=1024, max_value=100):

    random_data = []
    max_value_bytes = (max_value.bit_length() + 7) // 8
    max_int_for_bytes = 2**(max_value_bytes * 8) - 1
    min_bytes_needed =  max_value_bytes * size
    mod_cutoff = max_int_for_bytes - (max_int_for_bytes % max_value) - 1

    # Populate the 'random_data' array
    while len(random_data) < size:
        hex_data = rndo.get(length=min_bytes_needed)
        hex_chunks = list((hex_data[0+i:2 * max_value_bytes+i] for i in range(0, len(hex_data), 2 * max_value_bytes)))
        for i in hex_chunks:
            num = int(i, 16)
            if num <= mod_cutoff and len(random_data) < size:
                random_data.append( num % (max_value + 1) )

    return random_data

def pull_number(numbers: set, top: int, amount: int):
    dataset = generate_random_data(top, top-1)
    dataset.sort()
    pprint(dataset)
    # calculate the anomalies in the data
    zhaba = Lyagushka(dataset)
    analysis_results = json.loads(zhaba.search(1.0, 3))
    pprint(analysis_results)
    pick = [obj for obj in analysis_results if obj['num_elements'] == max(obj['num_elements'] for obj in analysis_results)]
    for p in pick:
        if len(numbers) < amount:
            numbers.add(int(p['centroid'] + 1))
    return numbers

def main():

    console = Console()

    description = "\nEach lottery ball is selected by generating hundreds of random values within the provided range. The data is analyzed to identify the most frequently occurring number, which is then chosen as the lottery ball. This process repeats until all balls are drawn. The entire method is a one-dimensional analogy to how attractor points are calculated in Randonautica.\n"
    console.print(description, style="italic green")
    
    num_lotto_balls = questionary.text(
        "Amount of balls to draw? (default: 5)",
        validate=lambda val: val.isdigit() or "Please enter a valid integer.",
        default="5"
    ).ask()
    num_lotto_balls = int(num_lotto_balls)

    highest_number = questionary.text(
        "Amount of balls in the lottery? (default: 70)",
        validate=lambda val: val.isdigit() or "Please enter a valid integer.",
        default="70"
    ).ask()
    highest_number = int(highest_number)

    highest_extra_ball = questionary.text(
        "Amount of balls in the extra draw? (default: 25)",
        validate=lambda val: val.isdigit() or "Please enter a valid integer.",
        default="25"
    ).ask()
    highest_extra_ball = int(highest_extra_ball)

    numbers = set()

    # Animation before displaying the results
    with Progress(TextColumn("[progress.description]{task.description}"), BarColumn(), transient=True) as progress:
        task = progress.add_task("Drawing numbers...", total=num_lotto_balls+1)
        while len(numbers) < num_lotto_balls:
            numbers = pull_number(numbers, highest_number, num_lotto_balls)
            progress.update(task, completed=(len(numbers)/(num_lotto_balls+1)*num_lotto_balls+1))
        megaball = pull_number(set(), highest_extra_ball, 1)
        progress.stop()

    # Print the results as styled lottery balls
    console.print("\nLottery numbers:\n", style="bold green")
    lottery_balls = [Text(f" {n} ", style="bold black on white") for n in sorted(numbers)]
    bonus_ball = Text(f" {list(megaball)[0]} ", style="bold black on yellow")
    console.print(*lottery_balls, bonus_ball, sep=" ")

if __name__ == "__main__":
    main()
