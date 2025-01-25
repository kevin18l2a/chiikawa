
# Chiikawa Game

Chiikawa is a simple Python game where you control a rabbit to catch falling lemons. The game is built using Tkinter for the graphical user interface and plays sound effects when the rabbit catches a lemon.

## Features

- Control a rabbit character to move left or right.
- Catch falling lemons to increase the score.
- Fun sound effects and animations.
- Built with Python, Tkinter, and the `playsound` library.

## Installation

Follow the steps below to get the project up and running on your local machine.

### 1. Clone the Repository

First, clone the repository to your local machine:

```bash
git clone https://github.com/yourusername/chiikawa-game.git
cd chiikawa-game
```

### 2. Create a Virtual Environment

Create a Python virtual environment to isolate the project's dependencies:

```bash
python -m venv venv
```

### 3. Activate the Virtual Environment

Activate the virtual environment:

- On **Windows**:
    ```bash
    venv\Scripts\activate
    ```

- On **Linux/macOS**:
    ```bash
    source venv/bin/activate
    ```

### 4. Install Dependencies

Once the virtual environment is activated, install the necessary dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### Step 1: Enter the Virtual Environment

If you haven't already activated the virtual environment, activate it:

- On **Windows**:
    ```bash
    venv\Scripts\activate
    ```

- On **Linux/macOS**:
    ```bash
    source venv/bin/activate
    ```

### Step 2: Run the Game

Once the virtual environment is activated, you can run the game by executing:

```bash
python chiikawa.py
```

This will open a window where you can control the rabbit and try to catch falling lemons.

### Step 3: Build the Executable with PyInstaller

If you'd like to create an executable for your game, follow these steps:

1. **Build the Executable:**
   Run the following command to create an executable:

   ```bash
   pyinstaller chiikawa.spec
   ```

   This will create a `dist/` folder containing the executable file. You can distribute this executable without needing Python installed.

2. **Running the Executable:**
   After building the executable, you can find it in the `dist/` folder and run it directly.

## Folder Structure

```
chiikawa-game/
│
├── chiikawa.py              # The main game script
├── chiikawa.spec            # PyInstaller specification file
├── requirements.txt         # List of required Python packages
├── resources/
│   ├── images/              # Folder containing images for the game
│   └── audios/              # Folder containing audio files for the game
└── README.md                # This file
```

## Contributing

We welcome contributions to the Chiikawa game! Here are some steps you can follow to contribute:

1. Fork the repository.
2. Create a new branch:
   ```bash
   git checkout -b feature-branch
   ```
3. Make your changes and commit them:
   ```bash
   git commit -am 'Add new feature'
   ```
4. Push to your branch:
   ```bash
   git push origin feature-branch
   ```
5. Submit a pull request describing your changes.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

For issues or suggestions, feel free to contact us through GitHub Issues or via email at `yourname@example.com`.

---

Thank you for playing Chiikawa! We hope you enjoy the game.
