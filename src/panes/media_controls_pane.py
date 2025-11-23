import customtkinter as ctk

class MediaControlsPane:
    def __init__(self, parent_frame, audio_backend, on_play=None, on_pause=None, 
                 on_stop=None, on_volume_change=None):
        self.parent = parent_frame
        self.audio_backend = audio_backend
        self.on_play = on_play
        self.on_pause = on_pause
        self.on_stop = on_stop
        self.on_volume_change = on_volume_change
        self.current_metadata = None
        
        self._build_ui()
        
    def _build_ui(self):
        # Main frame
        main_frame = ctk.CTkFrame(self.parent, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # --- METADATA SECTION ---
        self.metadata_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        self.metadata_frame.pack(fill="x", pady=(0, 15))
        
        # Album Art
        self.album_art_label = ctk.CTkLabel(self.metadata_frame, text="No Art", 
                                          image=None, width=80, height=80)
        self.album_art_label.pack(side="left", padx=(0, 15))
        
        # Song Info Frame
        info_frame = ctk.CTkFrame(self.metadata_frame, fg_color="transparent")
        info_frame.pack(side="left", fill="both", expand=True)
        
        self.song_title_label = ctk.CTkLabel(info_frame, text="No song selected", 
                                           font=("Arial", 14, "bold"), anchor="w")
        self.song_title_label.pack(anchor="w", pady=(5, 0))
        
        self.artist_label = ctk.CTkLabel(info_frame, text="Unknown Artist", 
                                       font=("Arial", 12), anchor="w")
        self.artist_label.pack(anchor="w", pady=(2, 0))
        
        self.duration_label = ctk.CTkLabel(info_frame, text="00:00", 
                                         font=("Arial", 11), text_color="gray", anchor="w")
        self.duration_label.pack(anchor="w", pady=(2, 0))
        
        # --- CONTROLS SECTION ---
        controls_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        controls_frame.pack(fill="x", pady=10)
        
        # Control buttons
        self.play_btn = ctk.CTkButton(controls_frame, text="▶", width=50, height=40,
                                    font=("Arial", 16), command=self._on_play)
        self.play_btn.pack(side="left", padx=5)
        
        self.pause_btn = ctk.CTkButton(controls_frame, text="⏸", width=50, height=40,
                                     font=("Arial", 16), command=self._on_pause)
        self.pause_btn.pack(side="left", padx=5)
        
        self.stop_btn = ctk.CTkButton(controls_frame, text="⏹", width=50, height=40,
                                    font=("Arial", 16), command=self._on_stop)
        self.stop_btn.pack(side="left", padx=5)
        
        # Volume Section
        volume_frame = ctk.CTkFrame(controls_frame, fg_color="transparent")
        volume_frame.pack(side="right", padx=10)
        
        volume_label = ctk.CTkLabel(volume_frame, text="🔊", font=("Arial", 14))
        volume_label.pack(side="left", padx=(0, 5))
        
        self.volume_slider = ctk.CTkSlider(volume_frame, from_=0, to=1, width=120,
                                         command=self._on_volume_change)
        self.volume_slider.set(0.5)
        self.volume_slider.pack(side="left", fill="x", expand=True)

    def update_song_info(self, metadata):
        """Actualiza la metadata de la canción actual"""
        self.current_metadata = metadata
        
        self.song_title_label.configure(text=metadata["title"])
        self.artist_label.configure(text=metadata["artist"])
        self.duration_label.configure(text=metadata["duration"])
        
        if metadata["album_art"]:
            self.album_art_label.configure(image=metadata["album_art"], text="")
        else:
            self.album_art_label.configure(image=None, text="🎵")

    def _on_play(self):
        if self.on_play:
            self.on_play()

    def _on_pause(self):
        if self.on_pause:
            self.on_pause()

    def _on_stop(self):
        if self.on_stop:
            self.on_stop()

    def _on_volume_change(self, value):
        if self.on_volume_change:
            self.on_volume_change(float(value))

def add_to(parent_frame, audio_backend, on_play=None, on_pause=None, 
           on_stop=None, on_volume_change=None):
    return MediaControlsPane(parent_frame, audio_backend, on_play, on_pause, 
                           on_stop, on_volume_change)