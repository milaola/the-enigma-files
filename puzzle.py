class Puzzle:

    def __init__(self, title, question, answer, hint, difficulty):
        self.title= title
        self.question = question
        self.answer = answer
        self.hint = hint
        self.difficulty = difficulty

    def display_question(self):
        print(f"Title: {self.title}")
        print(f"Question: {self.question}")
        print(f"Difficulty: {self.difficulty}")

    def check_answer( self, guess):
        if guess.strip().lower() == self.answer.strip().lower():
              return True
        else:
              return False

    def __str__(self):
          return f"{self.title} [{self.difficulty}]"


puzzle1 = Puzzle (
      "The First code",
      "What number comes next: 2, 4, 8, 16?",
      "32",
      "Each number doubles",
      "Easy",
)

puzzle1.display_question()

guess = input ("Your answer: ")

if puzzle1.check_answer(guess):
          print("Correct!")

else: 
          print("Not quite. Hint:", puzzle1.hint)
          pass