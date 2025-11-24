from .sort import merge_sort
from .data_manager import DataManager
import os

class SongList:
    def __init__(self, db:DataManager):
        self.db = db
        self.songlst = [] # store songs as their data, like {"path":..., "title":..., "artist":...}
        
    def fillWithPaths(self, path): # fills the songlst with songs from a given path:
        """Llena la lista de canciones con las rutas encontradas en el path dado"""
        # self.songlst = paths.copy()
        self.songlst.clear()
        for root, dirs, files in os.walk(path):
            for file in files:
                if file.lower().endswith(('.mp3', '.wav', '.flac', '.ogg', '.m4a', '.aac')):
                    full_path = os.path.join(root, file)
                    metadata = self.db.get_song_metadata(full_path)
                    song_data = {
                        "path": full_path,
                        "title": metadata.get("title", os.path.splitext(file)[0]),
                        "artist": metadata.get("artist", "Unknown Artist"),
                        "album": metadata.get("album", "Unknown Album"),
                        "duration": metadata.get("duration", 0)
                    }
                    self.songlst.append(song_data)
        self.songlst.sort(key=lambda x: x["title"]) # default sort by title
        
    def fillWithPlaylist(self, playlist_name:str):
        """Fills the song list with songs from a given playlist"""
        self.songlst.clear()
        paths = self.db.get_songs_in_playlist(playlist_name)
        for path in paths:
            metadata = self.db.get_song_metadata(path)
            song_data = {
                "path": path,
                "title": metadata.get("title", os.path.splitext(os.path.basename(path))[0]),
                "artist": metadata.get("artist", "Unknown Artist"),
                "album": metadata.get("album", "Unknown Album"),
                "duration": metadata.get("duration", 0)
            }
            self.songlst.append(song_data)
        self.songlst.sort(key=lambda x: x["title"]) # default sort by title
                    
    def sortBy(self, key:str, reverse:bool=False):
        """Sorts the song list by a given key (e.g., 'title', 'artist', 'duration')"""
        if key not in ["title", "artist", "album", "duration", "path"]:
            print(f"Invalid sort key: {key}. Must be one of 'title', 'artist', 'album', 'duration', 'path'.")
            return

        if key == "artist" or key == "album" or key == "duration":
            # Make sure to sort first by title to maintain order among same artists
            merge_sort(self.songlst, key=lambda x: x["title"], reverse=reverse)
        
        merge_sort(self.songlst, key=lambda x: x[key], reverse=reverse)
                    
                    
    def printSongs(self):
        for song in self.songlst:
            print(f"{song['artist']} - {song['title']} {{{song['album']}}} ({song['duration']}s) [{song['path']}]")
                



