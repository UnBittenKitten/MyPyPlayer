import sys
import os

def resource_path(relative_path):
    """ 
    Get absolute path to resource, works for dev and for PyInstaller.
    This is essential for finding assets (like icons) in the compiled .exe.
    """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS # pyright: ignore[reportAttributeAccessIssue]
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)