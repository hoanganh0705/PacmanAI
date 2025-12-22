# PacmanAI Project Documentation

## Overview

PacmanAI is a Python-based implementation of the classic Pacman game using the Pygame library. The game incorporates various AI search algorithms to control Pacman's movement, making it an educational tool for understanding pathfinding and adversarial search techniques. Players can select different levels, each utilizing specific algorithms, and navigate mazes to eat food while avoiding ghosts.

## Features

- **Multiple Levels**: Four levels with increasing difficulty and different AI algorithms.
- **Algorithm Integration**: Supports BFS, DFS, A\*, Local Search, Minimax, Alpha-Beta Pruning, and Expectimax.
- **Interactive Menu**: Start screen to choose level and map.
- **Real-time Gameplay**: Smooth animations and collision detection.
- **Scoring System**: Points for eating food, penalties for moves.
- **Win/Lose Conditions**: Game ends on collision with ghosts or eating all food.

## Project Structure

```
PacmanAI/
├── Document/                 # Documentation files
├── Input/                    # Map files organized by levels
│   ├── Level1/               # Maps for Level 1
│   ├── Level2/               # Maps for Level 2
│   ├── Level3/               # Maps for Level 3
│   └── Level4/               # Maps for Level 4
├── Source/                   # Main source code
│   ├── Algorithms/           # AI search algorithms
│   │   ├── AStar.py          # A* search implementation
│   │   ├── AlphaBetaPruning.py # Alpha-Beta Pruning for Minimax
│   │   ├── BFS.py            # Breadth-First Search
│   │   ├── DFS.py            # Depth-First Search
│   │   ├── Expectimax.py     # Expectimax algorithm
│   │   ├── Ghost_Move.py     # Ghost movement logic (A* for Level 4)
│   │   ├── LocalSearch.py    # Local search for Level 3
│   │   ├── Minimax.py        # Minimax algorithm for Level 4
│   │   └── SearchAgent.py    # Dispatcher for algorithms
│   ├── Object/               # Game object classes
│   │   ├── Food.py           # Food entity
│   │   ├── Menu.py           # Menu and button handling
│   │   ├── Player.py         # Pacman and ghost entities
│   │   └── Wall.py           # Wall entity
│   ├── Utils/                # Utility functions
│   │   └── utils.py          # Helper functions (validity checks, distance, etc.)
│   ├── constants.py          # Game constants (colors, sizes, algorithms)
│   ├── main.py               # Main game loop and logic
│   └── requirements.txt      # Python dependencies
└── images/                   # Image assets for Pacman and ghosts
```

## Installation and Setup

1. **Prerequisites**:

   - Python 3.x
   - Pygame library

2. **Install Dependencies**:

   ```
   pip install -r Source/requirements.txt
   ```

3. **Run the Game**:

   ```
   cd Source
   python main.py
   ```

4. **Assets**: Ensure `images/` folder contains the required PNG files for Pacman and ghosts.

## How the Game Works

- **Initialization**: Load selected map, initialize walls, food, ghosts, and Pacman.
- **Game Loop**:
  - Calculate Pacman's next move using the level's algorithm.
  - Move ghosts (randomly or via A\*).
  - Check for collisions and food consumption.
  - Update score and redraw screen.
- **End Game**: Display win/lose screen with options to continue or quit.

## Algorithms and Levels

- **Level 1 & 2**: Use BFS to find paths to nearest food.
- **Level 3**: Local Search for exploration.
- **Level 4**: Minimax for adversarial play against ghosts.
- Algorithms are selected via `LEVEL_TO_ALGORITHM` in `constants.py`.

## Key Classes and Functions

- **Player**: Handles Pacman/ghost position, image, movement.
- **Food**: Represents collectible items.
- **Wall**: Maze boundaries.
- **Menu**: UI for level/map selection.
- **SearchAgent**: Executes chosen algorithm.
- **Utils**: Path validation, distance calculations.

## Map Format

Maps are text files in `Input/LevelX/mapY.txt`:

- First line: `N M` (rows, columns)
- Next N lines: M integers (0=empty, 1=wall, 2=food, 3=ghost)
- Last line: Pacman's start position `row col`

## Contributing

- Modify algorithms in `Algorithms/` for experimentation.
- Add new maps in `Input/`.
- Update constants in `constants.py` for customization.
