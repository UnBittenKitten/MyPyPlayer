import customtkinter as ctk
import os
from classes import song_list

class ExplorerPane:
    def __init__(self, parent_frame, data_manager, on_song_click=None):
        self.parent = parent_frame
        self.db = data_manager
        self.on_song_click = on_song_click
        self.current_folder = None
        self.current_playlist = None 

        self.is_sorting_reverse = False
        self.is_sorting_by = "title"  # 'title', 'artist', 'album', 'duration'
        
        self.song_list = song_list.SongList(self.db)
        self._build_ui()
        
    def _build_ui(self):
        self.title_label = ctk.CTkLabel(self.parent, text="File Explorer", 
                                      font=("Arial", 16, "bold"))        

        self.title_label.pack(pady=(10, 5))
        
        self.path_label = ctk.CTkLabel(self.parent, text="No folder selected", 
                                     font=("Arial", 12), text_color="gray")
        self.path_label.pack(pady=(0, 5))
        
        header_frame = ctk.CTkFrame(self.parent, fg_color="transparent", height=30)
        header_frame.pack(fill="x", padx=5, pady=(5, 0))
        
        # --- TITLE HEADER (Clickable) ---
        self.header_title = ctk.CTkLabel(header_frame, text="Title", anchor="w", 
                                         font=("Arial", 12, "bold"), text_color="gray",
                                         cursor="hand2") # Hand cursor
        self.header_title.pack(side="left", padx=(15, 5), fill="x", expand=True)
        
        # Bind Click
        self.header_title.bind("<Button-1>", lambda e: self.title_lable_click())
        
        # Bind Hover Effects
        self.header_title.bind("<Enter>", lambda e: self.header_title.configure(text_color="#DCE4EE")) # Lighter on hover
        self.header_title.bind("<Leave>", lambda e: self.header_title.configure(text_color="gray")) # Back to gray
        
        # --- ARTIST HEADER (Clickable) ---
        self.header_artist = ctk.CTkLabel(header_frame, text="Artist", anchor="w", width=120, 
                                          font=("Arial", 12, "bold"), text_color="gray", 
                                          cursor="hand2")
        self.header_artist.pack(side="left", padx=5)
        
        # Bind Click
        self.header_artist.bind("<Button-1>", lambda e: self.artist_label_click())
        
        # Bind Hover Effects
        self.header_artist.bind("<Enter>", lambda e: self.header_artist.configure(text_color="#DCE4EE")) # Lighter on hover
        self.header_artist.bind("<Leave>", lambda e: self.header_artist.configure(text_color="gray")) # Back to gray
        
        # --- ALBUM HEADER (Clickable) ---
        self.header_album = ctk.CTkLabel(header_frame, text="Album", anchor="w", width=120, 
                                         font=("Arial", 12, "bold"), text_color="gray", 
                                         cursor="hand2")
        self.header_album.pack(side="left", padx=5)
        
        # Bind Click
        self.header_album.bind("<Button-1>", lambda e: self.album_label_click())
        
        # Bind Hover Effects
        self.header_album.bind("<Enter>", lambda e: self.header_album.configure(text_color="#DCE4EE")) # Lighter on hover
        self.header_album.bind("<Leave>", lambda e: self.header_album.configure(text_color="gray")) # Back to gray
        
        # --- DURATION HEADER (Clickable) ---
        self.header_duration = ctk.CTkLabel(header_frame, text="Time", anchor="center", width=60, 
                                            font=("Arial", 12, "bold"), text_color="gray", 
                                            cursor="hand2")
        self.header_duration.pack(side="left", padx=5)
        
        # Bind Click
        self.header_duration.bind("<Button-1>", lambda e: self.duration_label_click())
        
        # Bind Hover Effects
        self.header_duration.bind("<Enter>", lambda e: self.header_duration.configure(text_color="#DCE4EE")) # Lighter on hover
        self.header_duration.bind("<Leave>", lambda e: self.header_duration.configure(text_color="gray")) # Back to gray
        
        ctk.CTkFrame(header_frame, width=75, height=1, fg_color="transparent").pack(side="right")

        self.scroll_list = ctk.CTkScrollableFrame(self.parent, fg_color="transparent")
        self.scroll_list.pack(fill="both", expand=True, padx=5, pady=5)

    def title_lable_click(self):
        if self.is_sorting_by == "title":
            self.is_sorting_reverse = not self.is_sorting_reverse

        self.is_sorting_by = "title"

        self.song_list.sortBy("title", reverse=self.is_sorting_reverse)
        
        for widget in self.scroll_list.winfo_children():
            widget.destroy()
        
        for song_data in self.song_list.songlst:
            self._add_song_to_list(song_data, is_folder=(self.current_folder is not None))

    def artist_label_click(self):
        if self.is_sorting_by == "artist":
            self.is_sorting_reverse = not self.is_sorting_reverse

        self.is_sorting_by = "artist"

        self.song_list.sortBy("artist", reverse=self.is_sorting_reverse)
        
        for widget in self.scroll_list.winfo_children():
            widget.destroy()
        
        for song_data in self.song_list.songlst:
            self._add_song_to_list(song_data, is_folder=(self.current_folder is not None))

    def album_label_click(self):
        if self.is_sorting_by == "album":
            self.is_sorting_reverse = not self.is_sorting_reverse

        self.is_sorting_by = "album"

        self.song_list.sortBy("album", reverse=self.is_sorting_reverse)
        
        for widget in self.scroll_list.winfo_children():
            widget.destroy()
        
        for song_data in self.song_list.songlst:
            self._add_song_to_list(song_data, is_folder=(self.current_folder is not None))

    def duration_label_click(self):
        if self.is_sorting_by == "duration":
            self.is_sorting_reverse = not self.is_sorting_reverse

        self.is_sorting_by = "duration"

        self.song_list.sortBy("duration", reverse=self.is_sorting_reverse)
        
        for widget in self.scroll_list.winfo_children():
            widget.destroy()
        
        for song_data in self.song_list.songlst:
            self._add_song_to_list(song_data, is_folder=(self.current_folder is not None))

    def load_folder(self, folder_path):
        self.current_folder = folder_path
        self.current_playlist = None 
        self.path_label.configure(text=folder_path)
        
        for widget in self.scroll_list.winfo_children():
            widget.destroy()
        
        print(f"Loading folder: {folder_path}...")
        self.song_list.fillWithPaths(folder_path)
        
        for song_data in self.song_list.songlst:
            self._add_song_to_list(song_data)

    def load_playlist(self, playlist_name):
        self.current_folder = None
        self.current_playlist = playlist_name 
        self.path_label.configure(text=f"Playlist: {playlist_name}")
        
        for widget in self.scroll_list.winfo_children():
            widget.destroy()
        
        print(f"Loading playlist: {playlist_name}...")
        self.song_list.fillWithPlaylist(playlist_name)
        
        for song_data in self.song_list.songlst:
            # IMPORTANT: We pass is_folder=False here
            self._add_song_to_list(song_data, is_folder=False)

    def _remove_song_action(self, song_path):
        if self.current_playlist:
            self.db.remove_song_from_playlist(self.current_playlist, song_path)
            self.load_playlist(self.current_playlist)

    def _add_song_to_list(self, song_data, is_folder=True):
        row = ctk.CTkFrame(self.scroll_list, fg_color="#333333")
        row.pack(fill="x", pady=2)
        
        file_path = song_data["path"]
        
        title = song_data.get("title", os.path.basename(file_path))
        artist = song_data.get("artist", "Unknown")
        album = song_data.get("album", "Unknown")
        duration = song_data.get("duration", 0)
        duration_text = duration

        # truncate title if too long
        if len(title) > 30:
            title = title[:27] + "..."

        lbl_title = ctk.CTkLabel(row, text=title, anchor="w", cursor="hand2", font=("Arial", 13, "bold"))
        lbl_title.pack(side="left", padx=(10, 5), pady=5, fill="x", expand=True)
        
        ctk.CTkLabel(row, text=artist, anchor="w", width=120, text_color="#b0b0b0", font=("Arial", 12)).pack(side="left", padx=5, pady=5)
        ctk.CTkLabel(row, text=album, anchor="w", width=120, text_color="#b0b0b0", font=("Arial", 12)).pack(side="left", padx=5, pady=5)
        ctk.CTkLabel(row, text=duration_text, anchor="center", width=60, text_color="#b0b0b0", font=("Arial", 12)).pack(side="left", padx=5, pady=5)

        lbl_title.bind("<Button-1>", lambda e, p=file_path: self._on_song_click(p))
        lbl_title.bind("<Enter>", lambda e, l=lbl_title: l.configure(text_color="#3B8ED0"))
        lbl_title.bind("<Leave>", lambda e, l=lbl_title: l.configure(text_color=["#DCE4EE", "#DCE4EE"]))

        # 1. Queue Button
        add_queue_btn = ctk.CTkButton(row, text="Q+", width=30, height=25,
                            command=lambda p=file_path: self._add_to_queue(p))
        add_queue_btn.pack(side="right", padx=(2, 10))
        # --- BUTTON LOGIC (Mutually Exclusive) ---
        if is_folder:

            # 2. Add to Playlist Button
            add_playlist_btn = ctk.CTkButton(row, text="P+", width=30, height=25, fg_color="#2C5F2D", hover_color="#1E421F")
            add_playlist_btn.configure(command=lambda b=add_playlist_btn, r=row, p=file_path: self._show_playlist_selector(r, p, b))
            add_playlist_btn.pack(side="right", padx=2)

        else:
            # Playlist View: Show Remove (X) ONLY
            remove_btn = ctk.CTkButton(row, text="X", width=30, height=25, fg_color="#C0392B", hover_color="#962D22",
                                command=lambda p=file_path: self._remove_song_action(p))
            remove_btn.pack(side="right", padx=(2, 10))


    def _show_playlist_selector(self, parent_row, song_path, original_btn):
        original_btn.pack_forget()

        playlists = self.db.get_playlists()
        
        if not playlists:
            print("No playlists found. Create one first.")
            original_btn.pack(side="right", padx=2)
            return

        playlist_names = [p[1] for p in playlists]

        cancel_btn = ctk.CTkButton(parent_row, text="x", width=25, height=25, fg_color="#C0392B", hover_color="#962D22")
        cancel_btn.pack(side="right", padx=2)
        
        confirm_btn = ctk.CTkButton(parent_row, text="✓", width=25, height=25, fg_color="#27AE60", hover_color="#1E8449")
        confirm_btn.pack(side="right", padx=2)

        combo = ctk.CTkComboBox(parent_row, values=playlist_names, width=130, height=25)
        combo.pack(side="right", padx=2)

        def cancel_action():
            combo.destroy()
            confirm_btn.destroy()
            cancel_btn.destroy()
            original_btn.pack(side="right", padx=2)

        def confirm_action():
            selected = combo.get()
            if selected:
                self.db.add_song_to_playlist(selected, song_path)
                print(f"Added to playlist '{selected}': {os.path.basename(song_path)}")
            cancel_action()

        cancel_btn.configure(command=cancel_action)
        confirm_btn.configure(command=confirm_action)

    def _on_song_click(self, song_path):
        if self.on_song_click:
            self.on_song_click(song_path)

    def _add_to_queue(self, song_path):
        parent = self.parent
        while parent and not hasattr(parent, 'queue_component'):
            parent = parent.master
            
        if parent and hasattr(parent, 'queue_component'):
            parent.queue_component.add_to_queue(song_path)
            print(f"Added to queue: {song_path}")

def add_to(parent_frame, data_manager, on_song_click=None):
    return ExplorerPane(parent_frame, data_manager, on_song_click)