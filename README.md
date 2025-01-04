# Battle City in Python 🛡️💥

A **Python-based remake of the classic Battle City game**, implemented using the Pygame library. This project is a course assignment for the **Python Programming course at Jiangnan University**. The game offers a nostalgic gameplay experience with modern enhancements and improvements.

## 🛠️ Technologies Used

-   **Python**: Core programming language.
-   **Pygame**: Game development library for handling graphics, audio, and input.

## 📂 Project Structure

```txt
BattleCity/
├── BattleCity.py               # Main script to run the game
├── assets/                     # Contains all game resources
│   ├── audios/                 # Sound effects used in the game
│   ├── font/                   # Fonts used in the game
│   ├── images/                 # All graphical assets
│   ├── saves/                  # Saved game states
│   └── screenshots/            # Screenshots taken during gameplay
├── dist/                       # Distribution-ready builds
│   ├── Linux/                  # Build for Linux systems
│   └── Windows/                # Build for Windows systems
├── entity/                     # Game entity definitions and logic
│   ├── __init__.py             # Marks this as a Python package
│   ├── bullet.py               # Logic for bullets
│   ├── food.py                 # Logic for collectible items
│   ├── home.py                 # Logic for the base/home object
│   ├── resources.py            # Resource management
│   ├── result.py               # Handles game results and scores
│   ├── scene.py                # Scene and map-related logic
│   └── tank.py                 # Logic for player and enemy tanks
├── git-log.txt                 # Development log generated via Git
├── requirements.txt            # Python dependencies for the project
├── utils/                      # Utility modules
│   ├── __init__.py             # Marks this as a Python package
│   ├── config.py               # Configuration settings
│   └── tools.py                # General-purpose utility functions
└── views/                      # UI and display logic
    ├── __init__.py             # Marks this as a Python package
    ├── archive.py              # Save/load game archives
    ├── menu.py                 # Menu interface logic
    ├── print_screen.py         # Screenshot capture and display
    └── ui.py                   # General UI rendering logic
```

## 🚀 Getting Started

### Prerequisites

-   Python 3.8 or later installed on your system.
-   `pip` package manager.

### Installation

1.  Clone this repository:

    ```bash
    git clone https://github.com/WXY-V1hZ/BattleCity.git
    cd BattleCity
    ```

2.  Install required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

### Running the Game

Run the game using:

```bash
python BattleCity.py
```

## 🤝 Contributions

Contributions are welcome! Feel free to open issues or submit pull requests for bug fixes, new features, or enhancements.

## 📜 License

This project is open-source and available under the [MIT License](https://chatgpt.com/c/LICENSE).

---

Let me know if you want to modify or add any sections!