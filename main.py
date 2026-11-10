from puzzle import Puzzle 

puzzle_a = Puzzle(
    "Number Challenge",
    "What number comes next? 2, 4, 8, 16, ?",
    "32",
    "Each number doubles",
    "Easy",
)

puzzle_b = Puzzle(
    "Word Challenge",
    "Decode the reversed word: NOHTYP",
    "PYTHON",
    "Read it from right to left",
    "Medium ",
)

puzzle_a.display_question()
guess = input("Your answer: ")
if puzzle_a.check_answer(guess):
    print("Correct!")
else: 
    print("Not quite.")
    puzzle_a.show_hint()

print()

puzzle_b.display_question()
guess = input("Your answer: ")
if puzzle_b.check_answer(guess):
    print("Correct!")
else: 
    print("Not quite.")
    puzzle_b.show_hint()
