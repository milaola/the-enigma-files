# 🔐 The Enigma Files

**Think critically. Solve puzzles. Escape the unknown.**

## 1. Problem Statement

Many puzzle games offer limited variety and lack persistent player progression, making it difficult to maintain engagement and track individual performance over time.

The Enigma Files addresses this by providing an interactive escape-room experience where players solve challenges, earn points, track their progress and compete on a leaderboard.

## 2. Project Overview

The Enigma Files is a Python-based escape-room puzzle game built using Streamlit. Players navigate through different rooms, solve challenges, use hints when necessary and attempt to escape by completing each room.

The application uses SQLite to store player information and game progress, while JSON files store puzzle data.

The project applies object-oriented programming through a reusable Puzzle class, allowing individual puzzles to be created, displayed and checked using dedicated methods.

## 3. Features

- **Player Registration:** New players can create an account to begin playing.
- **Returning Player Login:** Existing players can log back in and restore their progress.
- **Multiple Puzzle Rooms:** Players progress through different rooms containing unique challenges.
- **Object-Oriented Puzzle System:** A reusable Puzzle class manages puzzle questions, answers, hints and difficulty levels.
- **JSON-Based Puzzle Storage:** Puzzle information is stored separately from the main game logic.
- **Hint System:** Players can request hints when they encounter difficult challenges.
- **Scoring System:** Players earn points as they successfully complete rooms.
- **Attempt Tracking:** The application records player attempts and hint usage.
- **Progress Persistence:** Player information and completed rooms are stored in an SQLite database.
- **Leaderboard:** Players can view rankings based on their performance.

## 4. Technologies Used

| Technology | Purpose                     |
| ---------- | --------------------------- |
| Python     | Core programming language   |
| Streamlit  | User interface              |
| SQLite     | Persistent database storage |
| JSON       | Puzzle data storage         |
| Git        | Version control             |
| GitHub     | Source code hosting         |

## 5. Project Structure

```text
the-enigma-files/
│
├── main.py                 # Main application entry point
├── app2.py                 # Additional application module
├── game.py                 # Core game logic
├── manager.py              # Game management
├── player.py               # Player functionality
├── puzzle.py               # Reusable Puzzle class
├── database.py             # SQLite database operations
├── leaderboard.py          # Leaderboard functionality
│
├── puzzles/
│   ├── __init__.py
│   ├── code_vault.py
│   ├── final_challenge.py
│   ├── hidden_message.py
│   ├── room1.json
│   ├── room2.json
│   └── room3.json
│
├── data/                    # Game data
├── assests/                 # Project assets
│
├── test_database.py         # Database tests
├── test_puzzle.py           # Puzzle tests
│
├── .env.example             # Environment configuration template
├── .gitignore               # Git exclusions
├── requirements.txt         # Project dependencies
└── README.md
```

## 6. Object-Oriented Programming

The project uses a reusable `Puzzle` class to organise individual puzzle challenges.

Each puzzle object contains:

- A title identifying the challenge.
- A question presented to the player.
- A correct answer used for validation.
- A hint to assist players.
- A difficulty level.

The class includes methods for displaying questions, checking submitted answers and showing hints.

Individual puzzle objects can be created from the same class, reducing code duplication and making it easier to introduce additional challenges.

## 7. Puzzle Management and Storage

Puzzle content is organised using Python modules and JSON files.

The `puzzles` directory contains individual Python modules for challenges such as Code Vault, Hidden Message and Final Challenge.

The JSON files (`room1.json`, `room2.json` and `room3.json`) store room-specific puzzle information.

Separating puzzle content from the main application makes the project easier to maintain and expand.

## 8. Database Management

The application uses SQLite to maintain player records and game progress between sessions.

The database supports:

- Creating player records.
- Retrieving player information.
- Updating scores and room progress.
- Recording attempts and hints.
- Deleting player records.
- Retrieving leaderboard information.

The database is initialised automatically by the application.

## 9. Installation and Setup

### Prerequisites

- Python 3.13
- Git
- pip

### Step 1: Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/the-enigma-files.git
```

### Step 2: Navigate into the project directory

```bash
cd the-enigma-files
```

### Step 3: Create a virtual environment

```bash
python -m venv venv
```

Activate the environment:

**Windows – Git Bash**

```bash
source venv/Scripts/activate
```

**Windows – Command Prompt**

```cmd
venv\Scripts\activate.bat
```

**macOS/Linux**

```bash
source venv/bin/activate
```

### Step 4: Install dependencies

```bash
pip install -r requirements.txt
```

### Step 5: Configure environment variables

If environment variables are required, create a local `.env` file using `.env.example` as a template.

Never commit your `.env` file or expose private credentials on GitHub.

### Step 6: Run the application

```bash
python -m streamlit run main.py
```

The application will open in your browser.

## 10. Testing

The project includes tests for important application components, including database functionality and puzzle logic.

Run the tests using:

```bash
python -m unittest discover -s . -p "test_*.py"
```

## 12. Future Improvements

Potential improvements include:

- Additional puzzle rooms and difficulty levels.
- More puzzle categories and mechanics.
- Enhanced player statistics.
- Improved user interface and accessibility.
- Expanded automated testing.

## 13. Author

**Project:** The Enigma Files

**Programming Language:** Python

**Interface:** Streamlit

**Database:** SQLite

**Version Control:** Git and GitHub

---

*Every room has a secret. Every puzzle has a solution. Can you escape?* 🔐

