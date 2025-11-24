import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="pygame")
import customtkinter as ctk
import tkinter as tk
import utils.resource_path as rp
import classes.audio_backend as ab
import classes.data_manager as dm

# Import the panes
import panes.sources_pane as sources_pane
import panes.explorer_pane as explorer_pane
import panes.playlists_pane as playlists_pane
import panes.media_controls_pane as media_controls_pane
import panes.song_queue_pane as song_queue_pane

my_app_id = "MyPyPlayer.v0.0.1" 

try:
    from ctypes import windll
    windll.shell32.SetCurrentProcessExplicitAppUserModelID(my_app_id)
except ImportError:
    pass

class AppWindow(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # --- Data Manager (Init First) ---
        self.data_manager = dm.DataManager() 

        # --- Configure Window ---
        self.title("MyPyPlayer - Music Player")
        
        # --- Restore Geometry & State ---
        saved_geometry = self.data_manager.get_setting("window_geometry")
        saved_state = self.data_manager.get_setting("window_state")

        if saved_geometry:
            try:
                self.geometry(saved_geometry)
            except Exception:
                self.geometry("800x600")
        else:
            self.geometry("800x600")

        if saved_state == "zoomed":
            self.after(10, lambda: self.state("zoomed"))

        # --- Audio Backend ---
        self.audio_backend = ab.AudioBackend() 
        self.audio_backend.set_volume(0.5)
        self.current_song_path = None
        self.current_metadata = None
        
        # --- Set the icon ---
        try:
            icon_path = rp.resource_path("assets/icon/icon.ico")
            self.iconbitmap(icon_path)
        except Exception:
            pass
        
        # Style configuration
        pane_config = {
            "bd": 0,
            "sashwidth": 4,
            "bg": "#242424", 
            "sashrelief": "flat"
        }

        # 1. MAIN HORIZONTAL SPLIT (Left vs Right)
        self.main_pane = tk.PanedWindow(self, orient="horizontal", **pane_config)
        self.main_pane.pack(fill="both", expand=True)

        # --- LEFT SIDE (Vertical Split) ---
        self.left_pane = tk.PanedWindow(self.main_pane, orient="vertical", **pane_config)
        self.main_pane.add(self.left_pane) 

        # Section 1: Left Top - PLAYLISTS
        self.sec1 = ctk.CTkFrame(self.left_pane, fg_color="#2B2B2B", corner_radius=0)
        self.left_pane.add(self.sec1, stretch="always")

        try:
            self.playlists_component = playlists_pane.add_to(
                self.sec1,
                self.data_manager,
                on_playlist_click=lambda path: print(f"Playlist clicked: {path}")
            )
        except Exception as e:
            print(f"Playlists pane load error: {e}")

        # Section 2: Left Bottom - SOURCES PANE
        self.sec2 = ctk.CTkFrame(self.left_pane, fg_color="#3A3A3A", corner_radius=0)
        self.left_pane.add(self.sec2, stretch="always")
        
        try:
            self.sources_component = sources_pane.add_to(
                self.sec2,
                self.data_manager,
                # CONECTAR CON AUDIO BACKEND
                on_folder_click=lambda path: self.on_folder_selected(path)
            )
        except Exception as e:
            print(f"Sources pane load error: {e}")

        # --- RIGHT SIDE (Vertical Split) ---
        self.right_pane = tk.PanedWindow(self.main_pane, orient="vertical", **pane_config)
        self.main_pane.add(self.right_pane) 

        # -- Right Top Area (Horizontal Split) --
        self.right_top_pane = tk.PanedWindow(self.right_pane, orient="horizontal", **pane_config)
        self.right_pane.add(self.right_top_pane, stretch="always")

        # Section 3: Right Top Left - EXPLORER PANE
        self.sec3 = ctk.CTkFrame(self.right_top_pane, fg_color="#494949", corner_radius=0)
        self.right_top_pane.add(self.sec3, stretch="always")
        
        try:
            self.explorer_component = explorer_pane.add_to(
                self.sec3,
                self.data_manager,
                on_song_click=lambda song_path: self.on_song_selected(song_path)
            )
        except Exception as e:
            print(f"Explorer pane load error: {e}")

        # Section 4: Right Top Right - SONG QUEUE
        self.sec4 = ctk.CTkFrame(self.right_top_pane, fg_color="#585858", corner_radius=0)
        self.right_top_pane.add(self.sec4, stretch="always")

        try:
            self.queue_component = song_queue_pane.add_to(
                self.sec4,
                self.data_manager,
                self.audio_backend
            )
        except Exception as e:
            print(f"Song queue pane load error: {e}")
        
        # Section 5: Right Bottom - MEDIA CONTROLS & METADATA
        self.sec5 = ctk.CTkFrame(self.right_pane, fg_color="#676767", corner_radius=0)
        self.right_pane.add(self.sec5, stretch="always")
        
        try:
            self.media_controls = media_controls_pane.add_to(
                self.sec5,
                self.audio_backend,
                on_play=self.on_play_clicked,
                on_pause=self.on_pause_clicked,
                on_stop=self.on_stop_clicked,
                on_volume_change=self.on_volume_changed,
                on_previous=self.on_previous_clicked,
                on_next=self.on_next_clicked
            )
        except Exception as e:
            print(f"Media controls load error: {e}")

        # --- Layout Restoration Logic ---
        self.after(200, self.load_layout)
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def on_previous_clicked(self):
        """Maneja el botón anterior"""
        # Aquí se implementará la lógica para ir a la canción anterior - WIP
        print("Previous song clicked")

    def on_next_clicked(self):
        """Maneja el botón siguiente"""
        # Aquí se implementará la lógica para ir a la siguiente canción - WIP
        print("Next song clicked")

    def on_folder_selected(self, folder_path):
        """Cuando se hace clic en una carpeta en Sources Pane"""
        print(f"Folder selected: {folder_path}")
        # Cargar archivos de audio de la carpeta en el Explorer Pane
        if hasattr(self, 'explorer_component'):
            self.explorer_component.load_folder(folder_path)

    def on_song_selected(self, song_path):
        """Cuando se hace clic en una canción en Explorer Pane"""
        print(f"Song selected: {song_path}")
        self.current_song_path = song_path
        
        try:
            self.audio_backend.load_music(song_path)
            self.audio_backend.play_music()
            
            self.current_metadata = self.data_manager.get_song_metadata(song_path)
            if hasattr(self, 'media_controls'):
                self.media_controls.update_song_info(self.current_metadata)
                self.media_controls.set_playing_state(True)
            
        except Exception as e:
            print(f"Error loading song: {e}")

    def update_now_playing_ui(self, metadata):
        """Actualiza la sección Now Playing con metadata"""
        self.song_title_label.configure(text=metadata["title"])
        self.artist_label.configure(text=metadata["artist"])
        self.duration_label.configure(text=metadata["duration"])
        
        if metadata["album_art"]:
            self.album_art_label.configure(image=metadata["album_art"], text="")
        else:
            self.album_art_label.configure(image=None, text="No Art")

    def on_play_clicked(self):
        """Callback para botón Play"""
        if self.current_song_path:
            self.audio_backend.unpause_music() # play_music reinicia el progreso de la canción

    def on_pause_clicked(self):
        """Callback para botón Pause"""
        self.audio_backend.pause_music()

    def on_stop_clicked(self):
        """Callback para botón Stop"""
        self.audio_backend.stop_music()

    def on_volume_changed(self, volume):
        """Callback para cambio de volumen"""
        self.audio_backend.set_volume(volume)

    def create_label(self, parent, text):
        """Helper to add a centered label"""
        label = ctk.CTkLabel(parent, text=text, font=("Arial", 20, "bold"))
        label.place(relx=0.5, rely=0.5, anchor="center")

    def load_layout(self):
        """Fetches ratios from DB and applies them."""
        try:
            self.update_idletasks()

            def apply_ratio(pane, db_key, is_vertical=False):
                ratio = self.data_manager.get_setting(db_key)
                if ratio is not None:
                    try:
                        ratio = float(ratio)
                        if is_vertical:
                            total_size = pane.winfo_height()
                            new_pos = int(total_size * ratio)
                            if new_pos > 0:
                                pane.sash_place(0, 0, new_pos)
                        else:
                            total_size = pane.winfo_width()
                            new_pos = int(total_size * ratio)
                            if new_pos > 0:
                                pane.sash_place(0, new_pos, 0)
                    except Exception as e:
                        print(f"Error applying ratio for {db_key}: {e}")

            apply_ratio(self.main_pane, "ratio_main", is_vertical=False)
            apply_ratio(self.left_pane, "ratio_left", is_vertical=True)
            apply_ratio(self.right_pane, "ratio_right", is_vertical=True)
            apply_ratio(self.right_top_pane, "ratio_right_top", is_vertical=False)

        except Exception as e:
            print(f"Error loading layout: {e}")

    def on_close(self):
        """Saves ratios (0.0 - 1.0) to DB and closes."""
        try:
            def get_ratio(pane, is_vertical=False):
                try:
                    coords = pane.sash_coord(0)
                    if is_vertical:
                        total = pane.winfo_height()
                        pos = coords[1]
                    else:
                        total = pane.winfo_width()
                        pos = coords[0]
                    
                    if total > 0:
                        return pos / total
                    return 0.5
                except Exception:
                    return 0.5

            self.data_manager.save_setting("ratio_main", get_ratio(self.main_pane, False))
            self.data_manager.save_setting("ratio_left", get_ratio(self.left_pane, True))
            self.data_manager.save_setting("ratio_right", get_ratio(self.right_pane, True))
            self.data_manager.save_setting("ratio_right_top", get_ratio(self.right_top_pane, False))
            
            current_state = self.state()
            self.data_manager.save_setting("window_state", current_state)

            if current_state != "zoomed":
                self.data_manager.save_setting("window_geometry", self.geometry())
            
        except Exception as e:
            print(f"Error saving layout: {e}")

        self.destroy()