ENCRYPTED_MESSAGE = "VHFUHW"

ANSWER = "SECRET"

SECURITY_PASSWORD = "NIGHTFALL"

HINTS = [
    "The message uses a Caesar cipher.",
    "Each letter has been shifted forward by 3 positions.",
    "To decrypt it, move every letter backwards by 3 positions."
]


def decrypt_message(message, shift=3):
    """Decrypt a message using a Caesar cipher."""

    decrypted = ""

    for letter in message:

        if letter.isalpha():

            position = ord(letter) - ord("A")

            new_position = (position - shift) % 26

            decrypted += chr(new_position + ord("A"))

        else:
            decrypted += letter

    return decrypted


def check_answer(user_answer):
    """Check whether the decoded message is correct."""

    return user_answer.strip().upper() == ANSWER
