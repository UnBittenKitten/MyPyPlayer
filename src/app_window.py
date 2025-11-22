import warnings
# Filter out the specific warning about pkg_resources
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
    """
    Main application window class, inheriting from customtkinter.CTk.
    """
    def __init__(self, *args, **kwargs):
        # Call the parent class constructor
        super().__init__(*args, **kwargs)

        # --- Data Manager (Init First) ---
        # We initialize this FIRST so we can load geometry before showing the window
        self.data_manager = dm.DataManager() 

        # --- Configure Window ---
        self.title("Custom Tkinter App")
        
        # --- Restore Geometry & State ---
        # 1. Load saved settings
        saved_geometry = self.data_manager.get_setting("window_geometry")
        saved_state = self.data_manager.get_setting("window_state")

        # 2. Apply Geometry (Size + Position)
        if saved_geometry:
            try:
                self.geometry(saved_geometry)
            except Exception:
                self.geometry("800x600")
        else:
            self.geometry("800x600")

        # 3. Apply State (Maximized/Zoomed)
        # We use .after(10) because sometimes setting state immediately on init fails
        if saved_state == "zoomed":
            self.after(10, lambda: self.state("zoomed"))

        # --- Audio Backend ---
        self.audio_backend = ab.AudioBackend() 
        self.audio_backend.set_volume(0.5)
        try:
            self.audio_backend.load_music(rp.resource_path("assets/samplemusic/sample1.mp3"))
            self.audio_backend.play_music()
        except Exception as e:
            print(f"Audio init warning: {e}")
        
        # --- Debug / Initial Data Setup ---
        print("Current Sources in DB:", self.data_manager.get_sources())
        self.data_manager.create_playlist("My Favorites")
        self.data_manager.add_song_to_playlist("My Favorites", rp.resource_path("assets/samplemusic/sample1.mp3"))
        print("Songs in 'My Favorites':", self.data_manager.get_songs_in_playlist("My Favorites"))
        
        # --- Set the icon ---
        try:
            icon_path = rp.resource_path("assets/icon/icon.ico")
            self.iconbitmap(icon_path)
        except Exception:
            pass
        
        # Style configuration for the draggable dividers (sashes)
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

        # Section 1: Left Top
        self.sec1 = ctk.CTkFrame(self.left_pane, fg_color="#2B2B2B", corner_radius=0)
        self.create_label(self.sec1, "1. Left Top")
        self.left_pane.add(self.sec1, stretch="always")

        # Section 2: Left Bottom
        self.sec2 = ctk.CTkFrame(self.left_pane, fg_color="#3A3A3A", corner_radius=0)
        self.create_label(self.sec2, "2. Left Bottom")
        self.left_pane.add(self.sec2, stretch="always")
        
        try:
            self.sources_component = sources_pane.add_to(
                self.sec2,
                self.data_manager,
                on_folder_click=lambda path: print(f"Folder clicked: {path}")
            )
        except Exception as e:
            print(f"Sources pane load error: {e}")


        # --- RIGHT SIDE (Vertical Split) ---
        self.right_pane = tk.PanedWindow(self.main_pane, orient="vertical", **pane_config)
        self.main_pane.add(self.right_pane) 

        # -- Right Top Area (Horizontal Split) --
        self.right_top_pane = tk.PanedWindow(self.right_pane, orient="horizontal", **pane_config)
        self.right_pane.add(self.right_top_pane, stretch="always")

        # Section 3: Right Top Left
        self.sec3 = ctk.CTkFrame(self.right_top_pane, fg_color="#494949", corner_radius=0)
        self.create_label(self.sec3, "3. Right Top (L)")
        self.right_top_pane.add(self.sec3, stretch="always")

        # Section 4: Right Top Right
        self.sec4 = ctk.CTkFrame(self.right_top_pane, fg_color="#585858", corner_radius=0)
        self.create_label(self.sec4, "4. Right Top (R)")
        self.right_top_pane.add(self.sec4, stretch="always")

        # Section 5: Right Bottom
        self.sec5 = ctk.CTkFrame(self.right_pane, fg_color="#676767", corner_radius=0)
        self.create_label(self.sec5, "5. Right Bottom")
        self.right_pane.add(self.sec5, stretch="always")
        
        # --- Layout Restoration Logic ---
        self.after(200, self.load_layout)
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def create_label(self, parent, text):
        """Helper to add a centered label"""
        label = ctk.CTkLabel(parent, text=text, font=("Arial", 20, "bold"))
        label.place(relx=0.5, rely=0.5, anchor="center")

    def load_layout(self):
        """Fetches coords from DB and applies them to sashes."""
        try:
            def apply_sash(pane, db_key):
                coords = self.data_manager.get_setting(db_key)
                if coords and len(coords) == 2:
                    pane.sash_place(0, int(coords[0]), int(coords[1]))

            apply_sash(self.main_pane, "sash_main")
            apply_sash(self.left_pane, "sash_left")
            apply_sash(self.right_pane, "sash_right")
            apply_sash(self.right_top_pane, "sash_right_top")

        except Exception as e:
            print(f"Error loading layout: {e}")

    def on_close(self):
        """Saves current geometry and sashes to DB and closes."""
        try:
            # 1. Save Sash Positions
            self.data_manager.save_setting("sash_main", self.main_pane.sash_coord(0))
            self.data_manager.save_setting("sash_left", self.left_pane.sash_coord(0))
            self.data_manager.save_setting("sash_right", self.right_pane.sash_coord(0))
            self.data_manager.save_setting("sash_right_top", self.right_top_pane.sash_coord(0))
            
            # 2. Save Window Geometry & State
            current_state = self.state()
            self.data_manager.save_setting("window_state", current_state)

            # Only save specific dimensions if we are NOT maximized. 
            # If we save while maximized, the "restore" size is lost.
            if current_state != "zoomed":
                self.data_manager.save_setting("window_geometry", self.geometry())
            
        except Exception as e:
            print(f"Error saving layout: {e}")

        self.destroy()