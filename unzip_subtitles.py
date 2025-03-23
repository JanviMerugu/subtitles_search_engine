import os
import zipfile

# Paths
ZIP_FOLDER = "../dataset/subtitle_zips"  # Folder where ZIP files are stored
EXTRACTED_FOLDER = "../dataset/subtitles"  # Where to store extracted subtitles

def unzip_subtitles():
    """Extracts subtitle files from all ZIP archives."""
    
    # Ensure output folder exists
    os.makedirs(EXTRACTED_FOLDER, exist_ok=True)

    # List all ZIP files
    zip_files = [f for f in os.listdir(ZIP_FOLDER) if f.endswith(".zip")]

    for zip_file in zip_files:
        zip_path = os.path.join(ZIP_FOLDER, zip_file)

        try:
            # Open ZIP file and extract subtitles
            with zipfile.ZipFile(zip_path, "r") as zip_ref:
                zip_ref.extractall(EXTRACTED_FOLDER)
                print(f"✅ Extracted: {zip_file}")

        except zipfile.BadZipFile:
            print(f"❌ Skipping corrupted ZIP: {zip_file}")

    print(f"\n✅ All subtitle files extracted to: {EXTRACTED_FOLDER}")

if __name__ == "__main__":
    unzip_subtitles()
