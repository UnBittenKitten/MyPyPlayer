import pygame

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
            sound = pygame.mixer.Sound(file_path)
            self.song_length = sound.get_length()
        except pygame.error as e:
            print(f"Error loading file: {e}")
            self.song_length = 0

    def play_music(self, start_pos=0):
        """Plays the currently loaded song from a specific position."""
        if self.current_file:
            try:
                pygame.mixer.music.play(start=start_pos)
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

    def get_pos(self):
        """Returns current playback position in seconds."""
        return pygame.mixer.music.get_pos() / 1000.0 

    def set_pos(self, position): # MODIFICADO NOMBRE DE 'seek' A 'set_pos'
        """set to a specific position in the song (in seconds)."""
        if self.current_file:
            self.stop_music()
            self.play_music(start_pos=position)

    def get_song_length(self):
        """Returns the total length of the current song in seconds."""
        return self.song_length