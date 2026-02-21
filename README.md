*This project has been created as part of the 42 curriculum by aabi-mou, mfakih*

# Description

`A-maze-ing` is a maze generator + solver project with two display modes:

- Python ASCII display (interactive menu in terminal)
- C MiniLibX display (interactive button panel)

The program reads a config file, generates a maze, solves it, writes outputs to disk, then displays the result.

Core features:

- Multiple generation algorithms (`dfs`, `bfs`, `prim`, `huntkill`)
- Multiple solver algorithms (`dfs`, `bfs`, `a*`, `ucs`)
- Shape support (`square`, `heart`, `flower`, `star`)
- Optional perfect / non-perfect maze generation
- Color customization for wall, flag, and path
- Runtime interactive controls in both display modes

# Instructions

## 1. Prerequisites

- Python 3.10+ (project tested with Python 3.12 in local setup)
- GCC / make
- X11 development libraries (for MiniLibX mode on Linux)

## 2. Project setup

```bash
git clone git@vogsphere.42beirut.com:vogsphere/intra-uuid-a96ca7bd-39f8-463b-b5ac-20628b80fe8c-7216753-aabi-mou
cd A-maze-ing
```

Optional virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install Python dependency:

```bash
pip install webcolors
```

## 3. Build MiniLibX display executable

```bash
make
```

This builds:

- MiniLibX static library
- `project/maze_displayer/minilibx_display/main.exe`

## 4. Run

```bash
python3 a_maze_ing.py config.txt
```

Config file is expected in:

- `configuration/config.txt`

## 5. Display modes

- `DISPLAY_MODE=ascii`
  - Terminal output with interactive menu:
    - regenerate maze
    - toggle path
    - change wall/flag/path color
    - change shape
    - change generation/solver algorithm

- `DISPLAY_MODE=minilibx`
  - Graphical window with animation + button panel
  - Buttons update config and regenerate automatically

# Resources

General references used during design and learning:
- put references here

# Config file / additional features

Mandatory keys:

- `WIDTH`
- `HEIGHT`
- `ENTRY`
- `EXIT`

Optional keys:

- `OUTPUT_FILE` (must end with `.txt`)
- `PERFECT` (`true` / `false`)
- `SHAPE` (`square`, `heart`, `flower`, `star`)
- `GENERATION_ALGORITHM` (`dfs`, `bfs`, `prim`, `huntkill`)
- `SOLVER_ALGORITHM` (`dfs`, `bfs`, `a*`, `ucs`)
- `DISPLAY_MODE` (`ascii`, `minilibx`)
- `WALL_COLOR`
- `FLAG_COLOR`
- `PATH_COLOR`

Example (`configuration/config.txt`):

```ini
WIDTH=35
HEIGHT=35
ENTRY=6,10
EXIT=29,16
OUTPUT_FILE=maze.txt
PERFECT=true
SHAPE=heart
GENERATION_ALGORITHM=bfs
SOLVER_ALGORITHM=dfs
DISPLAY_MODE=minilibx
WALL_COLOR=light_blue
FLAG_COLOR=light_magenta
PATH_COLOR=grey
```

Notes:

- `ENTRY` / `EXIT` format is `x,y`
- Wall and flag colors are validated to avoid identical values

# Maze generation algorithms
---

## 1. DFS Generator (Depth-First Search / backtracking style)

Type: Stack-based traversal.

How it works:

- starts from entry
- carves into unvisited neighbors using randomized order
- continues until all reachable cells are processed

Texture:

- long corridors
- many dead ends

## 2. BFS Generator (Breadth-First style carving)

Type: Queue-based traversal.

How it works:

- starts from entry
- expands layer-by-layer through randomized neighbor ordering
- carves edges when visiting new cells

Texture:

- more even spread
- different branching pattern than DFS

## 3. Randomized Prim Generator

Type: Frontier-based randomized Prim variant.

How it works:

- keeps a frontier list
- picks random frontier edges
- carves only when target cell is unvisited

Texture:

- organic branching and balanced spread

## 4. Hunt-and-Kill Generator

Type: Hybrid walk + hunt strategy.

How it works:

- performs random walk carving
- when stuck, hunts next valid frontier candidate
- repeats until completion

Texture:

- mixed corridor lengths and branching patterns

## Perfect vs non-perfect mazes

- `PERFECT=true`: keep tree-like structure (single path between cells)
- `PERFECT=false`: adds extra loops after generation

# Reusable parts

Main reusable components in this repo:

- `project/parsing/parsing.py`
  - config parser and validation
- `mazegen/generators/`
  - generator abstraction + algorithms
- `mazegen/solvers/`
  - solver abstraction + algorithms
- `project/maze_displayer/ascii_display/ascii_display.py`
  - terminal renderer and runtime menu
- `project/maze_displayer/minilibx_display/`
  - C renderer and runtime button controls

Output contracts:

- Maze output file in `output/*.txt`
- Generation path file in `configuration/gen_path.txt`

# Roles

Team collaboration covered:

- architecture and planning
- generator / solver implementation
- parsing and validation
- ASCII interaction design
- MiniLibX graphical interface and animation
- testing, debugging, and integration

