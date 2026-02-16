from mazegen.generators.maze_generator import MazeGenerator
import sys
import os

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


def clear_terminal() -> None:
    os.system('cls' if os.name == 'nt' else 'clear')


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
    solution_cells: set,
    path: bool,
    flag_code: str,
    reset_code: str,
    entry: tuple,
    exit: tuple,
):
    cell_row = r // 2
    cell_col = c // 2
    if (path is True) and ((cell_col, cell_row) in solution_cells):
        print(" ★ ", end="")
    elif (cell_col, cell_row) in logo_cells:
        print(flag_code + "███" + reset_code, end="")
    elif (cell_col, cell_row) == entry:
        print(flag_code + " E " + reset_code, end="")
    elif (cell_col, cell_row) == exit:
        print(flag_code + " X " + reset_code, end="")
    else:
        print("   ", end="")


def show_options(maze_gen: MazeGenerator, path: bool) -> None:
    try:
        print("\n=== A-MAZE-ING ===")
        print("1. Re-generate a new maze")
        print("2. Show/Hide path from entry to exit")
        print("3. Rotate maze colors")
        print("4. Rotate flag color")
        print("5. Quit")
        choice = int(input("Choice? (1-5): "))
        match choice:
            case 1:
                # code that re-generates the maze
                maze_gen.generate()
                maze_gen.output_to_file()
                clear_terminal()
                display_terminal(maze_gen, path)
            case 2:
                # code that shows/hides path from entry to exit
                # initially it is hidden, then we make it visible
                if path is True:
                    clear_terminal()
                    display_terminal(maze_gen, False)
                else:
                    clear_terminal()
                    display_terminal(maze_gen, True)
            case 3:
                # rotate colors
                # ask user for new wall color
                color = "hi"
                while (color not in color_map.keys()):
                    color = input("Enter a valid wall color: ")
                else:
                    clear_terminal()
                    maze_gen.wall_color = color
                    display_terminal(maze_gen, path)
            case 4:
                # change flag color
                color = "hi"
                while (color not in color_map.keys()):
                    color = input("Enter a valid flag color: ")
                else:
                    clear_terminal()
                    maze_gen.flag_color = color
                    display_terminal(maze_gen, path)
            case 5:
                sys.exit()
    except ValueError:
        print("Error! Invalid choice.")
        sys.exit()


def display_terminal(maze_gen: MazeGenerator, path: bool):
    # if path is true show emoji on self.path values
    H = maze_gen.height
    W = maze_gen.width
    EAST = 2
    SOUTH = 4
    grid = maze_gen.maze
    logo_cells = maze_gen.logo_cells
    entry = maze_gen.entry
    exit = maze_gen.exit

    # Extract solution cells from path
    solution_cells = {cell for cell, _,
                      is_solution in maze_gen.path if is_solution}

    # default white
    wall_code = f"\033[{color_map.get(maze_gen.wall_color, 37)}m"
    flag_code = f"\033[{color_map.get(maze_gen.flag_color, 34)}m"
    # solution_code = f"\033[{color_map.get(
    #     getattr(maze_gen, 'solution_color', 'white'), 32)}m"
    reset_code = "\033[0m"

    for r in range(2 * H + 1):
        for c in range(2 * W + 1):
            if r % 2 == 0 and c % 2 == 0:
                _print_corner(wall_code, reset_code)
            elif r % 2 == 0 and c % 2 == 1:
                _print_horizontal_wall(
                    r, c, H, W, grid, wall_code, reset_code, SOUTH)
            elif r % 2 == 1 and c % 2 == 0:
                _print_vertical_wall(
                    r, c, W, grid, wall_code, reset_code, EAST)
            else:
                _print_cell_interior(r, c, logo_cells, solution_cells,
                                     path, flag_code, reset_code,
                                     entry, exit)

        print()
    show_options(maze_gen, path)
