import os
import json
from mutagen.easyid3 import EasyID3
from dotenv import load_dotenv


def validate_mp3(path: str, songs: list):
    """Validate MP3 files in the folder against JSON metadata."""

    # Pair song title and artists in a set of valid songs
    valid_metadata = { (song['name'], "/".join(song['artists'])) for song in songs }
        
    for file_name in os.listdir(path):
        if not file_name.lower().endswith(".mp3"): continue
        file_path = os.path.join(path, file_name)
        try:
            # Load metadata using mutagen
            audio = EasyID3(file_path)
            title: str = audio.get('title', [None])[0]
            artists: str = audio.get('artist', [None])[0]

            # Skip files with not enough metadata
            if not title or not artists:
                print(f"Skipping file with missing metadata: {file_name}")
                continue

            # Delete the files not found in the spotdl list
            if (title, artists) not in valid_metadata:
                print(f"Deleting unmatched file: {file_name} :: ${title} - {artists}")
                input("Press Enter to continue.")
                os.remove(file_path)
        except Exception as e:
            print(f"Error reading metadata from {file_name}: {e}")

def main():
    load_dotenv()

    # Get paths from environment variables
    spotdl_path = os.getenv("SPOTDL_FILE")
    folder_path = os.getenv("MUSIC_FOLDER")

    if not spotdl_path or not folder_path:
        print("Error: Please set JSON_FILE_PATH and FOLDER_PATH in the .env file.")
        return

    # Load songs from JSON
    with open(spotdl_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    songs = data.get("songs", [])
    
    validate_mp3(folder_path, songs)

if __name__ == "__main__":
    main()
