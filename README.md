# MyPyPlayer

A simple song player built with CustomTkinter and Python.

It supports basic functionalities like play, pause, next, previous.

You can add folders to explore and play songs from your local directories.

You can create playlists to organize your music.
It has a song queue feature to manage upcoming tracks.

And you can play previously played songs.

## How to set up environment

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

     ```bash
     source venv/bin/activate
     ```

     3.1 Update pip to the latest version:

   ```bash
    pip install --upgrade pip
   ```

4. Install the required packages:

   ```bash
    pip install -r requirements.txt
   ```

## How to run the application

1. Ensure your virtual environment is activated.
2. Run the main application:

   ```bash
    python src/main.py
   ```

## How to build the application into an executable

1. Ensure your virtual environment is activated.
2. Use PyInstaller to build the executable:

   ```bash
   ./release.bat
   ```

## Contributors

- Luis Perez [UnBittenKitten](https://github.com/UnBittenKitten) - Developer, created the file explorer.
- Roberto Carlos [ZULINOSITY](https://github.com/ZULINOSITY) - Developer, created the media controls and made the ux better.
- Nathanael Hernandez [nathah3rnandez-dotcom](https://github.com/nathah3rnandez-dotcom) - Developer, created the song queue pane and the required logic for it.
- Jonathan Javier [FudgeBit](https://github.com/FudgeBit) - Developer, created the playlist pane and the sources management system.
