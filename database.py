
import sqlite3
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path


# Keep the database in the same folder as this file.
DATABASE_NAME = Path(__file__).resolve().parent / "enigma.db"


@contextmanager
def get_connection():
    """Create, manage and safely close a database connection."""

    connection = None

    try:
        connection = sqlite3.connect(
            DATABASE_NAME,
            timeout=10
        )

        connection.execute("PRAGMA foreign_keys = ON")

        yield connection

        connection.commit()

    except sqlite3.Error as error:

        if connection is not None:
            connection.rollback()

        raise RuntimeError(
            f"Database operation failed: {error}"
        ) from error

    except Exception:

        if connection is not None:
            connection.rollback()

        raise

    finally:

        if connection is not None:
            connection.close()


def init_db():
    """Create the players and player_rooms tables if they do not exist."""

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

    if not name or not name.strip():
        raise ValueError("Player name cannot be empty.")

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

    if not isinstance(points, int) or points < 0:
        raise ValueError("Points must be a non-negative integer.")

    played_on = datetime.now().isoformat(timespec="seconds")

    with get_connection() as connection:

        cursor = connection.execute("""
            INSERT INTO player_rooms
                (player_id, room_number, completed)
            VALUES (?, ?, 1)
            ON CONFLICT(player_id, room_number)
            DO UPDATE SET completed = 1
            WHERE player_rooms.completed = 0
        """, (player_id, room_number))

        # If the room was already completed, do not award points again.
        if cursor.rowcount == 0:
            return False

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

    if room_number not in (1, 2, 3):
        raise ValueError("Invalid room number.")

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

    if room_number not in (1, 2, 3):
        raise ValueError("Invalid room number.")

    with get_connection() as connection:

        connection.execute("""
            INSERT INTO player_rooms
                (player_id, room_number, hints_used)
            VALUES (?, ?, 1)
            ON CONFLICT(player_id, room_number)
            DO UPDATE SET hints_used = hints_used + 1
        """, (player_id, room_number))


def get_player_progress(player_id):
    """Retrieve saved progress for all three rooms."""

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
    """Find a player using their ID and name."""

    with get_connection() as connection:

        cursor = connection.execute("""
            SELECT id, name
            FROM players
            WHERE id = ? AND LOWER(name) = LOWER(?)
        """, (player_id, name.strip()))

        return cursor.fetchone()


def get_leaderboard():
    """Retrieve the top ten players."""

    with get_connection() as connection:

        cursor = connection.execute("""
            SELECT name, score, rooms_completed, played_on
            FROM players
            ORDER BY score DESC, rooms_completed DESC
            LIMIT 10
        """)

        return cursor.fetchall()


def delete_player(player_id):
    """Delete a player and their associated room records."""

    with get_connection() as connection:

        cursor = connection.execute("""
            DELETE FROM players
            WHERE id = ?
        """, (player_id,))

        return cursor.rowcount > 0


# Initialise the database when this module is imported.
init_db()
