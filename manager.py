import json
import random
from pathlib import Path


PUZZLE_FOLDER = Path(__file__).parent / "puzzles"


def load_puzzles(room_number):
    """Load all puzzles for a specific room."""

    file_path = PUZZLE_FOLDER / f"room{room_number}.json"

    with open(file_path, "r", encoding="utf-8") as file:
        puzzles = json.load(file)

    return puzzles


def select_random_puzzle(room_number):
    """Select one random puzzle from a room."""

    puzzles = load_puzzles(room_number)

    return random.choice(puzzles)


def check_answer(user_answer, correct_answer):
    """Compare the player's answer with the correct answer."""

    return user_answer.strip().upper() == correct_answer.strip().upper()
