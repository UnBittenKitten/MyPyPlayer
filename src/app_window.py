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
        self.data_manager = dm.DataManager() 

        # --- Configure Window ---
        self.title("Custom Tkinter App")
        
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
        try:
            self.audio_backend.load_music(rp.resource_path("assets/samplemusic/sample1.mp3"))
            self.audio_backend.play_music()
        except Exception as e:
            print(f"Audio init warning: {e}")
        
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
        # self.create_label(self.sec1, "1. Left Top")
        self.left_pane.add(self.sec1, stretch="always")

        try:
            self.playlists_component = playlists_pane.add_to(
                self.sec1,
                self.data_manager,
                on_playlist_click=lambda path: print(f"Playlist clicked: {path}")
            )
        except Exception as e:
            print(f"Playlists pane load error: {e}")

        # Section 2: Left Bottom
        self.sec2 = ctk.CTkFrame(self.left_pane, fg_color="#3A3A3A", corner_radius=0)
        # self.create_label(self.sec2, "2. Left Bottom")
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
        """Fetches ratios from DB and applies them."""
        try:
            # Force an update so we have real dimensions to work with
            self.update_idletasks()

            def apply_ratio(pane, db_key, is_vertical=False):
                ratio = self.data_manager.get_setting(db_key)
                if ratio is not None:
                    try:
                        ratio = float(ratio)
                        if is_vertical:
                            total_size = pane.winfo_height()
                            new_pos = int(total_size * ratio)
                            # Avoid setting sash to 0 or negative
                            if new_pos > 0:
                                pane.sash_place(0, 0, new_pos)
                        else:
                            total_size = pane.winfo_width()
                            new_pos = int(total_size * ratio)
                            if new_pos > 0:
                                pane.sash_place(0, new_pos, 0)
                    except Exception as e:
                        print(f"Error applying ratio for {db_key}: {e}")

            # Apply ratios
            apply_ratio(self.main_pane, "ratio_main", is_vertical=False)
            apply_ratio(self.left_pane, "ratio_left", is_vertical=True)
            apply_ratio(self.right_pane, "ratio_right", is_vertical=True)
            apply_ratio(self.right_top_pane, "ratio_right_top", is_vertical=False)

        except Exception as e:
            print(f"Error loading layout: {e}")

    def on_close(self):
        """Saves ratios (0.0 - 1.0) to DB and closes."""
        try:
            # Helper to calculate ratio
            def get_ratio(pane, is_vertical=False):
                try:
                    # sash_coord returns (x, y)
                    coords = pane.sash_coord(0)
                    if is_vertical:
                        # For vertical, we care about Y position relative to Height
                        total = pane.winfo_height()
                        pos = coords[1]
                    else:
                        # For horizontal, we care about X position relative to Width
                        total = pane.winfo_width()
                        pos = coords[0]
                    
                    if total > 0:
                        return pos / total
                    return 0.5
                except Exception:
                    return 0.5

            # 1. Save Ratios
            self.data_manager.save_setting("ratio_main", get_ratio(self.main_pane, False))
            self.data_manager.save_setting("ratio_left", get_ratio(self.left_pane, True))
            self.data_manager.save_setting("ratio_right", get_ratio(self.right_pane, True))
            self.data_manager.save_setting("ratio_right_top", get_ratio(self.right_top_pane, False))
            
            # 2. Save Window Geometry & State
            current_state = self.state()
            self.data_manager.save_setting("window_state", current_state)

            if current_state != "zoomed":
                self.data_manager.save_setting("window_geometry", self.geometry())
            
        except Exception as e:
            print(f"Error saving layout: {e}")

        self.destroy()