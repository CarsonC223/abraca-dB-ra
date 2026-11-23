import sqlite3

# 1. Connect (automatically creates 'songs.db' if it doesn't exist)
conn = sqlite3.connect("songs.db")
cursor = conn.cursor()

# 2. Create a table (standard SQL)
cursor.execute("""
    CREATE TABLE IF NOT EXISTS songs (
        song_id INTEGER PRIMARY KEY,
        title TEXT,
        artist TEXT
    )
""")

# 3. Insert data safely using '?' placeholders
cursor.execute("INSERT INTO songs (title, artist) VALUES (?, ?)", ("Song B", "Artist 2"))
conn.commit()  # Save changes

# 4. Query the data
cursor.execute("SELECT * FROM songs")
print(cursor.fetchall())

conn.close()