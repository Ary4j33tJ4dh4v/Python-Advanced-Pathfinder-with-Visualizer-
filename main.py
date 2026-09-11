import curses
import random
import time
from collections import deque
from heapq import heappush, heappop


# ============================================================
# CONFIGURATION
# ============================================================

WALL = "#"
EMPTY = " "
START = "O"
END = "X"

ANIMATION_DELAY = 0.05


# ============================================================
# DEFAULT MAZE
# ============================================================

DEFAULT_MAZE = [
    ["#", "O", "#", "#", "#", "#", "#", "#", "#"],
    ["#", " ", " ", " ", " ", " ", " ", " ", "#"],
    ["#", " ", "#", "#", " ", "#", "#", " ", "#"],
    ["#", " ", "#", " ", " ", " ", "#", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", "#", "#"],
    ["#", " ", " ", " ", " ", " ", " ", " ", "#"],
    ["#", "#", "#", "#", "#", "#", "#", "X", "#"]
]


# ============================================================
# COLORS
# ============================================================

def setup_colors():
    curses.start_color()

    curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_BLACK)      # Walls
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)     # Start
    curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)       # End
    curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_BLACK)    # Visited
    curses.init_pair(5, curses.COLOR_MAGENTA, curses.COLOR_BLACK)   # Path
    curses.init_pair(6, curses.COLOR_CYAN, curses.COLOR_BLACK)      # Current
    curses.init_pair(7, curses.COLOR_WHITE, curses.COLOR_BLACK)      # Text


# ============================================================
# MAZE UTILITIES
# ============================================================

def copy_maze(maze):
    """Create a copy of the maze."""

    return [row[:] for row in maze]


def find_position(maze, target):
    """Find the position of START or END."""

    for row in range(len(maze)):
        for col in range(len(maze[row])):
            if maze[row][col] == target:
                return row, col

    return None


def find_neighbors(maze, row, col):
    """Find all valid neighboring cells."""

    directions = [
        (-1, 0),  # Up
        (1, 0),   # Down
        (0, -1),  # Left
        (0, 1)    # Right
    ]

    neighbors = []

    for row_change, col_change in directions:

        new_row = row + row_change
        new_col = col + col_change

        if (
            0 <= new_row < len(maze)
            and 0 <= new_col < len(maze[0])
            and maze[new_row][new_col] != WALL
        ):
            neighbors.append((new_row, new_col))

    return neighbors


# ============================================================
# DRAW MAZE
# ============================================================

def draw_maze(
    maze,
    stdscr,
    visited=None,
    path=None,
    current=None,
    algorithm=""
):
    """Draw the maze and pathfinding information."""

    if visited is None:
        visited = set()

    if path is None:
        path = []

    stdscr.clear()

    for row in range(len(maze)):

        for col in range(len(maze[row])):

            position = (row, col)
            value = maze[row][col]

            # Final path
            if position in path:
                character = "*"
                color = curses.color_pair(5)

            # Currently processing
            elif position == current:
                character = "@"
                color = curses.color_pair(6)

            # Visited cell
            elif position in visited:
                character = "."
                color = curses.color_pair(4)

            # Start
            elif value == START:
                character = "O"
                color = curses.color_pair(2)

            # End
            elif value == END:
                character = "X"
                color = curses.color_pair(3)

            # Wall
            elif value == WALL:
                character = "#"
                color = curses.color_pair(1)

            # Empty space
            else:
                character = " "
                color = curses.color_pair(7)

            stdscr.addstr(
                row,
                col * 2,
                character,
                color
            )

    # Information below maze
    info_row = len(maze) + 1

    stdscr.addstr(
        info_row,
        0,
        f"Algorithm: {algorithm}"
    )

    stdscr.addstr(
        info_row + 1,
        0,
        f"Visited: {len(visited)}"
    )

    stdscr.refresh()


# ============================================================
# PATH RECONSTRUCTION
# ============================================================

def reconstruct_path(parent, start, end):
    """Reconstruct the path from END back to START."""

    path = []

    current = end

    while current != start:

        path.append(current)

        if current not in parent:
            return []

        current = parent[current]

    path.append(start)

    path.reverse()

    return path


# ============================================================
# BREADTH-FIRST SEARCH
# ============================================================

