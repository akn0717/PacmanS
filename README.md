# PacmanS

The PacmanS project is inspired from the classic legendary game Pacman. The objective of our game is for the players to navigate Pacman through an enclosed maze, eating Pac-Dots to increase the score. The player with the highest accumulated score, wins the game. The game was written in Python utilizing pygame library for gameplay development and TCP socket for netwoking between server and players.


![image](https://github.com/akn0717/PacmanS/assets/59268707/b1d289ec-e2ae-4860-a038-c9a1feedf8d9)

## How to Use
- Setup virtual environment, virual environment helps isolating all the dependencies from your global environment, this avoids conflicts if you have many Python projects that require different dependency versions.
```bash
# create new Python virtual environment venv
python -m venv venv
```

- Activate Python virtual environment.
```bash
# Linux:
source ./venv/bin/activate

# Window:
.\venv\Scripts\activate
```

- Install dependencies.
```bash
pip install -r requirements.txt
```
- To play.
```bash
python main.py
```

## Supported OS
Python version 3.7.8 on

- Windows 10 <br>
- Linux <br>
- MAC OS (Not tested) <br>
