import pygame

class AudioBackend:
    def __init__(self):
        # Pre-initialize mixer with standard settings to avoid lag/silence
        # Frequency: 44100Hz, Size: -16 bit, Channels: 2 (Stereo), Buffer: 2048
        try:
            pygame.mixer.pre_init(44100, -16, 2, 2048)
            pygame.mixer.init()
            print("AudioBackend initialized successfully.")
        except pygame.error as e:
            print(f"Failed to initialize audio mixer: {e}")

        self.paused = False

    def load_music(self, file_path):
        try:
            pygame.mixer.music.load(file_path)
            print(f"Loaded: {file_path}")
        except pygame.error as e:
            print(f"Error loading music file: {e}")
            raise e # Re-raise to let the app know

    def play_music(self):
        try:
            pygame.mixer.music.play()
            self.paused = False
            print("Playback started.")
        except pygame.error as e:
            print(f"Error starting playback: {e}")

    def pause_music(self):
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.pause()
            self.paused = True

    def unpause_music(self):
        if self.paused:
            pygame.mixer.music.unpause()
            self.paused = False

    def stop_music(self):
        pygame.mixer.music.stop()
        self.paused = False

    def set_volume(self, volume):
        # Ensure volume is float 0.0 to 1.0
        try:
            pygame.mixer.music.set_volume(float(volume))
        except Exception:
            pass

    def is_playing(self):
        return pygame.mixer.music.get_busy()

    def is_idle(self):
        """
        Returns True ONLY if the player is stopped/empty.
        Returns False if playing OR paused.
        """
        return not pygame.mixer.music.get_busy() and not self.paused
    
    def process_events(self):
        """
        Call this periodically to keep pygame internals happy.
        Not strictly necessary for music only, but good practice.
        """
        pygame.event.pump()