def bfs(maze, stdscr):
    """
    Breadth-First Search.

    BFS guarantees the shortest path in an unweighted maze.
    """

    start = find_position(maze, START)
    end = find_position(maze, END)

    if start is None or end is None:
        return [], 0

    queue = deque([start])

    visited = {start}

    parent = {}

    explored = 0

    while queue:

        current = queue.popleft()

        explored += 1

        draw_maze(
            maze,
            stdscr,
            visited=visited,
            current=current,
            algorithm="BFS"
        )

        time.sleep(ANIMATION_DELAY)

        # Destination reached
        if current == end:

            path = reconstruct_path(
                parent,
                start,
                end
            )

            animate_final_path(
                maze,
                stdscr,
                visited,
                path,
                "BFS"
            )

            return path, explored

        # Explore neighbors
        for neighbor in find_neighbors(
            maze,
            current[0],
            current[1]
        ):

            if neighbor in visited:
                continue

            visited.add(neighbor)

            parent[neighbor] = current

            queue.append(neighbor)

    return [], explored


# ============================================================
# A* HEURISTIC
# ============================================================

def heuristic(a, b):
    """
    Manhattan distance.

    Used by A* to estimate the distance
    between two cells.
    """

    return abs(a[0] - b[0]) + abs(a[1] - b[1])


# ============================================================
# A* SEARCH
# ============================================================

def astar(maze, stdscr):
    """
    A* Search algorithm.

    Uses the Manhattan distance heuristic
    to prioritize promising cells.
    """

    start = find_position(maze, START)
    end = find_position(maze, END)

    if start is None or end is None:
        return [], 0

    open_set = []

    heappush(
        open_set,
        (0, start)
    )

    parent = {}

    g_score = {
        start: 0
    }

    visited = set()

    explored = 0

    while open_set:

        _, current = heappop(open_set)

        if current in visited:
            continue

        visited.add(current)

        explored += 1

        draw_maze(
            maze,
            stdscr,
            visited=visited,
            current=current,
            algorithm="A*"
        )

        time.sleep(ANIMATION_DELAY)

        # Destination reached
        if current == end:

            path = reconstruct_path(
                parent,
                start,
                end
            )

            animate_final_path(
                maze,
                stdscr,
                visited,
                path,
                "A*"
            )

            return path, explored

        # Explore neighbors
        for neighbor in find_neighbors(
            maze,
            current[0],
            current[1]
        ):

            new_cost = g_score[current] + 1

            if (
                neighbor not in g_score
                or new_cost < g_score[neighbor]
            ):

                g_score[neighbor] = new_cost

                parent[neighbor] = current

                f_score = (
                    new_cost
                    + heuristic(neighbor, end)
                )

                heappush(
                    open_set,
                    (f_score, neighbor)
                )

    return [], explored


# ============================================================
# FINAL PATH ANIMATION
# ============================================================

def animate_final_path(
    maze,
    stdscr,
    visited,
    path,
    algorithm
):
    """Animate the final discovered path."""

    for i in range(len(path)):

        current_path = path[:i + 1]

        draw_maze(
            maze,
            stdscr,
            visited=visited,
            path=current_path,
            algorithm=algorithm
        )

        time.sleep(0.03)


# ============================================================
# RANDOM MAZE GENERATOR
# ============================================================

def generate_random_maze(rows=15, cols=31):
    """
    Generate a random maze.

    Note:
    Random generation does not guarantee
    that a path exists.
    """

    maze = []

    for row in range(rows):

        current_row = []

        for col in range(cols):

            # Create border walls
            if (
                row == 0
                or row == rows - 1
                or col == 0
                or col == cols - 1
            ):
                current_row.append(WALL)

            else:

                # 25% chance of wall
                if random.random() < 0.25:
                    current_row.append(WALL)

                else:
                    current_row.append(EMPTY)

        maze.append(current_row)

    # Start and end
    maze[1][1] = START
    maze[rows - 2][cols - 2] = END

    return maze


# ============================================================
# GUARANTEED RANDOM MAZE
# ============================================================

def generate_open_maze(rows=15, cols=31):
    """
    Generate a maze with a guaranteed basic path.

    Creates an open grid with random walls placed
    away from the main path.
    """

    maze = [
        [WALL for _ in range(cols)]
        for _ in range(rows)
    ]

    # Create a basic path from start to end
    row = 1
    col = 1

    maze[row][col] = START

    while row < rows - 2 or col < cols - 2:

        if row == rows - 2:
            col += 1

        elif col == cols - 2:
            row += 1

        elif random.choice([True, False]):
            row += 1

        else:
            col += 1

        maze[row][col] = EMPTY

    maze[rows - 2][cols - 2] = END

    # Add random open cells
    for r in range(1, rows - 1):

        for c in range(1, cols - 1):

            if maze[r][c] == WALL:

                if random.random() < 0.35:
                    maze[r][c] = EMPTY

    return maze


# ============================================================
# RESULTS SCREEN
# ============================================================

