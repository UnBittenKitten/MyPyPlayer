import customtkinter as ctk
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
        self.geometry("400x300") 

        # --- Set the icon for the title bar ---
        # Use the resource_path function to get the correct path
        icon_path = rp.resource_path("assets/icon/icon.ico")
        self.iconbitmap(icon_path)
        
        # --- Add widgets ---
        self.label = ctk.CTkLabel(self, text="Hello, CustomTkinter!")
        self.label.pack(pady=20, padx=20)

        # --- You can add more widgets or methods here ---