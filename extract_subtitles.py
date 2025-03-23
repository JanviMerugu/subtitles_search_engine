import sqlite3
import pandas as pd
import json

# Path to the SQLite database
DB_PATH = r"C:\Users\91939\Downloads\eng_subtitles_database.db"

# Output CSV and JSON file paths
OUTPUT_CSV = "../dataset/extracted_subtitles.csv"
OUTPUT_JSON = "../dataset/subtitles.json"

def extract_subtitles():
    """Extracts subtitle text from the correct database table and saves to CSV and JSON."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 🔹 Change 'movie_subtitles' to your actual table name
    cursor.execute("SELECT video_id, subtitle_text FROM movie_subtitles")  

    rows = cursor.fetchall()

    if rows:
        df = pd.DataFrame(rows, columns=["video_id", "subtitle_text"])
        
        # Save as CSV
        df.to_csv(OUTPUT_CSV, index=False)
        print(f"✅ Extracted {len(rows)} subtitles to {OUTPUT_CSV}")

        # Save as JSON
        subtitles_list = df.to_dict(orient="records")
        with open(OUTPUT_JSON, "w", encoding="utf-8") as json_file:
            json.dump(subtitles_list, json_file, indent=4, ensure_ascii=False)

        print(f"✅ Extracted {len(rows)} subtitles to {OUTPUT_JSON}")

    else:
        print("⚠️ No subtitles found in the database.")

    conn.close()

if __name__ == "__main__":
    extract_subtitles()
