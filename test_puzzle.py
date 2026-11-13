
from manager import select_random_puzzle

for room_number in range(1, 4):

    puzzle = select_random_puzzle(room_number)

    print(f"\nROOM {room_number}")
    print("Question:", puzzle["question"])
    print("Hint:", puzzle["hint"])
