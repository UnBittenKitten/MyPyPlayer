import customtkinter as ctk
import os
from classes.queue import Queue 

class SongQueuePane:
    def __init__(self, parent_frame, data_manager, audio_backend, on_play_start=None):
        self.parent = parent_frame
        self.db = data_manager
        self.audio_backend = audio_backend
        self.on_play_start = on_play_start # Callback
        self.queue_backend = Queue()
        self.queue_items = [] 
        self._build_ui()
        
    def _build_ui(self):
        title_frame = ctk.CTkFrame(self.parent, fg_color="transparent")
        title_frame.pack(fill="x", pady=(10, 5), padx=10)
        ctk.CTkLabel(title_frame, text="Song Queue", font=("Arial", 16, "bold")).pack(side="left")
        ctk.CTkButton(title_frame, text="Clear", width=60, height=25, command=self.clear_queue).pack(side="right")
        
        self.queue_list = ctk.CTkScrollableFrame(self.parent, fg_color="transparent")
        self.queue_list.pack(fill="both", expand=True, padx=5, pady=5)
        self.placeholder_label = ctk.CTkLabel(self.queue_list, text="Queue is empty\n\nAdd songs from the explorer",
                                            text_color="gray", justify="center")
        self.placeholder_label.pack(pady=40)

    def add_to_queue(self, song_path):
        # --- AUTO-PLAY CHECK ---
        if hasattr(self.audio_backend, 'is_idle') and self.audio_backend.is_idle():
            if self.on_play_start:
                print(f"Player idle. Playing: {song_path}")
                self.on_play_start(song_path)
                return 
        # -----------------------

        self.queue_backend.add(song_path)
        if self.placeholder_label.winfo_viewable():
            self.placeholder_label.pack_forget()
        
        queue_item = QueueItem(self.queue_list, song_path, len(self.queue_items), self)
        queue_item.pack(fill="x", pady=2)
        self.queue_items.append({'path': song_path, 'widget': queue_item})

    def pop_next_song(self):
        if self.queue_backend.length() == 0: return None
        
        next_song = self.queue_backend.front.value
        self.queue_backend.remove()

        self.queue_items[0]['widget'].destroy()
        self.queue_items.pop(0)
        for i, item in enumerate(self.queue_items):
            item['widget'].update_index(i)
        
        if not self.queue_items: self.placeholder_label.pack(pady=40)
        return next_song

    def clear_queue(self):
        self.queue_backend.clear()
        for item in self.queue_items:
            item['widget'].destroy()
        self.queue_items.clear()
        self.placeholder_label.pack(pady=40)

    def remove_from_queue(self, index):
        if 0 <= index < len(self.queue_items):
            self.queue_backend.remove_at_index(index)
            self.queue_items[index]['widget'].destroy()
            self.queue_items.pop(index)
            for i, item in enumerate(self.queue_items):
                item['widget'].update_index(i)
            if not self.queue_items:
                self.placeholder_label.pack(pady=40)

    def request_move(self, old_index, new_pos_str):
        try: new_pos = int(float(new_pos_str))
        except: return 
        max_len = self.queue_backend.length()
        if new_pos < 1: new_pos = 1 
        if new_pos > max_len: new_pos = max_len
        new_index = new_pos - 1 
        self.queue_backend.moveNodeKtoL(old_index, new_index)
        self._move_frontend_item(old_index, new_index)

    def _move_frontend_item(self, old, new):
        item = self.queue_items.pop(old)
        self.queue_items.insert(new, item)
        for child in self.queue_list.winfo_children():
            if child == self.placeholder_label: continue
            child.pack_forget()
        for i, item in enumerate(self.queue_items):
            item['widget'].update_index(i)
            item['widget'].pack(fill="x", pady = 2)

class QueueItem(ctk.CTkFrame):
    def __init__(self, parent, song_path, index, controller):
        super().__init__(parent, fg_color="#333333", height=40)
        self.song_path = song_path
        self.index = index
        self.controller = controller
        self._build_ui()

    def _build_ui(self):
        # Use self.index_label to reference later
        self.index_label = ctk.CTkLabel(self, text=f"{self.index + 1}.", width=30, font=("Arial", 11))
        self.index_label.pack(side="left", padx=(10, 5))
        
        file_name = os.path.basename(self.song_path)
        display_name = file_name[:27] + "..." if len(file_name) > 30 else file_name
        ctk.CTkLabel(self, text=display_name, anchor="w", font=("Arial", 11)).pack(side="left", padx=5, fill="x", expand=True)
        
        remove_btn = ctk.CTkButton(self, text="×", width=25, height=25, font=("Arial", 14), fg_color="#C9302C", 
                                 hover_color="#96221F", command=self._remove_self)
        remove_btn.pack(side="right", padx=5)

        self.bind("<Double-Button-1>", self._on_double_click)
        for widget in self.winfo_children():
            if widget != remove_btn: widget.bind("<Double-Button-1>", self._on_double_click)

    def _on_double_click(self, event):
        popup = ctk.CTkToplevel(self)
        popup.geometry(f"100x40+{self.winfo_rootx() + 20}+{self.winfo_rooty()}")
        popup.overrideredirect(True) 
        popup.attributes("-topmost", True)
        entry = ctk.CTkEntry(popup, width=80)
        entry.pack(padx=5, pady=5)
        entry.focus_set()

        def on_enter(event=None):
            new_pos = entry.get()
            popup.destroy()
            self.controller.request_move(self.index, new_pos)
        entry.bind("<Return>", on_enter)
        entry.bind("<Escape>", lambda e: popup.destroy())
        entry.bind("<FocusOut>", lambda e: popup.destroy())

    def update_index(self, new_index):
        self.index = new_index
        self.index_label.configure(text=f"{new_index + 1}.")

    def _remove_self(self):
        if self.controller:
            self.controller.remove_from_queue(self.index)

def add_to(parent_frame, data_manager, audio_backend, on_play_start=None):
    return SongQueuePane(parent_frame, data_manager, audio_backend, on_play_start)