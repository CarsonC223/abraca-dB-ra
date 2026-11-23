import sqlite3
from pathlib import Path
from FFT import fingerprint_song


def setup_database():
    conn = sqlite3.connect("shazam.db")
    conn.execute("PRAGMA foreign_keys = ON")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS songs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            filename TEXT NOT NULL UNIQUE
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS fingerprint_points (
            song_id INTEGER NOT NULL,
            time REAL NOT NULL,
            frequency REAL NOT NULL,
            FOREIGN KEY (song_id) REFERENCES songs(id)
        )
    """)

    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_points_song
        ON fingerprint_points(song_id)
    """)

    conn.commit()
    conn.close()


def store_song(filename):
    # Generate constellation points
    points = fingerprint_song(filename)

    # Get song title from filename
    title = Path(filename).stem

    conn = sqlite3.connect("shazam.db")
    conn.execute("PRAGMA foreign_keys = ON")

    try:
        with conn:
            cursor = conn.cursor()

            # Add song to songs table
            cursor.execute(
                "INSERT INTO songs (title, filename) VALUES (?, ?)",
                (title, filename)
            )

            # Get the ID of the newly added song
            song_id = cursor.lastrowid

            # Associate all points with this song
            data = [
                (song_id, time, frequency)
                for time, frequency in points
            ]

            # Insert all points at once
            cursor.executemany(
                """
                INSERT INTO fingerprint_points
                (song_id, time, frequency)
                VALUES (?, ?, ?)
                """,
                data
            )

        print(f"Stored {title}: {len(points)} points")

    finally:
        conn.close()