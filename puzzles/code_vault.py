SEQUENCE = [3, 8, 15, 24, 35, "?"]

ANSWER = 48

SECURITY_CODE = "7319"

HINTS = [
    "Look at the difference between consecutive numbers.",
    "The differences are increasing by 2 each time.",
    "The differences are 5, 7, 9, 11. What comes after 35?"
]


def check_answer(user_answer):
    """Check whether the player's answer is correct."""

    try:
        return int(user_answer) == ANSWER
    except (ValueError, TypeError):
        return False
