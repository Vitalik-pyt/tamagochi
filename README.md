# Ursina Tamagotchi Game 🐱

A simple, interactive Tamagotchi-style pet simulator built with Python and the **Ursina Engine**. Take care of your virtual pet, keep it fed, and play a mini-game to achieve the highest score!

## 🎮 Features

* **Real-time Needs:** Your pet's hunger increases over time. Keep an eye on the status bar!
* **Interactive Feeding:** Use the "Feed" button to lower hunger and see a fun scale animation.
* **Jump Mini-game:** Click "Play" to start a side-scrolling obstacle game.
    * Jump over cacti using the **Spacebar**.
    * Successful dodges increase your score and slightly reduce hunger.
* **Highscore System:** The game automatically saves your best score to a `highscore.txt` file.
* **Permadeath:** If hunger reaches 100%, the pet dies and the game ends.

## 🛠️ Installation

1.  **Requirement:** Make sure you have Python installed on your system.
2.  **Install Ursina Engine:**
    ```bash
    pip install ursina
    ```
3.  **Assets:** Ensure you have the pet texture file (`cat_face.jpg`) in the same directory as the script.

## 🚀 How to Run

Run the game using the following command:
```bash
python tamagochi.py
