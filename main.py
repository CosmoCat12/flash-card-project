import pandas as pd
import random
from tkinter import *

# Constants
BACKGROUND_COLOR = "#B1DDC6"
CARD_FLIP_DELAY = 3000  # 3 seconds in milliseconds

# Load the data from CSV into a pandas DataFrame
data = pd.read_csv('./data/japanese_words_translations.csv', on_bad_lines='skip')  # Skip malformed rows

# Strip leading and trailing spaces from column names
data.columns = data.columns.str.strip()

# Convert to a list of dictionaries
words_list = data.to_dict(orient="records")

# File to store words the user wants to learn
WORDS_TO_LEARN_FILE = './data/words_to_learn.csv'

# Initialize window
window = Tk()
window.title("Flash Card App")
window.config(bg=BACKGROUND_COLOR, pady=50, padx=50)

# Load images
back = PhotoImage(file="./images/card_back.png")
front = PhotoImage(file="./images/card_front.png")
right = PhotoImage(file="./images/right.png")
wrong = PhotoImage(file="./images/wrong.png")

# Create canvas
canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR)
canvas.config(highlightthickness=0)
card_image = canvas.create_image(400, 263, image=front)
card_title = canvas.create_text(400, 150, text="", font=("Arial", 40, "italic"))
card_word = canvas.create_text(400, 263, text="", font=("Arial", 60, "bold"))
card_transcription = canvas.create_text(400, 350, text="", font=("Arial", 20), fill="gray")
canvas.grid(row=0, column=0, columnspan=2)

# Global variables
current_word_pair = {}
flip_timer = None

# Define function to display a new flashcard
def next_flashcard():
    global current_word_pair, flip_timer
    window.after_cancel(flip_timer)  # Cancel any existing flip timer

    # Pick a random word pair from the words list
    current_word_pair = random.choice(words_list)
    japanese_word = current_word_pair['Japanese word']
    transcription = current_word_pair['Transcription']

    # Update the text and image on the canvas for the front side
    canvas.itemconfig(card_image, image=front)
    canvas.itemconfig(card_title, text="Japanese", fill="black")
    canvas.itemconfig(card_word, text=japanese_word, fill="black")
    canvas.itemconfig(card_transcription, text=transcription, fill="gray")

    # Set a timer to flip the card after 3 seconds
    flip_timer = window.after(CARD_FLIP_DELAY, flip_card)

# Define function to flip the card and show the translation
def flip_card():
    russian_translation = current_word_pair['Translation']

    # Update the text and image on the canvas for the back side
    canvas.itemconfig(card_image, image=back)
    canvas.itemconfig(card_title, text="Russian", fill="white")
    canvas.itemconfig(card_word, text=russian_translation, fill="white")
    canvas.itemconfig(card_transcription, text="", fill="")

# Define function to handle "wrong" button press
def handle_wrong():
    # Append the current word to "words_to_learn.csv"
    df = pd.DataFrame([current_word_pair])
    try:
        df.to_csv(WORDS_TO_LEARN_FILE, mode='a', index=False, header=not pd.io.common.file_exists(WORDS_TO_LEARN_FILE))
    except Exception as e:
        print(f"Error writing to file: {e}")

    # Show the next flashcard
    next_flashcard()

# Define function to handle "right" button press
def handle_right():
    # Simply move to the next card
    next_flashcard()

# Create buttons for right and wrong answers
wrong_button = Button(image=wrong, highlightthickness=0, command=handle_wrong)
wrong_button.grid(row=1, column=0)

right_button = Button(image=right, highlightthickness=0, command=handle_right)
right_button.grid(row=1, column=1)

# Display the first flashcard when the app starts
flip_timer = window.after(0, next_flashcard)

# Run the window
window.mainloop()
