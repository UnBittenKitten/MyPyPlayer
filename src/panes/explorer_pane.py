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
        self.is_sorting_by = "title" 
        
        self.song_list = song_list.SongList(self.db)
        self._build_ui()
        
    def _build_ui(self):
        self.title_label = ctk.CTkLabel(self.parent, text="File Explorer", font=("Arial", 16, "bold"))        
        self.title_label.pack(pady=(10, 5))
        
        self.path_label = ctk.CTkLabel(self.parent, text="No folder selected", font=("Arial", 12), text_color="gray")
        self.path_label.pack(pady=(0, 5))
        
        # HEADERS
        header_frame = ctk.CTkFrame(self.parent, fg_color="transparent", height=30)
        header_frame.pack(fill="x", padx=5, pady=(5, 0))
        
        def make_header(text, key, width=None, expand=False):
            lbl = ctk.CTkLabel(header_frame, text=text, anchor="w", font=("Arial", 12, "bold"), text_color="gray", cursor="hand2")
            if width: lbl.configure(width=width)
            if expand: lbl.pack(side="left", padx=(15, 5), fill="x", expand=True)
            else: lbl.pack(side="left", padx=5)
            lbl.bind("<Button-1>", lambda e: self.sort_by(key))
            return lbl

        make_header("Title", "title", expand=True)
        make_header("Artist", "artist", width=120)
        make_header("Album", "album", width=120)
        make_header("Time", "duration", width=60)
        
        ctk.CTkFrame(header_frame, width=75, height=1, fg_color="transparent").pack(side="right")

        self.scroll_list = ctk.CTkScrollableFrame(self.parent, fg_color="transparent")
        self.scroll_list.pack(fill="both", expand=True, padx=5, pady=5)

    def sort_by(self, key):
        if self.is_sorting_by == key:
            self.is_sorting_reverse = not self.is_sorting_reverse
        else:
            self.is_sorting_reverse = False
            self.is_sorting_by = key
        
        self.song_list.sortBy(key, reverse=self.is_sorting_reverse)
        self.refresh_list()

    def refresh_list(self):
        for widget in self.scroll_list.winfo_children():
            widget.destroy()
        is_folder = (self.current_folder is not None)
        for song_data in self.song_list.songlst:
            self._add_song_to_list(song_data, is_folder=is_folder)

    def load_folder(self, folder_path):
        self.current_folder = folder_path
        self.current_playlist = None 
        self.path_label.configure(text=folder_path)
        self.song_list.fillWithPaths(folder_path)
        self.refresh_list()

    def load_playlist(self, playlist_name):
        self.current_folder = None
        self.current_playlist = playlist_name 
        self.path_label.configure(text=f"Playlist: {playlist_name}")
        self.song_list.fillWithPlaylist(playlist_name)
        self.refresh_list()

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
        duration = str(song_data.get("duration", 0))

        # truncate long titles
        if len(title) > 30:
            title = title[:27] + "..."

        lbl_title = ctk.CTkLabel(row, text=title, anchor="w", cursor="hand2", font=("Arial", 13, "bold"))
        lbl_title.pack(side="left", padx=(10, 5), pady=5, fill="x", expand=True)
        
        ctk.CTkLabel(row, text=artist, anchor="w", width=120, text_color="#b0b0b0", font=("Arial", 12)).pack(side="left", padx=5, pady=5)
        ctk.CTkLabel(row, text=album, anchor="w", width=120, text_color="#b0b0b0", font=("Arial", 12)).pack(side="left", padx=5, pady=5)
        ctk.CTkLabel(row, text=duration, anchor="center", width=60, text_color="#b0b0b0", font=("Arial", 12)).pack(side="left", padx=5, pady=5)

        lbl_title.bind("<Button-1>", lambda e, p=file_path: self._on_song_click(p))
        
        ctk.CTkButton(row, text="Q+", width=30, height=25, command=lambda p=file_path: self._add_to_queue(p)).pack(side="right", padx=(2, 10))
        
        if is_folder:
            btn = ctk.CTkButton(row, text="P+", width=30, height=25, fg_color="#2C5F2D")
            btn.configure(command=lambda b=btn, r=row, p=file_path: self._show_playlist_selector(r, p, b))
            btn.pack(side="right", padx=2)
        else:
            ctk.CTkButton(row, text="X", width=30, height=25, fg_color="#C0392B", command=lambda p=file_path: self._remove_song_action(p)).pack(side="right", padx=(2, 10))

    def _show_playlist_selector(self, parent_row, song_path, original_btn):
        original_btn.pack_forget()
        playlists = self.db.get_playlists()
        if not playlists:
            original_btn.pack(side="right", padx=2)
            return
        playlist_names = [p[1] for p in playlists]
        
        cancel = ctk.CTkButton(parent_row, text="x", width=25, fg_color="#C0392B")
        cancel.pack(side="right", padx=2)
        confirm = ctk.CTkButton(parent_row, text="✓", width=25, fg_color="#27AE60")
        confirm.pack(side="right", padx=2)
        combo = ctk.CTkComboBox(parent_row, values=playlist_names, width=130)
        combo.pack(side="right", padx=2)

        def close():
            combo.destroy()
            confirm.destroy()
            cancel.destroy()
            original_btn.pack(side="right", padx=2)
        
        def save():
            if combo.get(): self.db.add_song_to_playlist(combo.get(), song_path)
            close()

        cancel.configure(command=close)
        confirm.configure(command=save)

    def _on_song_click(self, song_path):
        if self.on_song_click: self.on_song_click(song_path)

    def _add_to_queue(self, song_path):
        parent = self.parent
        while parent and not hasattr(parent, 'queue_component'): parent = parent.master
        if hasattr(parent, 'queue_component'): parent.queue_component.add_to_queue(song_path)

def add_to(parent_frame, data_manager, on_song_click=None):
    return ExplorerPane(parent_frame, data_manager, on_song_click)