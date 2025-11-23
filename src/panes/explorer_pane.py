import customtkinter as ctk
import os
import glob

class ExplorerPane:
    def __init__(self, parent_frame, data_manager, on_song_click=None):
        self.parent = parent_frame
        self.db = data_manager
        self.on_song_click = on_song_click
        self.current_folder = None
        
        self._build_ui()
        
    def _build_ui(self):
        # Title Label
        self.title_label = ctk.CTkLabel(self.parent, text="File Explorer", 
                                      font=("Arial", 16, "bold"))
        self.title_label.pack(pady=(10, 5))
        
        # Current Path Label
        self.path_label = ctk.CTkLabel(self.parent, text="No folder selected", 
                                     font=("Arial", 12), text_color="gray")
        self.path_label.pack(pady=(0, 10))
        
        # Scrollable List for files
        self.scroll_list = ctk.CTkScrollableFrame(self.parent, fg_color="transparent")
        self.scroll_list.pack(fill="both", expand=True, padx=5, pady=5)

    def load_folder(self, folder_path):
        """Carga los archivos de audio de una carpeta"""
        self.current_folder = folder_path
        self.path_label.configure(text=folder_path)
        
        # Limpiar lista anterior
        for widget in self.scroll_list.winfo_children():
            widget.destroy()
        
        # Extensiones de audio soportadas
        audio_extensions = ['*.mp3', '*.wav', '*.flac', '*.ogg', '*.m4a', '*.aac']
        audio_files = []
        
        for extension in audio_extensions:
            pattern = os.path.join(folder_path, '**', extension)
            audio_files.extend(glob.glob(pattern, recursive=True))
        
        # Mostrar archivos
        for file_path in audio_files:
            self._add_song_to_list(file_path)

    def _add_song_to_list(self, file_path):
        """Añade una canción a la lista del explorador"""
        row = ctk.CTkFrame(self.scroll_list, fg_color="#333333")
        row.pack(fill="x", pady=2)
        
        # Nombre del archivo
        file_name = os.path.basename(file_path)
        
        # Label clickeable para reproducir
        lbl = ctk.CTkLabel(row, text=file_name, anchor="w", cursor="hand2")
        lbl.pack(side="left", padx=10, pady=5, fill="x", expand=True)
        
        # Bind click event para reproducir
        lbl.bind("<Button-1>", lambda e, p=file_path: self._on_song_click(p))
        
        # Botón para añadir a la cola
        add_btn = ctk.CTkButton(row, text="+", width=30, height=25,
                              command=lambda p=file_path: self._add_to_queue(p))
        add_btn.pack(side="right", padx=5)
        
        # Hover effects
        lbl.bind("<Enter>", lambda e, l=lbl: l.configure(text_color="#1f6aa5"))
        lbl.bind("<Leave>", lambda e, l=lbl: l.configure(text_color=["#DCE4EE", "#DCE4EE"]))

    def _on_song_click(self, song_path):
        """Maneja el clic en una canción (reproducir)"""
        if self.on_song_click:
            self.on_song_click(song_path)

    def _add_to_queue(self, song_path):
        """Añade canción a la cola (necesitas acceso al queue_component)"""
        # Esto requiere que el parent (app_window) exponga el queue_component
        parent = self.parent
        while parent and not hasattr(parent, 'queue_component'):
            parent = parent.master
            
        if parent and hasattr(parent, 'queue_component'):
            parent.queue_component.add_to_queue(song_path)
            print(f"Added to queue: {song_path}")

def add_to(parent_frame, data_manager, on_song_click=None):
    return ExplorerPane(parent_frame, data_manager, on_song_click)