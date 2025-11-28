import customtkinter as ctk
import time

class MediaControlsPane:
    def __init__(self, parent_frame, audio_backend, queue_component=None, on_play=None, on_pause=None, 
                 on_stop=None, on_volume_change=None, on_previous=None, on_next=None):
        self.parent = parent_frame
        self.audio_backend = audio_backend
        self.queue_component = queue_component
        self.on_play = on_play
        self.on_pause = on_pause
        self.on_stop = on_stop
        self.on_volume_change = on_volume_change
        self.on_previous = on_previous
        self.on_next = on_next
        self.current_metadata = None
        self.is_playing = False
        self.is_finished = False
        self.current_time = 0
        self.total_time = 0
        
        self.PROGRESS_SLIDER_LENGTH = 400
        self.VOLUME_SLIDER_WIDTH = 80
        
        # ID del after para el progreso
        self.progress_after_id = None
        self.is_dragging = False # NEW
        
        self._build_ui()
        
    def _build_ui(self):
        # Main frame
        main_frame = ctk.CTkFrame(self.parent, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=20, pady=15)
        
        main_frame.grid_columnconfigure(0, weight=0)  # Album art (fixed)
        main_frame.grid_columnconfigure(1, weight=0)  # Título/Artista (fixed)
        main_frame.grid_columnconfigure(2, weight=1)  # Centro - Progress y controles (expande)
        main_frame.grid_columnconfigure(3, weight=0)  # Volumen (fixed)
        main_frame.grid_rowconfigure(0, weight=1)     # Fila única
        
        # --- COLUMNA 0: Album Art ---
        self.album_art_container = ctk.CTkFrame(main_frame, width=40, height=40, 
                                                fg_color="transparent", corner_radius=8)
        self.album_art_container.grid(row=0, column=0, padx=(0, 10), sticky="nsew")
        self.album_art_container.grid_propagate(False)
        
        self.album_art_label = ctk.CTkLabel(self.album_art_container, text="🎵", 
                                            image=None, width=40, height=40,
                                            font=("Arial", 16), corner_radius=6)
        self.album_art_label.pack(fill="both", expand=True)
        
        # --- COLUMNA 1: Título y Artista ---
        info_frame = ctk.CTkFrame(main_frame, fg_color="transparent", width=120)
        info_frame.grid(row=0, column=1, padx=(0, 20), sticky="nsew")
        info_frame.grid_propagate(False)
        
        # Centrar verticalmente título y artista
        info_frame.grid_rowconfigure(0, weight=1)
        info_frame.grid_rowconfigure(1, weight=1)
        info_frame.grid_rowconfigure(2, weight=1)
        info_frame.grid_columnconfigure(0, weight=1)
        
        # Espaciador superior
        ctk.CTkLabel(info_frame, text="", height=1).grid(row=0, column=0)
        
        # Título en primera línea
        self.song_title_label = ctk.CTkLabel(info_frame, text="No song selected", 
                                             font=("Arial", 14, "bold"), anchor="w")
        self.song_title_label.grid(row=1, column=0, sticky="w", pady=(0, 1))
        
        # Artista en segunda línea
        self.artist_label = ctk.CTkLabel(info_frame, text="Unknown Artist", 
                                         font=("Arial", 13.5), anchor="w", text_color="lightgray")
        self.artist_label.grid(row=2, column=0, sticky="w", pady=(1, 0))
        
        # Espaciador inferior
        ctk.CTkLabel(info_frame, text="", height=1).grid(row=3, column=0)
        
        # --- COLUMNA 2: Centro (Controles + Progress Bar) ---
        center_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        center_frame.grid(row=0, column=2, sticky="nsew")
        
        # Configurar grid del centro
        center_frame.grid_rowconfigure(0, weight=1)  # Espaciador superior
        center_frame.grid_rowconfigure(1, weight=0)  # Controles
        center_frame.grid_rowconfigure(2, weight=0)  # Progress bar
        center_frame.grid_rowconfigure(3, weight=1)  # Espaciador inferior
        center_frame.grid_columnconfigure(0, weight=1)
        
        # Espaciador superior
        ctk.CTkLabel(center_frame, text="", height=1).grid(row=0, column=0)
        
        # Fila 1: Controles de reproducción (centrados)
        controls_frame = ctk.CTkFrame(center_frame, fg_color="transparent")
        controls_frame.grid(row=1, column=0, sticky="n", pady=5)
        
        # Botón atrasar
        self.backward_btn = ctk.CTkLabel(controls_frame, text="↺", width=40, height=40,
                                        font=("Arial", 24),
                                        text_color="#CCCCCC",
                                        cursor="hand2")
        self.backward_btn.pack(side="left", padx=5)
        self.backward_btn.bind("<Button-1>", lambda e: self.on_backward())
        
        # Botón anterior
        self.previous_btn = ctk.CTkLabel(controls_frame, text="<<", width=40, height=40,
                                         font=("Arial", 18), 
                                         text_color="#CCCCCC",
                                         cursor="hand2")
        self.previous_btn.pack(side="left", padx=5)
        self.previous_btn.bind("<Button-1>", lambda e: self.on_previous())
        
        # Botón play/pause
        self.play_pause_btn = ctk.CTkButton(controls_frame, text="▶", width=50, height=50,
                                            font=("Arial", 22), command=self.on_play_pause,
                                            fg_color="#000000",
                                            hover_color="#333333",
                                            text_color="#FFFFFF",
                                            corner_radius=25)
        self.play_pause_btn.pack(side="left", padx=10)
        
        # Botón siguiente
        self.next_btn = ctk.CTkLabel(controls_frame, text=">>", width=40, height=40,
                                     font=("Arial", 18),
                                     text_color="#CCCCCC",
                                     cursor="hand2")
        self.next_btn.pack(side="left", padx=5)
        self.next_btn.bind("<Button-1>", lambda e: self.on_next())

        # Botón adelantar
        self.forward_btn = ctk.CTkLabel(controls_frame, text="↻", width=40, height=40,
                                        font=("Arial", 24),
                                        text_color="#CCCCCC",
                                        cursor="hand2")
        self.forward_btn.pack(side="left", padx=5)
        self.forward_btn.bind("<Button-1>", lambda e: self.on_forward())
        
        # Progress bar
        progress_frame = ctk.CTkFrame(center_frame, fg_color="transparent")
        progress_frame.grid(row=2, column=0, sticky="ew", pady=5)
        
        # Time labels and progress bar
        time_frame = ctk.CTkFrame(progress_frame, fg_color="transparent")
        time_frame.pack(fill="x", padx=20)
        
        self.current_time_label = ctk.CTkLabel(time_frame, text="0:00", 
                                             font=("Arial", 11), width=40)
        self.current_time_label.pack(side="left")
        
        # Progress bar
        self.progress_slider = ctk.CTkSlider(time_frame, from_=0, to=100, 
                                             width=self.PROGRESS_SLIDER_LENGTH, height=12, 
                                             progress_color="#1f6aa5",
                                             command=self._on_slider_move)
        self.progress_slider.set(0)
        self.progress_slider.pack(side="left", fill="x", expand=True, padx=10)
        
        # NEW: Bindings for drag events
        self.progress_slider.bind("<Button-1>", self._on_drag_start)
        self.progress_slider.bind("<ButtonRelease-1>", self._on_drag_end)
        
        self.total_time_label = ctk.CTkLabel(time_frame, text="0:00", 
                                             font=("Arial", 11), width=40)
        self.total_time_label.pack(side="right")
        
        # Espaciador inferior
        ctk.CTkLabel(center_frame, text="", height=1).grid(row=3, column=0)
        
        # --- COLUMNA 3: Volumen ---
        volume_frame = ctk.CTkFrame(main_frame, fg_color="transparent", width=100)
        volume_frame.grid(row=0, column=3, padx=(20, 0), sticky="nsew")
        volume_frame.grid_propagate(False)
        
        # Centrar verticalmente el volumen
        volume_frame.grid_rowconfigure(0, weight=1)
        volume_frame.grid_rowconfigure(1, weight=0)
        volume_frame.grid_rowconfigure(2, weight=1)
        volume_frame.grid_columnconfigure(0, weight=1)
        
        # Espaciador superior
        ctk.CTkLabel(volume_frame, text="", height=1).grid(row=0, column=0)
        
        # Control de volumen
        volume_control_frame = ctk.CTkFrame(volume_frame, fg_color="transparent")
        volume_control_frame.grid(row=1, column=0, sticky="")
        
        volume_label = ctk.CTkLabel(volume_control_frame, text="🔊", font=("Arial", 14))
        volume_label.pack(side="left", padx=(0, 8))
        
        self.volume_slider = ctk.CTkSlider(volume_control_frame, from_=0, to=1, 
                                           width=self.VOLUME_SLIDER_WIDTH, height=12,
                                           command=self._on_volume_change)
        self.volume_slider.set(0.5)
        self.volume_slider.pack(side="left")

    # --- NEW: SLIDER LOGIC ---
    def _on_drag_start(self, event):
        self.is_dragging = True

    def _on_slider_move(self, value):
        # Only update visual time while dragging
        if self.total_time > 0:
            temp_time = (value / 100.0) * self.total_time
            # Manually update label
            mins = int(temp_time // 60)
            secs = int(temp_time % 60)
            self.current_time_label.configure(text=f"{mins}:{secs:02d}")

    def _on_drag_end(self, event):
        self.is_dragging = False
        val = self.progress_slider.get()
        if self.total_time > 0:
            new_pos = (val / 100.0) * self.total_time
            self.audio_backend.set_pos(new_pos)
            self.current_time = new_pos
            self._update_time_display()
    # -------------------------

    def on_backward(self, event=None):
        """Atrasa la canción 5 segundos"""
        if self.audio_backend.current_file:
            current_pos = self.audio_backend.get_pos()
            new_pos = max(0, current_pos - 5)
            self.audio_backend.set_pos(new_pos)
            self.current_time = new_pos
            self._update_time_display()

    def on_forward(self, event=None):
        """Adelanta la canción 5 segundos"""
        if self.audio_backend.current_file:
            current_pos = self.audio_backend.get_pos()
            new_pos = min(self.total_time, current_pos + 5)
            self.audio_backend.set_pos(new_pos)
            self.current_time = new_pos
            self._update_time_display()

    def _update_time_display(self):
        """Actualiza la visualización del tiempo y progress bar"""
        # Actualizar label de tiempo actual
        mins = int(self.current_time // 60)
        secs = int(self.current_time % 60)
        self.current_time_label.configure(text=f"{mins}:{secs:02d}")
        
        # Actualizar progress bar
        if self.total_time > 0:
            progress = (self.current_time / self.total_time) * 100
            self.progress_slider.set(progress)
            
            time_remaining = self.total_time - self.current_time
            remaining_mins = int(time_remaining // 60)
            remaining_secs = int(time_remaining % 60)
            self.total_time_label.configure(text=f"-{remaining_mins}:{remaining_secs:02d}")


    def update_song_info(self, metadata):
        """Actualiza la metadata de la canción actual"""
        self.current_metadata = metadata
        
        self.song_title_label.configure(text=metadata["title"])
        self.artist_label.configure(text=metadata["artist"])
        
        self.total_time = self.audio_backend.get_song_length()
        
        if self.total_time <= 0:
            self.total_time = 0
            self.total_time_label.configure(text="-0:00")
        else:
            mins = int(self.total_time // 60)
            secs = int(self.total_time % 60)
            self.total_time_label.configure(text=f"-{mins}:{secs:02d}")
        
        self.current_time = 0
        self.current_time_label.configure(text="0:00")
        self.progress_slider.set(0)
        
        # Album art
        if metadata["album_art"]:
            self.album_art_label.configure(image=metadata["album_art"], text="")
        else:
            self.album_art_label.configure(image=None, text="🎵")
        
        self._start_progress_update()

    def _start_progress_update(self):
        """Inicia la actualización continua del progreso usando after()"""
        self._stop_progress_update()
        if self.is_playing and self.total_time > 0:
            self._update_progress()

    def _stop_progress_update(self):
        """Detiene la actualización del progreso"""
        if self.progress_after_id:
            self.parent.after_cancel(self.progress_after_id)
            self.progress_after_id = None

    def _update_progress(self):
        """Actualiza el progreso usando after() para llevar a cabo las iteraciones"""
        if self.is_playing and self.total_time > 0:
            # NEW: Don't update slider if dragging
            if not self.is_dragging:
                self.current_time = self.audio_backend.get_pos()
                
                if self.current_time >= self.total_time - 0.5:
                    self._on_song_end()
                    return
                    
                self._update_time_display()
            
            self.progress_after_id = self.parent.after(200, self._update_progress)

    def _on_song_end(self):
        """Maneja el final de la canción"""
        self.is_playing = False
        self.play_pause_btn.configure(text="▶")
        self._stop_progress_update()
        
        if self.on_next:
            self.on_next()

    def on_play_pause(self, event=None):
        """Maneja el botón play/pause"""
        if self.audio_backend.is_playing():
            # Pausar
            self.audio_backend.pause_music()
            self.set_playing_state(False)
            if self.on_pause:
                self.on_pause()
        else:
            # Reproducir
            if self.audio_backend.current_file:
                self.audio_backend.unpause_music()
                self.set_playing_state(True)
                if self.on_play:
                    self.on_play()

    def on_previous(self, event=None):
        if self.current_time > 5:
            self.audio_backend.set_pos(0)
            self.current_time = 0
            self._update_time_display()
        else:
            if self.on_previous:
                self.on_previous()

    def on_next(self, event=None):
        if self.on_next:
            self.on_next()

    def _on_volume_change(self, value):
        if self.on_volume_change:
            self.on_volume_change(float(value))

    def set_playing_state(self, playing):
        self.is_playing = playing
        if playing:
            self.play_pause_btn.configure(text="II")
            self._start_progress_update()
        else:
            self.play_pause_btn.configure(text="▶")
            self._stop_progress_update()

    def reset_progress(self):
        self.current_time = 0
        self.current_time_label.configure(text="0:00")
        self.progress_slider.set(0)

    def destroy(self):
        self._stop_progress_update()
        # if hasattr(super(), 'destroy'):
        #     super().destroy()

def add_to(parent_frame, audio_backend, queue_component=None, on_play=None, on_pause=None, 
           on_stop=None, on_volume_change=None, on_previous=None, on_next=None):
    return MediaControlsPane(parent_frame, audio_backend, queue_component, on_play, on_pause, 
                            on_stop, on_volume_change, on_previous, on_next)