import customtkinter as ctk

class SongQueuePane:
    def __init__(self, parent_frame, data_manager, audio_backend):
        self.parent = parent_frame
        self.db = data_manager
        self.audio_backend = audio_backend
        
        self._build_ui()
        
    def _build_ui(self):
        # Title Label
        title_label = ctk.CTkLabel(self.parent, text="Song Queue", 
                                 font=("Arial", 16, "bold"))
        title_label.pack(pady=(10, 5))
        
        # Queue list
        self.queue_list = ctk.CTkScrollableFrame(self.parent, fg_color="transparent")
        self.queue_list.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Placeholder
        placeholder = ctk.CTkLabel(self.queue_list, text="Queue is empty",
                                 text_color="gray")
        placeholder.pack(pady=20)

def add_to(parent_frame, data_manager, audio_backend):
    return SongQueuePane(parent_frame, data_manager, audio_backend)