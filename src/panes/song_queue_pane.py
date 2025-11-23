import customtkinter as ctk
import os

class SongQueuePane:
    def __init__(self, parent_frame, data_manager, audio_backend):
        self.parent = parent_frame
        self.db = data_manager
        self.audio_backend = audio_backend
        self.queue_items = []
        
        self._build_ui()
        
    def _build_ui(self):
        # Title Label
        title_frame = ctk.CTkFrame(self.parent, fg_color="transparent")
        title_frame.pack(fill="x", pady=(10, 5), padx=10)
        
        title_label = ctk.CTkLabel(title_frame, text="Song Queue", 
                                 font=("Arial", 16, "bold"))
        title_label.pack(side="left")
        
        # Clear queue button
        clear_btn = ctk.CTkButton(title_frame, text="Clear", width=60, height=25,
                                command=self.clear_queue)
        clear_btn.pack(side="right")
        
        # Queue list
        self.queue_list = ctk.CTkScrollableFrame(self.parent, fg_color="transparent")
        self.queue_list.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Placeholder
        self.placeholder_label = ctk.CTkLabel(self.queue_list, text="Queue is empty\n\nAdd songs from the explorer",
                                 text_color="gray", justify="center")
        self.placeholder_label.pack(pady=40)

    def add_to_queue(self, song_path):
        """Añade una canción a la cola"""
        # Ocultar placeholder si es la primera canción
        if self.placeholder_label.winfo_viewable():
            self.placeholder_label.pack_forget()
        
        # Crear item de la cola
        queue_item = QueueItem(self.queue_list, song_path, len(self.queue_items))
        queue_item.pack(fill="x", pady=2)
        
        self.queue_items.append({
            'path': song_path,
            'widget': queue_item
        })

    def clear_queue(self):
        """Limpia toda la cola"""
        for item in self.queue_items:
            item['widget'].destroy()
        
        self.queue_items.clear()
        
        # Mostrar placeholder nuevamente
        self.placeholder_label.pack(pady=40)

    def remove_from_queue(self, index):
        """Remueve una canción específica de la cola"""
        if 0 <= index < len(self.queue_items):
            self.queue_items[index]['widget'].destroy()
            self.queue_items.pop(index)
            
            # Reindexar items restantes
            for i, item in enumerate(self.queue_items):
                item['widget'].update_index(i)
            
            # Mostrar placeholder si la cola está vacía
            if not self.queue_items:
                self.placeholder_label.pack(pady=40)

class QueueItem(ctk.CTkFrame):
    def __init__(self, parent, song_path, index):
        super().__init__(parent, fg_color="#333333", height=40)
        self.song_path = song_path
        self.index = index
        
        self._build_ui()
        
    def _build_ui(self):
        # Número de posición
        index_label = ctk.CTkLabel(self, text=f"{self.index + 1}.", 
                                 width=30, font=("Arial", 11))
        index_label.pack(side="left", padx=(10, 5))
        
        # Nombre del archivo (truncado si es muy largo)
        file_name = os.path.basename(self.song_path)
        if len(file_name) > 30:
            display_name = file_name[:27] + "..."
        else:
            display_name = file_name
            
        name_label = ctk.CTkLabel(self, text=display_name, anchor="w",
                                font=("Arial", 11))
        name_label.pack(side="left", padx=5, fill="x", expand=True)
        
        # Botón de eliminar
        remove_btn = ctk.CTkButton(self, text="×", width=25, height=25,
                                 font=("Arial", 14), fg_color="#C9302C", 
                                 hover_color="#96221F",
                                 command=self._remove_self)
        remove_btn.pack(side="right", padx=5)

    def update_index(self, new_index):
        """Actualiza el número de posición"""
        self.index = new_index
        # Buscar y actualizar el label del índice
        for widget in self.winfo_children():
            if isinstance(widget, ctk.CTkLabel) and widget.cget("text").endswith("."):
                widget.configure(text=f"{new_index + 1}.")
                break

    def _remove_self(self):
        """Notifica al padre para remover este item"""
        parent = self.master
        if hasattr(parent, 'remove_from_queue'):
            parent.remove_from_queue(self.index)

def add_to(parent_frame, data_manager, audio_backend):
    return SongQueuePane(parent_frame, data_manager, audio_backend)