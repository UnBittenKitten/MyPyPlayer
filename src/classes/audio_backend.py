import pygame
from mutagen._file import File
from PIL import Image
import io
import customtkinter as ctk

class AudioBackend:
    def __init__(self):
        # Initialize pygame mixer
        pygame.mixer.init()
        self.current_file = None
        self.is_paused = False

    def load_music(self, file_path):
        """Loads a music file for playback."""
        self.current_file = file_path
        try:
            pygame.mixer.music.load(file_path)
        except pygame.error as e:
            print(f"Error loading file: {e}")

    def play_music(self):
        """Plays the currently loaded song."""
        if self.current_file:
            try:
                pygame.mixer.music.play()
                self.is_paused = False
            except Exception as e:
                print(f"Error playing: {e}")

    def pause_music(self):
        """Pauses playback."""
        pygame.mixer.music.pause()
        self.is_paused = True

    def unpause_music(self):
        """Unpauses playback."""
        pygame.mixer.music.unpause()
        self.is_paused = False

    def stop_music(self):
        """Stops playback completely."""
        pygame.mixer.music.stop()

    def set_volume(self, volume):
        """Sets volume from 0.0 to 1.0"""
        pygame.mixer.music.set_volume(volume)

    def get_song_metadata(self, file_path):
        """
        Extracts metadata using Mutagen.
        Returns a dictionary with title, artist, duration, and album_art (CTkImage).
        """
        data = {
            "title": "Unknown Title",
            "artist": "Unknown Artist",
            "duration": "00:00",
            "album_art": None 
        }

        try:
            audio = File(file_path)
            if audio is None:
                return data

            # --- 1. Get Text Tags (Artist/Title) ---
            # Mutagen tags vary by format (ID3 for mp3, Vorbis for flac)
            # This is a simplified generic lookup
            
            # EasyMP3 / ID3
            if 'TIT2' in audio.tags: data['title'] = str(audio.tags['TIT2'])
            if 'TPE1' in audio.tags: data['artist'] = str(audio.tags['TPE1'])
            
            # FLAC / OGG / MP4 (Common keys)
            if 'title' in audio.tags: data['title'] = str(audio.tags['title'][0])
            if 'artist' in audio.tags: data['artist'] = str(audio.tags['artist'][0])
            
            # Fallback: Use filename if title is missing
            if data['title'] == "Unknown Title":
                data['title'] = file_path.split("/")[-1]

            # --- 2. Get Duration ---
            if audio.info and audio.info.length:
                minutes = int(audio.info.length // 60)
                seconds = int(audio.info.length % 60)
                data['duration'] = f"{minutes:02}:{seconds:02}"

            # --- 3. Get Album Art ---
            # This is the tricky part. We look for APIC (MP3) or covr (MP4) frames.
            artwork_data = None
            
            # MP3 (ID3)
            if hasattr(audio, 'tags') and audio.tags:
                for tag in audio.tags.values():
                    if tag.FrameID == 'APIC':
                        artwork_data = tag.data
                        break
            
            # FLAC (Picture)
            if not artwork_data and hasattr(audio, 'pictures') and audio.pictures:
                artwork_data = audio.pictures[0].data

            # Create CTkImage if we found art
            if artwork_data:
                image = Image.open(io.BytesIO(artwork_data))
                # Resize for UI (e.g., 200x200)
                data['album_art'] = ctk.CTkImage(light_image=image, 
                                                 dark_image=image, 
                                                 size=(200, 200))
            
        except Exception as e:
            print(f"Error reading metadata: {e}")

        return data