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

    