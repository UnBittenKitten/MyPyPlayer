import customtkinter as ctk
import os

class SourcesPane:
    """
    Controller class for the Sources section.
    It builds the UI inside the given 'parent_frame' and handles interactions.
    """
    def __init__(self, parent_frame, data_manager, on_folder_click=None):
        self.parent = parent_frame
        self.db = data_manager
        self.on_click_callback = on_folder_click # Store the callback function
        
        # Build the UI immediately
        self._build_ui()
        
        # Load initial data
        self._refresh_list()

    def _build_ui(self):
        # Title Label
        self.title_label = ctk.CTkLabel(self.parent, text="Library Sources", font=("Arial", 16, "bold"))
        self.title_label.pack(pady=(10, 5))

        # Add Button
        self.add_btn = ctk.CTkButton(self.parent, text="+ Add Folder", command=self._add_folder_click)
        self.add_btn.pack(pady=5)

        # Scrollable List for the folders
        self.scroll_list = ctk.CTkScrollableFrame(self.parent, fg_color="transparent")
        self.scroll_list.pack(fill="both", expand=True, padx=5, pady=5)

    def _add_folder_click(self):
        """Open dialog to pick a folder, then save to DB."""
        folder_selected = ctk.filedialog.askdirectory()
        if folder_selected:
            success = self.db.add_source(folder_selected)
            if success:
                self._refresh_list()
            else:
                print("Source already exists or invalid.")

    def _refresh_list(self):
        """Clear and rebuild the list of source folders."""
        # 1. Remove old widgets
        for widget in self.scroll_list.winfo_children():
            widget.destroy()

        # 2. Fetch from DB
        sources = self.db.get_sources()

        # 3. Create a row for each source
        for path in sources:
            row = ctk.CTkFrame(self.scroll_list, fg_color="#333333")
            row.pack(fill="x", pady=2)

            # --- NEW LOGIC: Folder Name Only ---
            clean_path = os.path.normpath(path)
            folder_name = os.path.basename(clean_path)
            
            # Fallback for root drives
            if not folder_name:
                folder_name = clean_path

            # Truncate logic
            limit = 25
            if len(folder_name) > limit:
                display_text = folder_name[:limit] + "..."
            else:
                display_text = folder_name
            
            # --- CLICKABLE LABEL ---
            # We set cursor="hand2" to show it's clickable
            lbl = ctk.CTkLabel(row, text=display_text, anchor="w", cursor="hand2")
            lbl.pack(side="left", padx=10, pady=5, fill="x", expand=True)

            # Bind the Left Mouse Click (<Button-1>)
            # We use a lambda to pass the specific 'path' of this row
            lbl.bind("<Button-1>", lambda event, p=path: self._handle_label_click(p))
            
            # Optional: Add hover effect using bind
            lbl.bind("<Enter>", lambda event, l=lbl: l.configure(text_color="#1f6aa5")) # Blue on hover
            lbl.bind("<Leave>", lambda event, l=lbl: l.configure(text_color=["#DCE4EE", "#DCE4EE"])) # Default color

            # Delete Button
            del_btn = ctk.CTkButton(row, text="X", width=30, height=25, 
                                    fg_color="#C9302C", hover_color="#96221F",
                                    command=lambda p=path: self._remove_source(p))
            del_btn.pack(side="right", padx=5)

    def _handle_label_click(self, path):
        """Trigger the callback if it exists."""
        if self.on_click_callback:
            self.on_click_callback(path)

    def _remove_source(self, path):
        """Remove source from DB and refresh UI."""
        self.db.remove_source(path)
        self._refresh_list()

def add_to(parent_frame, data_manager, on_folder_click=None):
    """
    Helper function to initialize this component into a parent frame.
    """
    return SourcesPane(parent_frame, data_manager, on_folder_click)