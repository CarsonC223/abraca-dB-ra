import sqlite3

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