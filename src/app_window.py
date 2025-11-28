import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="pygame")
import customtkinter as ctk
import tkinter as tk
import utils.resource_path as rp
import classes.audio_backend as ab
import classes.data_manager as dm

import panes.sources_pane as sources_pane
import panes.explorer_pane as explorer_pane
import panes.playlists_pane as playlists_pane
import panes.media_controls_pane as media_controls_pane
import panes.song_queue_pane as song_queue_pane

my_app_id = "MyPyPlayer.v0.0.1" 

try:
    from ctypes import windll
    windll.shell32.SetCurrentProcessExplicitAppUserModelID(my_app_id)
except ImportError: pass

class AppWindow(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.data_manager = dm.DataManager() 
        self.title("MyPyPlayer - Music Player")
        
        saved_geometry = self.data_manager.get_setting("window_geometry")
        if saved_geometry:
            try: self.geometry(saved_geometry)
            except: self.geometry("800x600")
        else: self.geometry("800x600")

        if self.data_manager.get_setting("window_state") == "zoomed":
            self.after(10, lambda: self.state("zoomed"))

        self.audio_backend = ab.AudioBackend() 
        self.audio_backend.set_volume(0.5)
        self.current_song_path = None
        self.current_metadata = None
        
        try:
            icon_path = rp.resource_path("assets/icon/icon.ico")
            self.iconbitmap(icon_path)
        except: pass
        
        pane_config = {"bd": 0, "sashwidth": 4, "bg": "#242424", "sashrelief": "flat"}

        self.main_pane = tk.PanedWindow(self, orient="horizontal", **pane_config)
        self.main_pane.pack(fill="both", expand=True)

        self.left_pane = tk.PanedWindow(self.main_pane, orient="vertical", **pane_config)
        self.main_pane.add(self.left_pane) 

        self.sec1 = ctk.CTkFrame(self.left_pane, fg_color="#2B2B2B", corner_radius=0)
        self.left_pane.add(self.sec1, stretch="always")
        try:
            self.playlists_component = playlists_pane.add_to(self.sec1, self.data_manager, on_playlist_click=lambda n: self.on_playlist_selected(n))
        except: pass

        self.sec2 = ctk.CTkFrame(self.left_pane, fg_color="#3A3A3A", corner_radius=0)
        self.left_pane.add(self.sec2, stretch="always")
        try:
            self.sources_component = sources_pane.add_to(self.sec2, self.data_manager, on_folder_click=lambda p: self.on_folder_selected(p))
        except: pass

        self.right_pane = tk.PanedWindow(self.main_pane, orient="vertical", **pane_config)
        self.main_pane.add(self.right_pane) 

        self.right_top_pane = tk.PanedWindow(self.right_pane, orient="horizontal", **pane_config)
        self.right_pane.add(self.right_top_pane, stretch="always")

        self.sec3 = ctk.CTkFrame(self.right_top_pane, fg_color="#494949", corner_radius=0)
        self.right_top_pane.add(self.sec3, stretch="always")
        try:
            self.explorer_component = explorer_pane.add_to(self.sec3, self.data_manager, on_song_click=lambda p: self.on_song_selected(p))
        except: pass

        self.sec4 = ctk.CTkFrame(self.right_top_pane, fg_color="#585858", corner_radius=0)
        self.right_top_pane.add(self.sec4, stretch="always")
        try:
            self.queue_component = song_queue_pane.add_to(self.sec4, self.data_manager, self.audio_backend, on_play_start=lambda p: self.on_song_selected(p))
        except: pass
        
        self.sec5 = ctk.CTkFrame(self.right_pane, fg_color="#676767", corner_radius=0)
        self.right_pane.add(self.sec5, stretch="always")
        
        try:
            # Pass EMPTY callbacks for play/pause to prevent double-trigger
            self.media_controls = media_controls_pane.MediaControlsPane(
                self.sec5,
                self.audio_backend,
                queue_component=getattr(self, 'queue_component', None),
                on_play=None, 
                on_pause=None,
                on_stop=self.on_stop_clicked,
                on_volume_change=self.on_volume_changed,
                on_previous=self.on_previous_clicked,
                on_next=self.on_next_clicked
            )
        except: pass

        self.bind_keys()
        self.check_for_song_end()
        self.after(200, self.load_layout)
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def check_for_song_end(self):
        if self.current_song_path and self.audio_backend.has_song_ended():
            if hasattr(self, 'queue_component'):
                next_song = self.queue_component.pop_next_song()
                if next_song: self.on_song_selected(next_song)
        self.after(1000, self.check_for_song_end)

    def on_previous_clicked(self):
        prev = self.audio_backend.play_previous()
        if prev:
            self.current_song_path = prev
            self.current_metadata = self.data_manager.get_song_metadata(prev)
            if hasattr(self, 'media_controls'):
                self.media_controls.update_song_info(self.current_metadata)
                self.media_controls.set_playing_state(True)

    def on_next_clicked(self):
        if hasattr(self, 'queue_component'):
            next_song = self.queue_component.pop_next_song()
            if next_song: self.on_song_selected(next_song)

    def on_folder_selected(self, folder_path):
        if hasattr(self, 'explorer_component'): self.explorer_component.load_folder(folder_path)

    def on_playlist_selected(self, playlist_name):
        if hasattr(self, 'explorer_component'): self.explorer_component.load_playlist(playlist_name)

    def on_song_selected(self, song_path):
        self.current_song_path = song_path
        try:
            self.audio_backend.load_music(song_path)
            self.audio_backend.play_music()
            self.current_metadata = self.data_manager.get_song_metadata(song_path)
            if hasattr(self, 'media_controls'):
                self.media_controls.update_song_info(self.current_metadata)
                self.media_controls.set_playing_state(True)
        except: pass

    def on_play_clicked(self): pass
    def on_pause_clicked(self): pass
    def on_stop_clicked(self): self.audio_backend.stop_music()
    def on_volume_changed(self, volume): self.audio_backend.set_volume(volume)

    def load_layout(self):
        self.update_idletasks()
        try:
            def apply_ratio(pane, db_key, is_vertical=False):
                ratio = self.data_manager.get_setting(db_key)
                if ratio:
                    val = int((pane.winfo_height() if is_vertical else pane.winfo_width()) * float(ratio))
                    if val > 0: pane.sash_place(0, 0, val) if is_vertical else pane.sash_place(0, val, 0)
            
            apply_ratio(self.main_pane, "ratio_main", False)
            apply_ratio(self.left_pane, "ratio_left", True)
            apply_ratio(self.right_pane, "ratio_right", True)
            apply_ratio(self.right_top_pane, "ratio_right_top", False)
        except: pass

    def bind_keys(self):
        self.bind('<space>', lambda e: self._trigger_play_pause())
        self.bind('<Right>', lambda e: self._trigger_forward())
        self.bind('<Left>', lambda e: self._trigger_backward())
        self.bind('<Control-Right>', lambda e: self._trigger_next())
        self.bind('<Control-Left>', lambda e: self._trigger_previous())
        self.bind('<KeyPress>', self._prevent_arrow_focus)

    def _prevent_arrow_focus(self, event):
        """Previene que las flechas cambien el foco entre widgets"""
        if event.keysym in ('Left', 'Right') and not event.state & 0x4:  # 0x4 es Ctrl
            return "break"

    def _trigger_play_pause(self):
        """Dispara el botón play/pause"""
        if hasattr(self, 'media_controls'):
            self.media_controls.on_play_pause()

    def _trigger_forward(self):
        """Dispara el botón adelantar 5 segundos"""
        if hasattr(self, 'media_controls'):
            self.media_controls.on_forward()

    def _trigger_backward(self):
        """Dispara el botón atrasar 5 segundos"""
        if hasattr(self, 'media_controls'):
            self.media_controls.on_backward()

    def _trigger_next(self):
        """Dispara el botón siguiente canción"""
        if hasattr(self, 'media_controls'):
            self.media_controls.on_next()

    def _trigger_previous(self):
        """Dispara el botón canción anterior"""
        if hasattr(self, 'media_controls'):
            self.media_controls.on_previous()

    def on_close(self):
        try:
            def get_ratio(pane, is_vertical=False):
                coords = pane.sash_coord(0)
                if is_vertical: return coords[1] / pane.winfo_height()
                else: return coords[0] / pane.winfo_width()

            self.data_manager.save_setting("ratio_main", get_ratio(self.main_pane, False))
            self.data_manager.save_setting("ratio_left", get_ratio(self.left_pane, True))
            self.data_manager.save_setting("ratio_right", get_ratio(self.right_pane, True))
            self.data_manager.save_setting("ratio_right_top", get_ratio(self.right_top_pane, False))
            
            self.data_manager.save_setting("window_state", self.state())
            if self.state() != "zoomed":
                self.data_manager.save_setting("window_geometry", self.geometry())
        except: pass
        self.destroy()