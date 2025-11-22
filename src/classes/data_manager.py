import sqlite3
import os
import json

class DataManager:
    def __init__(self, app_name="MyPyPlayer"):
        self.app_name = app_name
        self.db_path = self._get_db_path()
        self._init_db()

    def _get_db_path(self):
        """Returns the path to the SQLite DB in AppData/Local or ~/.local/share."""
        if os.name == 'nt':
            base_path = os.getenv('LOCALAPPDATA')
        else:
            base_path = os.path.join(os.path.expanduser("~"), ".local", "share")
        
        app_data_dir = os.path.join(base_path, self.app_name)
        os.makedirs(app_data_dir, exist_ok=True)
        return os.path.join(app_data_dir, "library.db")

    def _init_db(self):
        """Initialize the database tables."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            # 0. Table for UI settings
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS ui_settings (
                key TEXT PRIMARY KEY,
                value TEXT
                )
            ''')
            
            # 1. Sources (Folders)
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS sources (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    path TEXT UNIQUE NOT NULL
                )
            ''')
            
            # 2. Playlists
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS playlists (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # 3. Playlist Items (with Order Index)
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS playlist_items (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    playlist_id INTEGER NOT NULL,
                    file_path TEXT NOT NULL,
                    order_index INTEGER NOT NULL,
                    FOREIGN KEY (playlist_id) REFERENCES playlists(id) ON DELETE CASCADE,
                    UNIQUE(playlist_id, file_path)
                )
            ''')
            conn.commit()

    # --- Source Management ---

    def add_source(self, folder_path):
        if not folder_path: return False
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("INSERT INTO sources (path) VALUES (?)", (folder_path,))
                return True
        except sqlite3.IntegrityError:
            return False 
        except Exception as e:
            print(f"DB Error (add_source): {e}")
            return False

    def get_sources(self):
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT path FROM sources")
                return [row[0] for row in cursor.fetchall()]
        except Exception as e:
            print(f"DB Error (get_sources): {e}")
            return []

    def remove_source(self, folder_path):
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("DELETE FROM sources WHERE path = ?", (folder_path,))
                return True
        except Exception as e:
            print(f"DB Error (remove_source): {e}")
            return False

    # --- Playlist Management ---

    def create_playlist(self, name):
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("INSERT INTO playlists (name) VALUES (?)", (name,))
                return True
        except sqlite3.IntegrityError:
            return False
        except Exception as e:
            print(f"DB Error (create_playlist): {e}")
            return False

    def get_playlists(self):
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT name FROM playlists")
                return [row[0] for row in cursor.fetchall()]
        except Exception as e:
            print(f"DB Error (get_playlists): {e}")
            return []

    def delete_playlist(self, name):
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("DELETE FROM playlists WHERE name = ?", (name,))
                return True
        except Exception as e:
            print(f"DB Error (delete_playlist): {e}")
            return False

    def add_song_to_playlist(self, playlist_name, file_path):
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # 1. Get Playlist ID
                cursor.execute("SELECT id FROM playlists WHERE name = ?", (playlist_name,))
                result = cursor.fetchone()
                if not result:
                    return False
                playlist_id = result[0]
                
                # 2. Get Next Order Index
                cursor.execute("SELECT MAX(order_index) FROM playlist_items WHERE playlist_id = ?", (playlist_id,))
                max_index = cursor.fetchone()[0]
                next_index = (max_index + 1) if max_index is not None else 0
                
                # 3. Insert
                cursor.execute(
                    "INSERT INTO playlist_items (playlist_id, file_path, order_index) VALUES (?, ?, ?)",
                    (playlist_id, file_path, next_index)
                )
                return True
        except sqlite3.IntegrityError:
            return False # Song already in playlist
        except Exception as e:
            print(f"DB Error (add_song_to_playlist): {e}")
            return False

    def get_songs_in_playlist(self, playlist_name):
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Join tables to get file paths ordered by index
                query = '''
                    SELECT pi.file_path 
                    FROM playlist_items pi
                    JOIN playlists p ON pi.playlist_id = p.id
                    WHERE p.name = ?
                    ORDER BY pi.order_index ASC
                '''
                cursor.execute(query, (playlist_name,))
                return [row[0] for row in cursor.fetchall()]
        except Exception as e:
            print(f"DB Error (get_songs_in_playlist): {e}")
            return []

    def remove_song_from_playlist(self, playlist_name, file_path):
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Subquery to find ID is cleaner, but simple join delete is also fine
                # We need the playlist ID first to be safe
                cursor.execute("SELECT id FROM playlists WHERE name = ?", (playlist_name,))
                result = cursor.fetchone()
                if not result:
                    return False
                playlist_id = result[0]

                conn.execute(
                    "DELETE FROM playlist_items WHERE playlist_id = ? AND file_path = ?",
                    (playlist_id, file_path)
                )
                return True
        except Exception as e:
            print(f"DB Error (remove_song_from_playlist): {e}")
            return False

            
    # --- UI Settings Management ---
    def save_setting(self, key, value):
        """Saves a setting. Value is automatically JSON stringified."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        try:
            json_val = json.dumps(value)
            cursor.execute('INSERT OR REPLACE INTO ui_settings (key, value) VALUES (?, ?)', (key, json_val))
            conn.commit()
        except Exception as e:
            print(f"Error saving setting {key}: {e}")
        finally:
            conn.close()

    def get_setting(self, key, default=None):
        """Retrieves a setting. Returns default if not found."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT value FROM ui_settings WHERE key = ?', (key,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            try:
                return json.loads(row[0])
            except json.JSONDecodeError:
                return row[0]
        return default