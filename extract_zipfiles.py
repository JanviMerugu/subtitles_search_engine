import sqlite3
import os

# Database path
DB_PATH = r"C:\Users\91939\Downloads\eng_subtitles_database.db"


# Folder to store extracted ZIP files
OUTPUT_FOLDER = "../dataset/subtitle_zips"

def extract_zipfiles():
    """Extracts ZIP files from the SQLite database and saves them to disk."""
    
    # Ensure the output folder exists
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    # Connect to SQLite database
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Fetch all ZIP files stored in the database
    cursor.execute("SELECT name, content FROM zipfiles")
    rows = cursor.fetchall()

    for i, (name, content) in enumerate(rows):
        try:
            # Ensure filename is valid
            filename = f"{name}.zip"

            # Full path to save the ZIP file
            filepath = os.path.join(OUTPUT_FOLDER, filename)

            # Check if the file already exists before writing
            if os.path.exists(filepath):
                print(f"File already exists, skipping: {filename}")
                continue

            # Write the ZIP content to the file
            with open(filepath, "wb") as f:
                f.write(content)

            print(f"Extracted: {filename}")

        except OSError as e:
            print(f"Error saving {filename}: {e}")

    # Close database connection
    conn.close()
    print(f"✅ All subtitle ZIP files saved to {OUTPUT_FOLDER}")

if __name__ == "__main__":
    extract_zipfiles()