def show_results(
    stdscr,
    algorithm,
    path,
    explored
):
    """Display final pathfinding statistics."""

    stdscr.clear()

    if path:

        stdscr.addstr(
            2,
            2,
            "PATH FOUND!",
            curses.color_pair(2)
            | curses.A_BOLD
        )

        stdscr.addstr(
            4,
            2,
            f"Algorithm: {algorithm}"
        )

        stdscr.addstr(
            5,
            2,
            f"Path length: {len(path)} cells"
        )

        stdscr.addstr(
            6,
            2,
            f"Cells explored: {explored}"
        )

    else:

        stdscr.addstr(
            2,
            2,
            "NO PATH FOUND!",
            curses.color_pair(3)
            | curses.A_BOLD
        )

        stdscr.addstr(
            4,
            2,
            f"Algorithm: {algorithm}"
        )

        stdscr.addstr(
            5,
            2,
            f"Cells explored: {explored}"
        )

    stdscr.addstr(
        8,
        2,
        "Press any key to return to the menu..."
    )

    stdscr.refresh()

    stdscr.getch()


# ============================================================
# MENU
# ============================================================

def show_menu(stdscr):
    """Display the main menu."""

    stdscr.clear()

    title = "PATHFINDING VISUALIZER"

    stdscr.addstr(
        1,
        2,
        title,
        curses.A_BOLD
    )

    stdscr.addstr(
        3,
        2,
        "Choose an option:"
    )

    stdscr.addstr(
        5,
        4,
        "[1] Run BFS"
    )

    stdscr.addstr(
        6,
        4,
        "[2] Run A*"
    )

    stdscr.addstr(
        7,
        4,
        "[3] Generate Random Maze"
    )

    stdscr.addstr(
        8,
        4,
        "[4] Generate Guaranteed Maze"
    )

    stdscr.addstr(
        9,
        4,
        "[5] Reset Default Maze"
    )

    stdscr.addstr(
        11,
        4,
        "[Q] Quit"
    )

    stdscr.addstr(
        13,
        2,
        "Legend:"
    )

    stdscr.addstr(
        14,
        4,
        "O = Start"
    )

    stdscr.addstr(
        15,
        4,
        "X = End"
    )

    stdscr.addstr(
        16,
        4,
        "# = Wall"
    )

    stdscr.addstr(
        17,
        4,
        ". = Visited"
    )

    stdscr.addstr(
        18,
        4,
        "* = Final Path"
    )

    stdscr.refresh()

    return stdscr.getch()


# ============================================================
# MAIN PROGRAM
# ============================================================

def main(stdscr):

    setup_colors()

    maze = copy_maze(DEFAULT_MAZE)

    while True:

        choice = show_menu(stdscr)

        # ----------------------------------------------------
        # QUIT
        # ----------------------------------------------------

        if choice in (ord("q"), ord("Q")):
            break

        # ----------------------------------------------------
        # BFS
        # ----------------------------------------------------

        elif choice == ord("1"):

            path, explored = bfs(
                maze,
                stdscr
            )

            show_results(
                stdscr,
                "Breadth-First Search (BFS)",
                path,
                explored
            )

        # ----------------------------------------------------
        # A*
        # ----------------------------------------------------

        elif choice == ord("2"):

            path, explored = astar(
                maze,
                stdscr
            )

            show_results(
                stdscr,
                "A* Search",
                path,
                explored
            )

        # ----------------------------------------------------
        # RANDOM MAZE
        # ----------------------------------------------------

        elif choice == ord("3"):

            maze = generate_random_maze()

            stdscr.clear()

            draw_maze(
                maze,
                stdscr,
                algorithm="Random Maze"
            )

            stdscr.addstr(
                len(maze) + 3,
                0,
                "Random maze generated!"
            )

            stdscr.addstr(
                len(maze) + 4,
                0,
                "Press any key to return to the menu..."
            )

            stdscr.refresh()

            stdscr.getch()

        # ----------------------------------------------------
        # GUARANTEED MAZE
        # ----------------------------------------------------

        elif choice == ord("4"):

            maze = generate_open_maze()

            stdscr.clear()

            draw_maze(
                maze,
                stdscr,
                algorithm="Guaranteed Maze"
            )

            stdscr.addstr(
                len(maze) + 3,
                0,
                "Guaranteed maze generated!"
            )

            stdscr.addstr(
                len(maze) + 4,
                0,
                "Press any key to return to the menu..."
            )

            stdscr.refresh()

            stdscr.getch()

        # ----------------------------------------------------
        # RESET
        # ----------------------------------------------------

        elif choice == ord("5"):

            maze = copy_maze(DEFAULT_MAZE)

            stdscr.clear()

            stdscr.addstr(
                2,
                2,
                "Maze reset to default."
            )

            stdscr.addstr(
                4,
                2,
                "Press any key to continue..."
            )

            stdscr.refresh()

            stdscr.getch()


# ============================================================
# PROGRAM ENTRY POINT
# ============================================================

if __name__ == "__main__":
    curses.wrapper(main)
