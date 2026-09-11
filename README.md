# 🧭 Python Pathfinding Visualizer

A terminal-based **Pathfinding Visualizer built with Python** that demonstrates how different pathfinding algorithms explore a maze and find the shortest path.

The project currently supports **Breadth-First Search (BFS)** and **A* Search**, with animated visualization, maze generation, path reconstruction, and performance statistics.

---

## ✨ Features

* 🧭 **Breadth-First Search (BFS)**
* ⭐ **A* Search Algorithm**
* 🎬 Real-time pathfinding animation
* 👀 Visualizes explored/visited cells
* 🛣️ Displays the final shortest path
* 🧱 Random maze generation
* ✅ Random maze generation with a guaranteed path
* 📊 Displays path length and cells explored
* 🔄 Reset to the default maze
* 🎨 Color-coded terminal interface
* 🚫 Handles cases where no path exists
* 🔁 Run multiple algorithms without restarting the program

---

## 🖥️ Preview

The visualizer uses the following symbols:

```text
O  → Start position
X  → End position
#  → Wall
.  → Explored cell
@  → Currently explored cell
*  → Final path
```

Example:

```text
# O . . # # . . . #
# . # . # . # . . #
# . # . . . # . # #
# . # # # . . . . #
# . . . . . # . X #
```

Once a path is found:

```text
# O . . # # . . . #
# * # . # . # . . #
# * # * * * # . # #
# * # # # * * * * #
# * * * * * # . X #
```

---

# 🧠 Algorithms

## 🔵 Breadth-First Search (BFS)

BFS explores the maze layer by layer.

It uses a queue to visit neighboring cells:

```text
Start
  ↓
Neighbors
  ↓
Next layer
  ↓
Next layer
  ↓
Destination
```

Because every movement has the same cost, BFS guarantees the **shortest path**.

### Complexity

For a graph with `V` vertices and `E` edges:

```text
Time:  O(V + E)
Space: O(V)
```

---

## ⭐ A* Search

A* improves upon uninformed search by using a heuristic to determine which cells are more promising.

The algorithm uses:

```text
f(n) = g(n) + h(n)
```

Where:

* `g(n)` = cost from the start to the current cell
* `h(n)` = estimated cost from the current cell to the destination
* `f(n)` = total estimated cost

This project uses **Manhattan distance** as the heuristic:

```python
abs(row1 - row2) + abs(col1 - col2)
```

A* can reach the destination while exploring fewer unnecessary cells than BFS.

### Complexity

For this grid implementation, practical performance depends on the maze structure and heuristic, while the priority queue operations add logarithmic overhead.

---

# 🆚 BFS vs A*

One of the main purposes of this project is to visually compare the two algorithms.

For example:

| Algorithm | Path Length | Cells Explored |
| --------- | ----------: | -------------: |
| BFS       |          27 |             82 |
| A*        |          27 |             51 |

Both algorithms can find the same shortest path, but **A*** may explore fewer cells because it uses information about the destination.

The exact numbers depend on the maze.

---

# 🎮 Menu

When the program starts, you'll see:

```text
PATHFINDING VISUALIZER

Choose an option:

    [1] Run BFS
    [2] Run A*
    [3] Generate Random Maze
    [4] Generate Guaranteed Maze
    [5] Reset Default Maze

    [Q] Quit
```

### Controls

| Key | Action                             |
| --- | ---------------------------------- |
| `1` | Run BFS                            |
| `2` | Run A*                             |
| `3` | Generate random maze               |
| `4` | Generate maze with guaranteed path |
| `5` | Reset maze                         |
| `Q` | Quit                               |

---

# 🧱 Maze Generation

The project includes two maze generators.

## Random Maze

Generates a maze with randomly placed walls.

```text
[3] Generate Random Maze
```

Because the walls are random, there is **no guarantee that a path exists**.

This makes it possible to test how the algorithms handle an unsolvable maze.

---

## Guaranteed Maze

The guaranteed maze generator creates a basic route between the start and destination before adding additional random cells.

```text
[4] Generate Guaranteed Maze
```

This ensures that the generated maze has a basic valid route.

---

# 📊 Pathfinding Statistics

After the algorithm finishes, the program displays statistics such as:

