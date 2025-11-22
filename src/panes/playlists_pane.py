import customtkinter as ctk
import os

class PlaylistsPane:
    """
    Controller class for the Playlists section.
    It builds the UI inside the given 'parent_frame' and handles interactions.
    """
    def __init__(self, parent_frame, data_manager, on_playlist_click=None):
        self.parent = parent_frame
        self.db = data_manager
        self.on_click_callback = on_playlist_click # Store the callback function
        self.active_playlist = None
        self.changing_name = False
        self.changing_name_to = None
        
        # Build the UI immediately
        self._build_ui()
        
        # Load initial data
        self._refresh_list()

    def _build_ui(self):

        # make the title label and button be on the same line,
        top_frame = ctk.CTkFrame(self.parent)
        top_frame.pack(fill="x", pady=(10, 5))

        # Title Label
        self.title_label = ctk.CTkLabel(top_frame, text="Playlists", font=("Arial", 16, "bold"))
        self.title_label.pack(side="left", pady=(10, 5), padx=10)
        # Add Button
        self.add_btn = ctk.CTkButton(top_frame, text="+", command=self._add_playlist_click)
        self.add_btn.pack(side="right", pady=(10, 5), padx=10)
        self.add_btn.configure(width=30, height=30)

        # make the button stick to the right of the frame
        # self.add_btn.pack(side="right", pady=(10, 5))

        # Scrollable List for the folders
        self.scroll_list = ctk.CTkScrollableFrame(self.parent, fg_color="transparent")
        self.scroll_list.pack(fill="both", expand=True, padx=5, pady=5)

    def _add_playlist_click(self):
        """Creates a new playlist with a default name."""
        # For simplicity, we add a playlist with a default name "New Playlist"
        default_name = "New Playlist"
        success = self.db.create_playlist(default_name)
        if success:
            self._refresh_list()
        else:
            print("Playlist already exists or invalid.")

    def _refresh_list(self):
        """Clear and rebuild the list of playlists."""
        # 1. Remove old widgets
        for widget in self.scroll_list.winfo_children():
            widget.destroy()

        # 2. Fetch from DB
        playlists = self.db.get_playlists()

        # 3. Create a row for each playlist
        for playlist in playlists:
            playlist_id, name = playlist
            row = ctk.CTkFrame(self.scroll_list, fg_color="#333333")
            row.pack(fill="x", pady=2)

            # Playlist Name Label
            label = ctk.CTkLabel(row, text=name, font=("Arial", 14), cursor="hand2")
            label.pack(side="left", padx=10, pady=5)
            label.bind("<Button-1>", lambda e, p=name: self._handle_label_click(p))

            # Remove Button
            remove_btn = ctk.CTkButton(row, text="x", command=lambda p=name: self._remove_source(p))
            remove_btn.pack(side="right", padx=10, pady=5)
            remove_btn.configure(width=30, height=30)

    def _handle_label_click(self, name):
        # if the playlist is already selected, temporarily set the label text to "",
        # then give the user a space to rename it
        if self.active_playlist == name and not self.changing_name:
            self.changing_name = True
            self.changing_name_to = name
            entry = ctk.CTkEntry(self.scroll_list, font=("Arial", 14))
            entry.insert(0, name)
            entry.pack(fill="x", pady=2)
            entry.focus_set()

            def on_enter(event):
                new_name = entry.get().strip()
                if new_name and new_name != name:
                    self._change_playlist_name(name, new_name)
                entry.destroy()
                self._refresh_list()
                self.changing_name = False
                self.changing_name_to = None

            entry.bind("<Return>", on_enter)
            return

        """Trigger the callback if it exists."""
        if self.on_click_callback:
            self.on_click_callback(name)

        self.active_playlist = name

    def _change_playlist_name(self, old_name, new_name):
        """Rename playlist in DB and refresh UI."""
        success = self.db.rename_playlist(old_name, new_name)
        if success:
            self._refresh_list()
        else:
            print("Failed to rename playlist (might already exist).")

    def _remove_source(self, name):
        """Remove source from DB and refresh UI."""
        self.db.remove_playlist(name)
        self._refresh_list()

        if self.active_playlist == name:
            self.active_playlist = None
        
        if self.changing_name_to == name:
            self.changing_name_to = None
            self.changing_name = False


def add_to(parent_frame, data_manager, on_playlist_click=None):
    """
    Helper function to initialize this component into a parent frame.
    """
    return PlaylistsPane(parent_frame, data_manager, on_playlist_click)