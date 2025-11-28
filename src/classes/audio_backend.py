import pygame
import time

class AudioBackend:
    def __init__(self):
        pygame.mixer.init()
        self.current_file = None
        self.is_paused = False
        self._is_playing = False
        self._start_time = 0
        self._current_position = 0
        self._last_update_time = 0

    def load_music(self, file_path):
        """Loads a music file for playback."""
        self.current_file = file_path
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
            print(f"Error loading file: {e}")
            self.song_length = 0
        self._is_playing = False
        self._current_position = 0
        self._start_time = 0

    def play_music(self, start_pos=0):
        """Plays the currently loaded song from a specific position."""
        if self.current_file:
            try:
                pygame.mixer.music.play(start=start_pos)
                self.is_paused = False
                self._is_playing = True
                self._current_position = start_pos
                self._last_update_time = time.time()
            except Exception as e:
                print(f"Error playing: {e}")

    def pause_music(self):
        """Pauses playback."""
        pygame.mixer.music.pause()
        self.is_paused = True
        self._is_playing = False
        # Actualizar posición actual al pausar
        if self._is_playing:
            self._update_position()

    def unpause_music(self):
        """Unpauses playback."""
        pygame.mixer.music.unpause()
        self.is_paused = False
        self._is_playing = True
        self._last_update_time = time.time()

    def stop_music(self):
        pygame.mixer.music.stop()
        self._is_playing = False
        self._current_position = 0

    def set_volume(self, volume):
        # Ensure volume is float 0.0 to 1.0
        try:
            pygame.mixer.music.set_volume(float(volume))
        except Exception:
            pass

    def get_pos(self):
        """Returns current playback position in seconds."""
        if self._is_playing and not self.is_paused:
            self._update_position()
        return self._current_position

    def _update_position(self):
        """Actualiza la posición basada en el tiempo transcurrido."""
        if self._is_playing and not self.is_paused:
            current_time = time.time()
            elapsed = current_time - self._last_update_time
            self._current_position += elapsed
            self._last_update_time = current_time
            
            # No permitir que exceda la duración
            if self._current_position > self.song_length:
                self._current_position = self.song_length

    def set_pos(self, position):
        """Set playback position in seconds."""
        if self.current_file:
            was_playing = self._is_playing and not self.is_paused
            
            # Detener temporalmente
            if was_playing:
                pygame.mixer.music.pause()
            
            # Establecer nueva posición
            self._current_position = max(0, min(position, self.song_length))
            self._last_update_time = time.time()
            
            # Reanudar si estaba reproduciéndose
            if was_playing:
                pygame.mixer.music.play(start=self._current_position)
                self._is_playing = True
                self.is_paused = False
            else:
                # Si estaba pausado, solo actualizar la posición
                pygame.mixer.music.load(self.current_file)

    def is_playing(self):
        return self._is_playing and not self.is_paused

    def has_song_ended(self):
        """
        Checks if the current song has ended.
        Note: This returns True if the player is idle (stopped).
        """
        return not pygame.mixer.music.get_busy() and not self.paused
    
    def get_song_length(self):
        """Returns the total length of the current song in seconds."""
        return getattr(self, 'song_length', 0)
