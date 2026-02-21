from mazegen.generators.maze_generator import MazeGenerator
from project.parsing import parsing as helper
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


def _config_path() -> str:
    if len(sys.argv) > 1 and sys.argv[1].endswith(".txt"):
        return f"configuration/{sys.argv[1]}"
    return "configuration/config.txt"


def update_config_value(file_path: str, key: str, new_value: str) -> None:
    normalized_key = key.lower()
    found = False
    lines = []

    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            lines = file.readlines()

    with open(file_path, "w", encoding="utf-8") as file:
        for line in lines:
            stripped = line.strip()
            if (not stripped) or stripped.startswith("#") or "=" not in line:
                file.write(line)
                continue

            existing_key = line.split("=", 1)[0].strip().lower()
            if existing_key == normalized_key:
                file.write(f"{key.upper()}={new_value}\n")
                found = True
            else:
                file.write(line)

        if not found:
            file.write(f"{key.upper()}={new_value}\n")


def _prompt_choice(prompt: str, options: list[str]) -> str:
    valid = {value.lower() for value in options}
    while True:
        value = input(prompt).strip().lower()
        if value in valid:
            return value
        print(f"Invalid choice. Available: {', '.join(options)}")


def _prompt_color(prompt: str, forbidden: str | None = None) -> str:
    while True:
        color = input(prompt).strip().lower()
        if color not in color_map:
            print(f"Invalid color. Available: {', '.join(color_map.keys())}")
            continue
        if forbidden is not None and color == forbidden:
            print("Wall and flag color must be different.")
            continue
        return color


def _write_runtime_setting(maze_gen: MazeGenerator, key: str,
                           value: str) -> None:
    maze_gen.settings[key] = value
    setattr(maze_gen, key, value)
    update_config_value(_config_path(), key, value)


def _regenerate(maze_gen: MazeGenerator) -> None:
    maze_gen.generate()
    maze_gen.output_to_file()
    maze_gen.write_path("configuration/gen_path.txt")


def _rebuild_generator(maze_gen: MazeGenerator,
                       updates: dict[str, str]) -> MazeGenerator:
    settings = dict(maze_gen.settings)
    settings.update(updates)
    new_generator = MazeGenerator.create_generator(settings)
    _regenerate(new_generator)

    config = _config_path()
    for key, value in updates.items():
        update_config_value(config, key, value)
    return new_generator


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
    path_code: str,
    entry: tuple,
    exit: tuple,
):
    cell_row = r // 2
    cell_col = c // 2
    if (path is True) and ((cell_col, cell_row) in solution_cells):
        print(path_code + " ★ " + reset_code, end="")
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
        print("3. Change wall color")
        print("4. Change flag color")
        print("5. Change path color")
        print("6. Change shape")
        print("7. Change generation algorithm")
        print("8. Change solver algorithm")
        print("9. Quit")
        choice = int(input("Choice? (1-9): "))
        match choice:
            case 1:
                _regenerate(maze_gen)
                clear_terminal()
                display_terminal(maze_gen, path)
            case 2:
                clear_terminal()
                display_terminal(maze_gen, not path)
            case 3:
                color = _prompt_color(
                    "Enter a valid wall color: ",
                    forbidden=maze_gen.flag_color
                )
                _write_runtime_setting(maze_gen, "wall_color", color)
                clear_terminal()
                display_terminal(maze_gen, path)
            case 4:
                color = _prompt_color(
                    "Enter a valid flag color: ",
                    forbidden=maze_gen.wall_color
                )
                _write_runtime_setting(maze_gen, "flag_color", color)
                clear_terminal()
                display_terminal(maze_gen, path)
            case 5:
                color = _prompt_color("Enter a valid path color: ")
                _write_runtime_setting(maze_gen, "path_color", color)
                clear_terminal()
                display_terminal(maze_gen, path)
            case 6:
                shape = _prompt_choice(
                    f"Enter a shape ({', '.join(helper.shapes)}): ",
                    helper.shapes,
                )
                maze_gen = _rebuild_generator(maze_gen, {"shape": shape})
                clear_terminal()
                display_terminal(maze_gen, path)
            case 7:
                generation_algorithm = _prompt_choice(
                    "Enter a generation algorithm "
                    f"({', '.join(helper.generation_algorithms)}): ",
                    helper.generation_algorithms,
                )
                maze_gen = _rebuild_generator(
                    maze_gen,
                    {"generation_algorithm": generation_algorithm}
                )
                clear_terminal()
                display_terminal(maze_gen, path)
            case 8:
                solver_algorithm = _prompt_choice(
                    "Enter a solver algorithm "
                    f"({', '.join(helper.solver_algorithms)}): ",
                    helper.solver_algorithms,
                )
                _write_runtime_setting(
                    maze_gen, "solver_algorithm", solver_algorithm)
                maze_gen.find_solution_path()
                maze_gen.output_to_file()
                maze_gen.write_path("configuration/gen_path.txt")
                clear_terminal()
                display_terminal(maze_gen, path)
            case 9:
                sys.exit()
            case _:
                print("Error! Invalid choice.")
                show_options(maze_gen, path)
    except ValueError:
        print("Error! Invalid choice.")
        show_options(maze_gen, path)


def display_terminal(maze_gen: MazeGenerator, path: bool):
    H = maze_gen.height
    W = maze_gen.width
    EAST = 2
    SOUTH = 4
    grid = maze_gen.maze
    logo_cells = maze_gen.logo_cells
    entry = maze_gen.entry
    exit = maze_gen.exit

    solution_cells = {
        cell for cell, _, is_solution in maze_gen.path if is_solution
    }

    wall_value = color_map.get(maze_gen.wall_color, 37)
    explicit_path_color = getattr(maze_gen, "path_color", None)
    if explicit_path_color and explicit_path_color in color_map:
        path_value = color_map[explicit_path_color]
    else:
        base_index = wall_value % 10
        opposite_index = (base_index + 4) % 8
        path_value = (90 if wall_value >= 90 else 30) + opposite_index

    wall_code = f"\033[{wall_value}m"
    path_code = f"\033[{path_value}m"
    flag_code = f"\033[{color_map.get(maze_gen.flag_color, 34)}m"
    reset_code = "\033[0m"

    for r in range(2 * H + 1):
        for c in range(2 * W + 1):
            if r % 2 == 0 and c % 2 == 0:
                _print_corner(wall_code, reset_code)
            elif r % 2 == 0 and c % 2 == 1:
                _print_horizontal_wall(
                    r, c, H, W, grid, wall_code, reset_code, SOUTH
                )
            elif r % 2 == 1 and c % 2 == 0:
                _print_vertical_wall(
                    r, c, W, grid, wall_code, reset_code, EAST
                )
            else:
                _print_cell_interior(
                    r, c, logo_cells, solution_cells,
                    path, flag_code, reset_code, path_code,
                    entry, exit
                )

        print()
    show_options(maze_gen, path)
