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
        
        # Timer para actualizar el progreso
        self.progress_timer = None
        
        self._build_ui()
        
    def _build_ui(self):
        # Main frame
        main_frame = ctk.CTkFrame(self.parent, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=20, pady=15)
        
        # --- TOP SECTION: Album Art + Song Info + Controls ---
        top_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        top_frame.pack(fill="x", pady=(0, 10))
        
        # Album Art (izquierda)
        self.album_art_container = ctk.CTkFrame(top_frame, width=120, height=120, 
                                               fg_color="transparent", corner_radius=8)
        self.album_art_container.pack(side="left", padx=(0, 20))
        self.album_art_container.pack_propagate(False)
        
        self.album_art_label = ctk.CTkLabel(self.album_art_container, text="🎵", 
                                          image=None, width=120, height=120,
                                          font=("Arial", 24), corner_radius=8)
        self.album_art_label.pack(fill="both", expand=True)
        
        # Centro: Song Info + Progress Bar
        center_frame = ctk.CTkFrame(top_frame, fg_color="transparent")
        center_frame.pack(side="left", fill="both", expand=True)
        
        # Song Info (parte superior del centro)
        info_frame = ctk.CTkFrame(center_frame, fg_color="transparent")
        info_frame.pack(fill="x", pady=(0, 5))
        
        self.song_title_label = ctk.CTkLabel(info_frame, text="No song selected", 
                                           font=("Arial", 18, "bold"), anchor="w")
        self.song_title_label.pack(anchor="w")
        
        self.artist_label = ctk.CTkLabel(info_frame, text="Unknown Artist", 
                                       font=("Arial", 14), anchor="w", text_color="gray")
        self.artist_label.pack(anchor="w", pady=(2, 0))
        
        # Progress Bar (parte inferior del centro - a la altura del artista)
        progress_frame = ctk.CTkFrame(center_frame, fg_color="transparent")
        progress_frame.pack(fill="x", pady=(5, 0))
        
        # Time labels and progress bar
        time_frame = ctk.CTkFrame(progress_frame, fg_color="transparent")
        time_frame.pack(fill="x")
        
        self.current_time_label = ctk.CTkLabel(time_frame, text="0:00", 
                                             font=("Arial", 11), width=40)
        self.current_time_label.pack(side="left")
        
        self.progress_slider = ctk.CTkSlider(time_frame, from_=0, to=100, 
                                           height=15, progress_color="#1f6aa5")
        self.progress_slider.set(0)
        self.progress_slider.pack(side="left", fill="x", expand=True, padx=10)
        self.progress_slider.bind("<Button-1>", self._on_progress_click)
        
        self.total_time_label = ctk.CTkLabel(time_frame, text="0:00", 
                                           font=("Arial", 11), width=40)
        self.total_time_label.pack(side="right")
        
        # Derecha: Controls + Volume (alineados verticalmente al centro)
        right_frame = ctk.CTkFrame(top_frame, fg_color="transparent")
        right_frame.pack(side="right", fill="both", padx=(20, 0))
        
        # Container principal para controles y volumen (centrado verticalmente)
        controls_main_container = ctk.CTkFrame(right_frame, fg_color="transparent")
        controls_main_container.pack(expand=True, fill="both")
        
        # Frame para centrar verticalmente todo el contenido derecho
        vertical_center_frame = ctk.CTkFrame(controls_main_container, fg_color="transparent")
        vertical_center_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        # Controls container (BOTONES CENTRADOS)
        controls_container = ctk.CTkFrame(vertical_center_frame, fg_color="transparent")
        controls_container.pack(pady=(0, 15))  # Espacio entre botones y volumen
        
        # Frame para centrar los botones horizontalmente
        button_center_frame = ctk.CTkFrame(controls_container, fg_color="transparent")
        button_center_frame.pack(anchor="center")
        
        self.previous_btn = ctk.CTkButton(button_center_frame, text="⏮", width=45, height=45,
                                        font=("Arial", 18), command=self._on_previous,
                                        fg_color="transparent", hover_color="#2B2B2B")
        self.previous_btn.pack(side="left", padx=5)
        
        self.play_pause_btn = ctk.CTkButton(button_center_frame, text="▶", width=55, height=55,
                                          font=("Arial", 20), command=self._on_play_pause,
                                          fg_color="#1f6aa5", hover_color="#1a5a8a")
        self.play_pause_btn.pack(side="left", padx=10)
        
        self.next_btn = ctk.CTkButton(button_center_frame, text="⏭", width=45, height=45,
                                    font=("Arial", 18), command=self._on_next,
                                    fg_color="transparent", hover_color="#2B2B2B")
        self.next_btn.pack(side="left", padx=5)
        
        # Volume control (centrado respecto al eje Y)
        volume_frame = ctk.CTkFrame(vertical_center_frame, fg_color="transparent")
        volume_frame.pack()
        
        # Frame para centrar el volumen horizontalmente
        volume_center_frame = ctk.CTkFrame(volume_frame, fg_color="transparent")
        volume_center_frame.pack(anchor="center")
        
        volume_label = ctk.CTkLabel(volume_center_frame, text="🔊", font=("Arial", 14))
        volume_label.pack(side="left", padx=(0, 8))
        
        self.volume_slider = ctk.CTkSlider(volume_center_frame, from_=0, to=1, width=100,
                                         height=15, command=self._on_volume_change)
        self.volume_slider.set(0.5)
        self.volume_slider.pack(side="left")

    def update_song_info(self, metadata):
        """Actualiza la metadata de la canción actual"""
        self.current_metadata = metadata
        
        self.song_title_label.configure(text=metadata["title"])
        self.artist_label.configure(text=metadata["artist"])
        
        # Parse duration para el progress bar
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
            self.progress_timer = self.parent.after(1000, self._update_progress)

    def _stop_progress_timer(self):
        """Detiene el timer de progreso"""
        if self.progress_timer:
            self.parent.after_cancel(self.progress_timer)
            self.progress_timer = None

    def _update_progress(self):
        """Actualiza el progreso de reproducción cada segundo"""
        if self.is_playing and self.current_time < self.total_time:
            self.current_time += 1
            
            # Actualizar labels de tiempo
            mins = self.current_time // 60
            secs = self.current_time % 60
            self.current_time_label.configure(text=f"{mins}:{secs:02d}")
            
            # Actualizar slider
            if self.total_time > 0:
                progress = (self.current_time / self.total_time) * 100
                self.progress_slider.set(progress)
            
            # Programar siguiente actualización
            self.progress_timer = self.parent.after(1000, self._update_progress)
        else:
            self._stop_progress_timer()

    def _on_progress_click(self, event):
        """Maneja el clic en la barra de progreso (para futuro seek)"""
        print("Progress bar clicked - Seek functionality not implemented yet")

    def _on_play_pause(self):
        """Maneja el botón play/pause"""
        if self.is_playing:
            self.is_playing = False
            self.play_pause_btn.configure(text="▶")
            self._stop_progress_timer()
            if self.on_pause:
                self.on_pause()
        else:
            self.is_playing = True
            self.play_pause_btn.configure(text="⏸")
            self._start_progress_timer()
            if self.on_play:
                self.on_play()

    def _on_previous(self):
        """Maneja el botón anterior"""
        if self.current_time > 5:  # Si lleva más de 5 segundos, reiniciar canción
            self.current_time = 0
            self.current_time_label.configure(text="0:00")
            self.progress_slider.set(0)
            if self.on_play:  # Reiniciar reproducción
                self.on_play()
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
        super().destroy()

def add_to(parent_frame, audio_backend, queue_component=None, on_play=None, on_pause=None, 
           on_stop=None, on_volume_change=None, on_previous=None, on_next=None):
    return MediaControlsPane(parent_frame, audio_backend, queue_component, on_play, on_pause, 
                           on_stop, on_volume_change, on_previous, on_next)