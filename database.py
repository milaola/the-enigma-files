
import sqlite3
from datetime import datetime

DATABASE_NAME = "enigma.db"


def get_connection():
    """Create and return a database connection."""
    connection = sqlite3.connect(DATABASE_NAME)
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def init_db():
    """Create the players and player_rooms tables."""
    with get_connection() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS players (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                score INTEGER DEFAULT 100,
                rooms_completed INTEGER DEFAULT 0,
                played_on TEXT
            )
        """)

        connection.execute("""
            CREATE TABLE IF NOT EXISTS player_rooms (
                player_id INTEGER NOT NULL,
                room_number INTEGER NOT NULL,
                completed INTEGER DEFAULT 0,
                attempts INTEGER DEFAULT 0,
                hints_used INTEGER DEFAULT 0,
                PRIMARY KEY (player_id, room_number),
                FOREIGN KEY (player_id)
                    REFERENCES players(id)
                    ON DELETE CASCADE
            )
        """)


def create_player(name):
    """Register a new player and return their database ID."""
    played_on = datetime.now().isoformat(timespec="seconds")

    with get_connection() as connection:
        cursor = connection.execute("""
            INSERT INTO players (name, played_on)
            VALUES (?, ?)
        """, (name.strip(), played_on))

        return cursor.lastrowid


def complete_room(player_id, room_number, points=100):
    """Complete a room and award points only once."""
    if room_number not in (1, 2, 3):
        raise ValueError("Room number must be 1, 2, or 3.")

    played_on = datetime.now().isoformat(timespec="seconds")

    with get_connection() as connection:
        cursor = connection.execute("""
            SELECT completed
            FROM player_rooms
            WHERE player_id = ? AND room_number = ?
        """, (player_id, room_number))

        existing_room = cursor.fetchone()

        if existing_room and existing_room[0]:
            return False

        connection.execute("""
            INSERT INTO player_rooms
                (player_id, room_number, completed)
            VALUES (?, ?, 1)
            ON CONFLICT(player_id, room_number)
            DO UPDATE SET completed = 1
        """, (player_id, room_number))

        connection.execute("""
            UPDATE players
            SET score = score + ?,
                rooms_completed = rooms_completed + 1,
                played_on = ?
            WHERE id = ?
        """, (points, played_on, player_id))

    return True


def record_attempt(player_id, room_number):
    """Record an unsuccessful attempt."""
    with get_connection() as connection:
        connection.execute("""
            INSERT INTO player_rooms
                (player_id, room_number, attempts)
            VALUES (?, ?, 1)
            ON CONFLICT(player_id, room_number)
            DO UPDATE SET attempts = attempts + 1
        """, (player_id, room_number))


def record_hint(player_id, room_number):
    """Record a requested hint."""
    with get_connection() as connection:
        connection.execute("""
            INSERT INTO player_rooms
                (player_id, room_number, hints_used)
            VALUES (?, ?, 1)
            ON CONFLICT(player_id, room_number)
            DO UPDATE SET hints_used = hints_used + 1
        """, (player_id, room_number))


def get_player_progress(player_id):
    """Return saved progress for all three rooms."""
    progress = {
        1: {"completed": False, "attempts": 0, "hints_used": 0},
        2: {"completed": False, "attempts": 0, "hints_used": 0},
        3: {"completed": False, "attempts": 0, "hints_used": 0}
    }

    with get_connection() as connection:
        cursor = connection.execute("""
            SELECT room_number, completed, attempts, hints_used
            FROM player_rooms
            WHERE player_id = ?
        """, (player_id,))

        for room_number, completed, attempts, hints_used in cursor.fetchall():
            if room_number in progress:
                progress[room_number] = {
                    "completed": bool(completed),
                    "attempts": attempts,
                    "hints_used": hints_used
                }

    return progress


def get_player_by_id(player_id, name):
    """Find an existing player using their ID and name."""
    with get_connection() as connection:
        cursor = connection.execute("""
            SELECT id, name
            FROM players
            WHERE id = ? AND LOWER(name) = LOWER(?)
        """, (player_id, name.strip()))

        return cursor.fetchone()


def get_leaderboard():
    """Return the top ten players."""
    with get_connection() as connection:
        cursor = connection.execute("""
            SELECT name, score, rooms_completed, played_on
            FROM players
            ORDER BY score DESC, rooms_completed DESC
            LIMIT 10
        """)

        return cursor.fetchall()


init_db()
