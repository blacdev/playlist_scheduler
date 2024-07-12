from models.playlist_models import Playlist
from datetime import datetime
from database import get_db
from mutagen.mp3 import MP3
from mutagen.wave import WAVE
import os
from typing import List

def get_playlists_from_db() -> list:
    """
    Get playlists from database:
        This function fetches all playlists from the database and returns them.
    """
    with get_db() as db:
        playlists = db.query(Playlist).all()
    return playlists

def get_playlist_by_id_from_db(playlist_id: str) -> Playlist:
    """
    Get playlist by id from database:
        This function fetches a playlist by its id from the database and returns it.
    """
    with get_db() as db:
        playlist = db.query(Playlist).filter(Playlist.id == playlist_id).first()
    return playlist
def get_playlist_by_name_from_db(playlist_name: str) -> Playlist:
    """
    Get playlist by name from database:
        This function fetches a playlist by its name from the database and returns it.
    """
    with get_db() as db:
        playlist = db.query(Playlist).filter(Playlist.name == playlist_name).first()
    return playlist

def save_playlist_to_db(playlist: Playlist):
    """
    Save playlist to database:
        This function saves a playlist to the database.
    """
    with get_db() as db:
        db.add(playlist)
        db.commit()

def save_playlists_to_db(playlists: List[Playlist]):
    """
    Save playlists to database:
        This function saves a list of playlists to the database.
    """
    existing_playlists = []
    new_playlists = []

    # Check if the playlist already exists in the database
    for playlist in playlists:
        if get_playlist_by_name_from_db(playlist.name):
            existing_playlists.append(playlist)
        else:
            new_playlists.append(playlist)

    if not new_playlists:
        print("All playlists already exist in the database")
        return ""

    with get_db() as db:
        db.add_all(new_playlists)
        db.commit()


def get_playlist_duration(path: str) -> tuple:
    """
    Get playlist duration:
        This function returns the duration of a playlist in hours, minutes, and seconds.
        It takes a folder path as an argument, calculates the time duration of all songs in the folder,
        and returns the total duration.
    """
    file_types = [".mp3", ".wav"]
    playlist_duration_seconds = 0
    for root, _, files in os.walk(path):
        for file in files:
            if file.endswith(file_types[0]):
                audio = MP3(os.path.join(root, file))
                playlist_duration_seconds += audio.info.length
            elif file.endswith(file_types[1]):
                audio = WAVE(os.path.join(root, file))
                playlist_duration_seconds += audio.info.length

    hours = int(playlist_duration_seconds // 3600)
    minutes = int((playlist_duration_seconds % 3600) // 60)
    seconds = int(playlist_duration_seconds % 60)

    return hours, minutes, seconds

if __name__ == "__main__":


    playlist_duration = get_playlist_duration("/mnt/c/Users/Precision 5540/Music/2018 - 01 (6 hours)")
    print(playlist_duration)
    