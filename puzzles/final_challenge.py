ANSWER = "MORGAN"

SECURITY_PHRASE = "FREEDOM"

HINTS = [
    "The culprit is not Alex.",
    "Jordan was seen near the control room, but was not responsible.",
    "Only one suspect remains after eliminating Alex and Jordan."
]


def check_answer(user_answer):
    """Check whether the player's answer is correct."""

    return user_answer.strip().upper() == ANSWER
