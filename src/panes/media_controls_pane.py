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
        
        self._build_ui()
        
    def _build_ui(self):
        # Main frame
        main_frame = ctk.CTkFrame(self.parent, fg_color="transparent")
        main_frame.pack(fill="x", pady=20)
        
        # Control buttons frame
        controls_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        controls_frame.pack(pady=10)
        
        # Play Button
        self.play_btn = ctk.CTkButton(controls_frame, text="▶", width=50, height=40,
                                    command=self._on_play)
        self.play_btn.pack(side="left", padx=5)
        
        # Pause Button
        self.pause_btn = ctk.CTkButton(controls_frame, text="⏸", width=50, height=40,
                                     command=self._on_pause)
        self.pause_btn.pack(side="left", padx=5)
        
        # Stop Button
        self.stop_btn = ctk.CTkButton(controls_frame, text="⏹", width=50, height=40,
                                    command=self._on_stop)
        self.stop_btn.pack(side="left", padx=5)
        
        # Volume Slider
        volume_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        volume_frame.pack(pady=10)
        
        volume_label = ctk.CTkLabel(volume_frame, text="Volume:")
        volume_label.pack(side="left", padx=5)
        
        self.volume_slider = ctk.CTkSlider(volume_frame, from_=0, to=1, 
                                         command=self._on_volume_change)
        self.volume_slider.set(0.5)  # Default volume
        self.volume_slider.pack(side="left", padx=5, fill="x", expand=True)

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