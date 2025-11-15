# MyPyPlayer

A simple media player built with CustomTkinter and Python.

# How to set up environment

1. Clone the repository:

   ```bash
    git clone <https://github.com/UnBittenKitten/MyPyPlayer.git>
    cd MyPyPlayer

   ```

2. Create a virtual environment:

   ```bash
    python -m venv venv
   ```

3. Activate the virtual environment:

   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS and Linux:
     `bash
source venv/bin/activate
`
     3.1 Update pip to the latest version:

   ```bash
    pip install --upgrade pip
   ```

4. Install the required packages:
   ```bash
    pip install -r requirements.txt
   ```

# How to run the application

1. Ensure your virtual environment is activated.
2. Run the main application:
   ```bash
    python src/main.py
   ```

# How to build the application into an executable

1. Ensure your virtual environment is activated.
2. Use PyInstaller to build the executable:
   ```bash
   ./release.bat
   ```
