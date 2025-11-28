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
        self.current_song_path = None # Track current song
        self.history = [] # Stack for history

    def load_music(self, file_path, push_to_history=True):
        """
        Loads a music file.
        :param push_to_history: If True, saves the *previous* current song to the stack.
        """
        # Save current song to history before loading new one
        if push_to_history and self.current_song_path:
             self.history.append(self.current_song_path)

        try:
            pygame.mixer.music.load(file_path)
            self.current_song_path = file_path # Update current
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

    def play_previous(self):
        """
        Plays the last song in the history stack.
        Returns the path of the song being played, or None if history is empty.
        """
        if not self.history:
            print("No history to play previous song.")
            return None
        
        # Pop the last song
        prev_song = self.history.pop()
        print(f"Going back to: {prev_song}")
        
        # Load it without pushing the *current* song to history 
        # (Since we are going back, we typically discard the current "future" state)
        try:
            self.load_music(prev_song, push_to_history=False)
            self.play_music()
            return prev_song
        except Exception as e:
            print(f"Failed to play previous song: {e}")
            return None

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

    def has_song_ended(self):
        """
        Checks if the current song has ended.
        Note: This returns True if the player is idle (stopped).
        """
        return not pygame.mixer.music.get_busy() and not self.paused
    
    def get_song_length(self):
        """
        Returns the length of the currently loaded song in seconds.
        Note: This requires the song to be loaded.
        """
        try:
            return pygame.mixer.Sound(self.current_song_path).get_length()
        except Exception as e:
            print(f"Error getting song length: {e}")
            return 0
        
    def get_pos(self):
        """
        Returns the current playback position in milliseconds.
        Note: This returns -1 if no music is playing.
        """
        return pygame.mixer.music.get_pos()