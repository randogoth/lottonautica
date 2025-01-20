import streamlit as st
import streamlit.components.v1 as components
from lyagushka import Lyagushka
from randonautentropy import rndo
import json
import time

# Validate Z-Score
def z_thresh(s):
    try:
        if float(s) >= 1.0 and float(s) <= 5.0:
            return True
        else:
            return False
    except ValueError:
        return False

# Generate random data with a specified size and maximum value
def generate_random_data(size=1024, max_value=100):
    random_data = []
    max_value_bytes = (max_value.bit_length() + 7) // 8
    max_int_for_bytes = 2**(max_value_bytes * 8) - 1
    mod_cutoff = max_int_for_bytes - (max_int_for_bytes % max_value) - 1

    while len(random_data) < size:
        hex_data = rndo.get(length=max_value_bytes * size)
        for i in (hex_data[j:j + 2 * max_value_bytes] for j in range(0, len(hex_data), 2 * max_value_bytes)):
            num = int(i, 16)
            if num <= mod_cutoff:
                random_data.append(num % (max_value + 1))
                if len(random_data) >= size:
                    break
    return random_data

# Analyze and select numbers based on Z-score
def pull_number(numbers: set, top: int, amount: int, z_score: float, progress_bar, task_name):
    dataset = generate_random_data(3000, 999)
    dataset.sort()
    zhaba = Lyagushka(dataset)
    analysis_results = json.loads(zhaba.search(4.0, 30))

    results = [obj for obj in analysis_results if obj['z_score'] is not None]
    max_z_score = max(obj['z_score'] for obj in results)

    total_tasks = amount - len(numbers)
    for idx, obj in enumerate(results):
        if obj['z_score'] == max_z_score and obj['z_score'] >= z_score:
            if len(numbers) < amount and (obj['centroid'] % 1 != 0.5):
                numbers.add(int((obj['centroid'] / 999) * top) + 1)
        # Update progress
        progress_bar.progress((len(numbers) / amount))
        time.sleep(0.05)  # Simulate some delay
        if len(numbers) >= amount:
            break
    return numbers

def generate_ball_html(numbers, bonus):
        balls_html = ""
        for num in numbers:
            balls_html += f"""
            <div class="ball white">{num}</div>
            """
        balls_html += f"""
        <div class="ball yellow">{bonus}</div>
        """
        return balls_html

description = "\nEach lottery ball is selected by generating hundreds of random values within the provided range. The data is analyzed to identify number clusters. The centroid values of the attractor clusters with a z-score above the set threshold are selected as lotto numbers. This process repeats until all balls are drawn. The entire method is a one-dimensional analogy to how attractor points are calculated in Randonautica.\n"

# Streamlit App
st.title("Lottonautica")
st.write(description)

# User Inputs
num_lotto_balls = st.number_input("Amount of balls to draw:", min_value=1, max_value=20, value=5)
highest_number = st.number_input("Amount of balls in the lottery:", min_value=1, max_value=100, value=70)
highest_extra_ball = st.number_input("Amount of balls in the extra draw:", min_value=1, max_value=50, value=25)
z_score_threshold = st.number_input("Minimum Z-Score Threshold:", min_value=1.0, max_value=5.0, value=3.0)

if st.button("Generate Lottery Numbers"):
    st.subheader("Generating Lottery Numbers...")
    numbers = set()
    megaball = set()

    # Progress bar for main numbers
    progress_main = st.progress(0)
    status_text = st.empty()

    st.text("Drawing main numbers...")
    while len(numbers) < num_lotto_balls:
        # Update numbers and progress
        numbers = pull_number(numbers, highest_number, num_lotto_balls, z_score_threshold, progress_main, "Main Numbers")
        progress_main.progress(len(numbers) / num_lotto_balls)

    # Progress bar for extra ball
    progress_extra = st.progress(0)
    st.text("Drawing the extra ball...")
    while len(megaball) < 1:
        # Update megaball and progress
        megaball = pull_number(megaball, highest_extra_ball, 1, z_score_threshold, progress_extra, "Bonus Ball")

    # Display Results
    st.subheader("Lottery Numbers")
    main_numbers = sorted(numbers)
    bonus_number = list(megaball)[0]

    # Full HTML with inline CSS
    custom_html = f"""
    <html>
    <head>
        <style>
            .container {{
                display: flex;
                justify-content: center;
                align-items: center;
                margin-top: 20px;
            }}
            .ball {{
                width: 50px;
                height: 50px;
                margin: 5px;
                border-radius: 50%;
                text-align: center;
                line-height: 50px;
                font-weight: bold;
                font-size: 18px;
                font-family: sans-serif;
                border: 2px solid black;
            }}
            .white {{
                background-color: white;
                color: black;
            }}
            .yellow {{
                background-color: yellow;
                color: black;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            {generate_ball_html(main_numbers, bonus_number)}
        </div>
    </body>
    </html>
    """

    components.html(custom_html, height=150)