from mazegen.generators.maze_generator import MazeGenerator

color_map = {
    "black": 30,
    "red": 31,
    "green": 32,
    "yellow": 33,
    "blue": 34,
    "magenta": 35,
    "cyan": 36,
    "white": 37,
    "bright_black": 90,
    "bright_red": 91,
    "bright_green": 92,
    "bright_yellow": 93,
    "bright_blue": 94,
    "bright_magenta": 95,
    "bright_cyan": 96,
    "bright_white": 97,
    "grey": 90,
    "gray": 90,
    "light_red": 91,
    "light_green": 92,
    "light_yellow": 93,
    "light_blue": 94,
    "light_magenta": 95,
    "light_cyan": 96,
    "light_white": 97,
}


def _print_corner(wall_code: str, reset_code: str):
    print(wall_code + "█" + reset_code, end="")


def _print_horizontal_wall(
    r: int,
    c: int,
    H: int,
    W: int,
    grid: list[list],
    wall_code: str,
    reset_code: str,
    SOUTH: int,
):
    if r == 0 or r == 2 * H:
        print(wall_code + "███" + reset_code, end="")
    else:
        cell_row = r // 2 - 1
        cell_col = c // 2
        if grid[cell_col][cell_row] & SOUTH:
            print(wall_code + "███" + reset_code, end="")
        else:
            print("   ", end="")


def _print_vertical_wall(
    r: int,
    c: int,
    W: int,
    grid: list[list],
    wall_code: str,
    reset_code: str,
    EAST: int,
):
    if c == 0 or c == 2 * W:
        print(wall_code + "█" + reset_code, end="")
    else:
        cell_row = r // 2
        cell_col = c // 2 - 1
        if grid[cell_col][cell_row] & EAST:
            print(wall_code + "█" + reset_code, end="")
        else:
            print(" ", end="")


def _print_cell_interior(
    r: int,
    c: int,
    logo_cells: set,
    flag_code: str,
    reset_code: str,
    entry: tuple,
    exit: tuple,
):
    cell_row = r // 2
    cell_col = c // 2
    if (cell_col, cell_row) in logo_cells:
        print(flag_code + "███" + reset_code, end="")
    elif (cell_col, cell_row) == entry:
        print(flag_code + " S " + reset_code, end="")
    elif (cell_col, cell_row) == exit:
        print(flag_code + " E " + reset_code, end="")
    else:
        print("   ", end="")


def display_gen(maze: MazeGenerator):
    H = maze.height
    W = maze.width
    EAST = 2
    SOUTH = 4
    grid = maze.maze
    logo_cells = maze.logo_cells
    entry = maze.entry
    exit = maze.exit

    # default white
    wall_code = f"\033[{color_map.get(maze.wall_color, 37)}m"
    flag_code = f"\033[{color_map.get(maze.flag_color, 34)}m"
    reset_code = "\033[0m"

    for r in range(2 * H + 1):
        for c in range(2 * W + 1):
            # Corners
            if r % 2 == 0 and c % 2 == 0:
                _print_corner(wall_code, reset_code)
            # Horizontal walls
            elif r % 2 == 0 and c % 2 == 1:
                _print_horizontal_wall(
                    r, c, H, W, grid, wall_code, reset_code, SOUTH)
            # Vertical walls
            elif r % 2 == 1 and c % 2 == 0:
                _print_vertical_wall(
                    r, c, W, grid, wall_code, reset_code, EAST)
            # Cell interior
            else:
                _print_cell_interior(r, c, logo_cells, flag_code, reset_code, entry, exit)

        print()
