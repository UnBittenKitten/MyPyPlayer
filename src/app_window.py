import customtkinter as ctk
import tkinter as tk
import utils.resource_path as rp

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

        # --- Configure Window ---
        self.title("Custom Tkinter App")
        WIDTH = 800
        HEIGHT = 600
        self.geometry(f"{WIDTH}x{HEIGHT}") 

        # --- Set the icon for the title bar ---
        # Use the resource_path function to get the correct path
        icon_path = rp.resource_path("assets/icon/icon.ico")
        self.iconbitmap(icon_path)
        
        # Style configuration for the draggable dividers (sashes)
        # bg="#242424" matches the default dark theme background
        # sashwidth=4 gives the user a small handle to grab
        pane_config = {
            "bd": 0,
            "sashwidth": 4,
            "bg": "#242424", 
            "sashrelief": "flat"
        }

        # 1. MAIN HORIZONTAL SPLIT (Left vs Right)
        # We pack this to fill the entire window
        self.main_pane = tk.PanedWindow(self, orient="horizontal", **pane_config)
        self.main_pane.pack(fill="both", expand=True)

        # --- LEFT SIDE (Vertical Split) ---
        self.left_pane = tk.PanedWindow(self.main_pane, orient="vertical", **pane_config)
        self.main_pane.add(self.left_pane) # Add left pane to main

        # Section 1: Left Top
        self.sec1 = ctk.CTkFrame(self.left_pane, fg_color="#2B2B2B", corner_radius=0)
        self.create_label(self.sec1, "1. Left Top")
        self.left_pane.add(self.sec1, stretch="always")

        # Section 2: Left Bottom
        self.sec2 = ctk.CTkFrame(self.left_pane, fg_color="#3A3A3A", corner_radius=0)
        self.create_label(self.sec2, "2. Left Bottom")
        self.left_pane.add(self.sec2, stretch="always")


        # --- RIGHT SIDE (Vertical Split) ---
        self.right_pane = tk.PanedWindow(self.main_pane, orient="vertical", **pane_config)
        self.main_pane.add(self.right_pane) # Add right pane to main

        # -- Right Top Area (Horizontal Split) --
        # This pane goes inside the top of the right pane
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
        
        # Change the default height of Section 5 (Right Bottom)
        self.right_pane.sash_place(0, 0, 333)  #Set initial sash position
        # Give it a min 
        self.right_pane.paneconfig(self.sec5, minsize=100)
        
        # Change the default width of the sash between Right Top Left and Right Top Right
        self.right_top_pane.sash_place(0, 300, 0)

    def create_label(self, parent, text):
        """Helper to add a centered label"""
        label = ctk.CTkLabel(parent, text=text, font=("Arial", 20, "bold"))
        label.place(relx=0.5, rely=0.5, anchor="center")