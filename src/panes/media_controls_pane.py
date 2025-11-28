import customtkinter as ctk
import pygame
import os

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
        self.current_time = 0
        self.total_time = 0
        self.is_seeking = False  # Para evitar actualizaciones durante el seek
        
        self.PROGRESS_SLIDER_LENGTH = 400
        self.VOLUME_SLIDER_WIDTH = 80
        
        # Timer para actualizar el progreso
        self.progress_timer = None
        
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
        self.album_art_container = ctk.CTkFrame(main_frame, width=80, height=80, 
                                               fg_color="transparent", corner_radius=8)
        self.album_art_container.grid(row=0, column=0, padx=(0, 10), sticky="nsew")
        self.album_art_container.grid_propagate(False)
        
        self.album_art_label = ctk.CTkLabel(self.album_art_container, text="🎵", 
                                          image=None, width=80, height=80,
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
        self.song_title_label.grid(row=1, column=0, sticky="w", pady=(0, 2))
        
        # Artista en segunda línea
        self.artist_label = ctk.CTkLabel(info_frame, text="Unknown Artist", 
                                       font=("Arial", 12), anchor="w", text_color="gray")
        self.artist_label.grid(row=2, column=0, sticky="w", pady=(2, 0))
        
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
        
        self.previous_btn = ctk.CTkButton(controls_frame, text="⏮", width=40, height=40,
                                        font=("Arial", 16), command=self._on_previous,
                                        fg_color="transparent", hover_color="#2B2B2B")
        self.previous_btn.pack(side="left", padx=5)
        
        self.play_pause_btn = ctk.CTkButton(controls_frame, text="▶", width=50, height=50,
                                          font=("Arial", 18), command=self._on_play_pause,
                                          fg_color="#1f6aa5", hover_color="#1a5a8a")
        self.play_pause_btn.pack(side="left", padx=10)
        
        self.next_btn = ctk.CTkButton(controls_frame, text="⏭", width=40, height=40,
                                    font=("Arial", 16), command=self._on_next,
                                    fg_color="transparent", hover_color="#2B2B2B")
        self.next_btn.pack(side="left", padx=5)
        
        # Fila 2: Progress Bar
        progress_frame = ctk.CTkFrame(center_frame, fg_color="transparent")
        progress_frame.grid(row=2, column=0, sticky="ew", pady=5)
        
        # Time labels and progress bar
        time_frame = ctk.CTkFrame(progress_frame, fg_color="transparent")
        time_frame.pack(fill="x", padx=20)
        
        self.current_time_label = ctk.CTkLabel(time_frame, text="0:00", 
                                             font=("Arial", 11), width=40)
        self.current_time_label.pack(side="left")
        
        self.progress_slider = ctk.CTkSlider(time_frame, from_=0, to=100, 
                                           width=self.PROGRESS_SLIDER_LENGTH, height=12, 
                                           progress_color="#1f6aa5",
                                           command=self._on_progress_drag)
        self.progress_slider.set(0)
        self.progress_slider.pack(side="left", fill="x", expand=True, padx=10)
        self.progress_slider.bind("<Button-1>", self._on_progress_click_start)
        self.progress_slider.bind("<ButtonRelease-1>", self._on_progress_click_end)
        
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
        
        # Espaciador inferior
        ctk.CTkLabel(volume_frame, text="", height=1).grid(row=2, column=0)

    def update_song_info(self, metadata):
        """Actualiza la metadata de la canción actual"""
        self.current_metadata = metadata
        
        self.song_title_label.configure(text=metadata["title"])
        self.artist_label.configure(text=metadata["artist"])
        
        # Usar la duración del audio backend en lugar de la metadata
        self.total_time = self.audio_backend.get_song_length()
        
        # Actualizar etiqueta de tiempo total
        if self.total_time > 0:
            mins = int(self.total_time // 60)
            secs = int(self.total_time % 60)
            self.total_time_label.configure(text=f"{mins}:{secs:02d}")
        else:
            # Fallback a metadata si no hay duración del backend
            try:
                if ":" in metadata["duration"]:
                    mins, secs = metadata["duration"].split(":")
                    self.total_time = int(mins) * 60 + int(secs)
                    self.total_time_label.configure(text=metadata["duration"])
                else:
                    self.total_time = 0
                    self.total_time_label.configure(text="0:00")
            except:
                self.total_time = 0
                self.total_time_label.configure(text="0:00")
        
        self.current_time = 0
        self.current_time_label.configure(text="0:00")
        self.progress_slider.set(0)
        
        # Album art
        if metadata["album_art"]:
            self.album_art_label.configure(image=metadata["album_art"], text="")
        else:
            self.album_art_label.configure(image=None, text="🎵")
        
        # Iniciar timer de progreso si la canción está reproduciéndose
        self._start_progress_timer()

    def _start_progress_timer(self):
        """Inicia el timer para actualizar el progreso de reproducción"""
        self._stop_progress_timer()
        if self.is_playing and self.total_time > 0:
            self.progress_timer = self.parent.after(100, self._update_progress)

    def _stop_progress_timer(self):
        """Detiene el timer de progreso"""
        if self.progress_timer:
            self.parent.after_cancel(self.progress_timer)
            self.progress_timer = None

    def _update_progress(self):
        """Actualiza el progreso de reproducción cada 100ms"""
        if self.is_playing and not self.is_seeking:
            # Obtener posición actual desde el audio backend
            current_pos = self.audio_backend.get_pos()
            
            # Verificar si la canción ha terminado
            if current_pos < self.current_time:  # Se reinició (canción terminó)
                self.current_time = 0
                self._on_song_end()
            else:
                self.current_time = current_pos
            
            # Actualizar labels de tiempo
            mins = int(self.current_time // 60)
            secs = int(self.current_time % 60)
            self.current_time_label.configure(text=f"{mins}:{secs:02d}")
            
            # Actualizar slider (solo si no está siendo arrastrado)
            if self.total_time > 0 and not self.is_seeking:
                progress = (self.current_time / self.total_time) * 100
                self.progress_slider.set(progress)
            
            # Programar siguiente actualización
            self.progress_timer = self.parent.after(100, self._update_progress)
        else:
            self._stop_progress_timer()

    def _on_song_end(self):
        """Maneja el final de la canción"""
        self.is_playing = False
        self.play_pause_btn.configure(text="▶")
        self._stop_progress_timer()
        # Aquí podrías llamar a on_next para reproducir la siguiente canción

    def _on_progress_click_start(self, event):
        """Inicia el proceso de seek"""
        self.is_seeking = True
        # Detener temporalmente el timer durante el seek
        self._stop_progress_timer()
        # NO cambiar el estado de reproducción durante el seek
        # Solo guardar el estado actual para restaurarlo después
        self.was_playing_before_seek = self.is_playing

    def _on_progress_drag(self, value):
        """Maneja el arrastre de la barra de progreso"""
        if self.is_seeking and self.total_time > 0:
            # Actualizar tiempo actual durante el arrastre
            new_time = (float(value) / 100.0) * self.total_time
            mins = int(new_time // 60)
            secs = int(new_time % 60)
            self.current_time_label.configure(text=f"{mins}:{secs:02d}")

    def _on_progress_click_end(self, event):
        """Maneja el final del clic en la barra de progreso (seek)"""
        if self.is_seeking and self.total_time > 0:
            # Calcular nueva posición basada en el valor del slider
            new_pos = (self.progress_slider.get() / 100.0) * self.total_time
            
            # Realizar el seek en el audio backend
            self.audio_backend.seek(new_pos)
            
            # Actualizar tiempo actual
            self.current_time = new_pos
            mins = int(new_pos // 60)
            secs = int(new_pos % 60)
            self.current_time_label.configure(text=f"{mins}:{secs:02d}")
            
            # RESTAURAR el estado de reproducción original
            # Si estaba reproduciéndose antes del seek, continuar reproduciendo
            if self.was_playing_before_seek:
                # Asegurarse de que el estado interno y el botón estén sincronizados
                self.is_playing = True
                self.play_pause_btn.configure(text="⏸")
                self.audio_backend.unpause_music()
            else:
                # Si estaba pausado, mantener pausado
                self.is_playing = False
                self.play_pause_btn.configure(text="▶")
            
        self.is_seeking = False
        
        # REANUDAR EL TIMER después del seek si la canción está reproduciéndose
        if self.is_playing:
            self._start_progress_timer()

    def _on_play_pause(self):
        """Maneja el botón play/pause"""
        if self.is_playing:
            # Pausar
            self.is_playing = False
            self.play_pause_btn.configure(text="▶")
            self._stop_progress_timer()
            if self.on_pause:
                self.on_pause()
        else:
            # Reproducir
            self.is_playing = True
            self.play_pause_btn.configure(text="⏸")
            self._start_progress_timer()
            if self.on_play:
                self.on_play()

    def _on_previous(self):
        """Maneja el botón anterior"""
        if self.current_time > 5:  # Si lleva más de 5 segundos, reiniciar canción
            self.audio_backend.seek(0)
            self.current_time = 0
            self.current_time_label.configure(text="0:00")
            self.progress_slider.set(0)
            # Mantener el estado de reproducción actual
            if self.is_playing:
                self.audio_backend.unpause_music()
        else:  # Si son menos de 5 segundos, canción anterior
            if self.on_previous:
                self.on_previous()
            else:
                print("No previous song handler")

    def _on_next(self):
        """Maneja el botón siguiente"""
        if self.on_next:
            self.on_next()
        else:
            print("No next song handler")

    def _on_volume_change(self, value):
        """Maneja el cambio de volumen"""
        if self.on_volume_change:
            self.on_volume_change(float(value))

    def set_playing_state(self, playing):
        """Actualiza el estado de reproducción desde fuera"""
        self.is_playing = playing
        if playing:
            self.play_pause_btn.configure(text="⏸")
            self._start_progress_timer()
        else:
            self.play_pause_btn.configure(text="▶")
            self._stop_progress_timer()

    def reset_progress(self):
        """Reinicia el progreso cuando cambia la canción"""
        self.current_time = 0
        self.current_time_label.configure(text="0:00")
        self.progress_slider.set(0)
        self._start_progress_timer()

    def destroy(self):
        """Limpia los timers al destruir"""
        self._stop_progress_timer()
        # if hasattr(super(), 'destroy'):
        #     super().destroy()

def add_to(parent_frame, audio_backend, queue_component=None, on_play=None, on_pause=None, 
           on_stop=None, on_volume_change=None, on_previous=None, on_next=None):
    return MediaControlsPane(parent_frame, audio_backend, queue_component, on_play, on_pause, 
                           on_stop, on_volume_change, on_previous, on_next)