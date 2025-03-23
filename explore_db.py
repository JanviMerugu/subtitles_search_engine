import sqlite3

DB_PATH = r"C:\Users\91939\Downloads\eng_subtitles_database.db"


def explore_database():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # List all tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print("Tables in the database:", [t[0] for t in tables])

    # Preview first 5 rows from zipfiles table
    cursor.execute("SELECT * FROM zipfiles LIMIT 5;")
    rows = cursor.fetchall()

    for row in rows:
        print(f"\nRow {row[0]}:")
        print(f"Name: {row[1]}")
        print(f"Content Type: {type(row[2])}")  # Check if it's binary (BLOB)

    conn.close()

if __name__ == "__main__":
    explore_database()
