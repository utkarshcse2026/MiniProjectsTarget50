# 🍎 Fruity Frenzy 🧺

A classic arcade-style fruit-catching game built with Python. Dodge what you can't catch and aim for the high score! This game is a complete, standalone desktop application featuring an animated intro, sound effects, and persistent scoring.


---

## ## Features

* **Animated Intro Screen:** A fun GIF and background music greet you on launch.
* **Dynamic Gameplay:** Catch multiple fruits falling at varying speeds.
* **4-Way Movement:** Full control to move the basket up, down, left, and right.
* **Life System:** Start with three lives, represented by hearts. Lose a life for each missed fruit!
* **Persistent High Score:** The game saves your high score in a `highscore.txt` file.
* **Sound Effects:** Includes background music and a satisfying sound for each catch.
* **Standalone Executable:** Comes with instructions to bundle the entire game into a single `.exe` file for easy distribution.

---

## ## 🛠️ Built With

* **Python 3**
* **Tkinter:** For the graphical user interface (GUI).
* **Pygame:** For handling music and sound effects.
* **Pillow (PIL):** For processing the animated intro GIF.

---

## ## 🚀 Getting Started

Follow these instructions to get a copy of the project up and running on your local machine.

### ### Prerequisites

Make sure you have **Python 3** installed on your system. You can download it from [python.org](https://www.python.org/downloads/).

### ### Installation

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/your_username/FruityFrenzy.git](https://github.com/your_username/FruityFrenzy.git)
    cd FruityFrenzy
    ```

2.  **Install the required Python packages:**
    ```bash
    pip install -r requirements.txt
    ```
    *(You will need to create a `requirements.txt` file with the content below.)*

3.  **Add Assets:**
    Make sure the following asset files are placed in the root directory of the project:
    * `intro.gif` (The intro animation)
    * `music.mp3` (Background music)
    * `1.mp3` (The fruit catch sound effect)
    * `icon.ico` (The icon for the executable)

---

## ## 🎮 How to Play

To run the game from the source code, execute the following command in your terminal from the project's root directory:

```bash
python FruitFrenzy.py
