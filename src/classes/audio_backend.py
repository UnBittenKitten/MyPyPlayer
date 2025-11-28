import pygame
import time
from classes.stack import Stack

class AudioBackend:
    def __init__(self):
        try:
            pygame.mixer.pre_init(44100, -16, 2, 2048)
            pygame.mixer.init()
        except:
            pygame.mixer.init()
            
        self.current_file = None
        self.is_paused = False
        self._is_playing = False
        self._current_position = 0
        self._last_update_time = 0

        # Use Custom Stack
        self.history_stack = Stack() 
        self.song_length = 0

    def load_music(self, file_path, push_history=True):
        """Loads a music file for playback."""
        # Save to history if requested and it's not a duplicate of top
        if push_history and self.current_file:
             if self.history_stack.is_empty() or self.history_stack.peek() != self.current_file:
                self.history_stack.push(self.current_file)

        self.current_file = file_path
        try:
            pygame.mixer.music.load(file_path)
            try:
                sound = pygame.mixer.Sound(file_path)
                self.song_length = sound.get_length()
            except:
                self.song_length = 0
        except pygame.error as e:
            print(f"Error loading file: {e}")
            self.song_length = 0
            raise e

        self._is_playing = False
        self.is_paused = False
        self._current_position = 0
        self._start_time = 0

    def play_music(self, start_pos=0):
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
        # FIX: Update position BEFORE setting paused flag
        if self._is_playing and not self.is_paused:
            self._update_position()
            pygame.mixer.music.pause()
            self.is_paused = True
            # Keep _is_playing True

    def unpause_music(self):
        if self.is_paused:
            pygame.mixer.music.unpause()
            self.is_paused = False
            self._is_playing = True
            self._last_update_time = time.time()
        elif self.current_file:
            self.play_music()

    def stop_music(self):
        pygame.mixer.music.stop()
        self._is_playing = False
        self.is_paused = False
        self._current_position = 0

    def set_volume(self, volume):
        try: pygame.mixer.music.set_volume(float(volume))
        except: pass

    def get_pos(self):
        if self._is_playing and not self.is_paused:
            self._update_position()
        return self._current_position

    def _update_position(self):
        if self._is_playing and not self.is_paused:
            current_time = time.time()
            elapsed = current_time - self._last_update_time
            self._current_position += elapsed
            self._last_update_time = current_time
            
            if self.song_length > 0 and self._current_position > self.song_length:
                self._current_position = self.song_length

    def set_pos(self, position):
        if self.current_file:
            was_playing = self._is_playing and not self.is_paused
            target_pos = max(0, min(position, self.song_length))
            self._current_position = target_pos
            self._last_update_time = time.time()
            
            if was_playing:
                pygame.mixer.music.play(start=self._current_position)
            else:
                pygame.mixer.music.play(start=self._current_position)
                pygame.mixer.music.pause()
                self.is_paused = True
                self._is_playing = True

    def is_playing(self):
        return self._is_playing and not self.is_paused
    
    def is_idle(self):
        return not pygame.mixer.music.get_busy() and not self.is_paused

    def has_song_ended(self):
        if self._is_playing and not self.is_paused:
            if not pygame.mixer.music.get_busy():
                return True
        return False

    def get_song_length(self):
        return getattr(self, 'song_length', 0)
        
    def play_previous(self):
        """Plays the previous song from the custom stack."""
        if self.history_stack.is_empty():
            return None
            
        prev_song = self.history_stack.pop()
        try:
            # Load without pushing to history (since we are going back)
            self.load_music(prev_song, push_history=False)
            self.play_music()
            return prev_song
        except: return None