```text
PATH FOUND!

Algorithm: A* Search
Path length: 31 cells
Cells explored: 47

Press any key to return to the menu...
```

If the maze is unsolvable:

```text
NO PATH FOUND!

Algorithm: BFS
Cells explored: 73
```

This makes it easier to understand how the algorithms behave.

---

# 🛠️ Technologies Used

* **Python 3**
* `curses`
* `collections.deque`
* `heapq`
* `random`
* `time`

No external libraries are required on Linux/macOS.

For Windows, install:

```bash
pip install windows-curses
```

---

# 🚀 Installation

## 1. Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/python-pathfinding-visualizer.git
```

## 2. Navigate to the project

```bash
cd python-pathfinding-visualizer
```

## 3. Install Windows dependency

If you're using Windows:

```bash
pip install windows-curses
```

Linux and macOS users generally already have access to the `curses` module.

## 4. Run the program

```bash
python main.py
```

Or:

```bash
python3 main.py
```

---

# 📂 Project Structure

```text
python-pathfinding-visualizer/
│
├── main.py
├── README.md
└── .gitignore
```

---

# 🔍 Code Structure

The project is organized into several components.

| Function                 | Purpose                                  |
| ------------------------ | ---------------------------------------- |
| `find_position()`        | Finds the start/end position             |
| `find_neighbors()`       | Finds valid neighboring cells            |
| `draw_maze()`            | Displays the maze                        |
| `reconstruct_path()`     | Reconstructs the discovered path         |
| `bfs()`                  | Performs Breadth-First Search            |
| `heuristic()`            | Calculates Manhattan distance            |
| `astar()`                | Performs A* Search                       |
| `animate_final_path()`   | Animates the final path                  |
| `generate_random_maze()` | Generates a random maze                  |
| `generate_open_maze()`   | Generates a maze with a guaranteed route |
| `show_results()`         | Displays pathfinding statistics          |
| `show_menu()`            | Displays the main menu                   |
| `main()`                 | Runs the application                     |

---

# 📚 Concepts Demonstrated

This project was built to practice and demonstrate:

### Python

* Functions
* Lists
* Sets
* Tuples
* Dictionaries
* Loops
* Conditional statements
* Exception-safe program flow
* Modules
* Terminal interfaces

### Data Structures

* Queue
* Priority Queue
* Set
* Dictionary
* Graph/grid representation

### Algorithms

* Breadth-First Search
* A* Search
* Manhattan distance
* Shortest-path reconstruction

### Software Development

* Modular code organization
* Algorithm visualization
* User input handling
* Performance measurement
* Randomized test cases

---

# 🎯 Learning Objectives

The main goal of this project is to understand how pathfinding algorithms work rather than simply implementing them.

By visualizing each step, you can see:

1. Where the algorithm starts
2. Which cells it explores
3. How it handles obstacles
4. How it chooses the next cell
5. How it reaches the destination
6. How the final path is reconstructed

This makes the difference between **uninformed search (BFS)** and **heuristic search (A*)** much easier to understand.

---

# ⚠️ Windows Users

This project uses Python's `curses` module.

Windows users may encounter:

```text
ModuleNotFoundError: No module named 'curses'
```

Install the Windows-compatible implementation:

```bash
pip install windows-curses
```

Then run:

```bash
python main.py
```

---

# 🔮 Future Improvements

Possible improvements include:

* 🖱️ Mouse-based maze editing
* 🧱 Manually drawing/removing walls
* 📍 Moving the start and end points
* 🎚️ Adjustable animation speed
* 🧮 Dijkstra's Algorithm
* 🧭 Depth-First Search
* 🌀 Greedy Best-First Search
* 📈 Algorithm performance comparison
* 🏗️ Additional maze-generation algorithms
* 🎨 Improved terminal UI
* 🖥️ Graphical interface using Pygame
* 📊 More detailed performance statistics

---

# 📜 License

This project is intended for educational and personal use.

You can add an **MIT License** if you want to make the project freely reusable and distributable.

---

# 👨‍💻 Author

**Aryajeet Jadhav**

Built as a Python algorithm visualization project to explore **pathfinding, graph traversal, data structures, and algorithmic problem solving**.

