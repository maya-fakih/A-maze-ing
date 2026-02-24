from typing import Any
from mazegen.generators.maze_generator import MazeGenerator
from project.parsing import parsing as helper
from project.colors import Colors
import sys
import os
import time


def clear_terminal() -> None:
    """Clear the terminal screen. Args: none. Returns: None."""
    os.system('cls' if os.name == 'nt' else 'clear')


def _config_path() -> str:
    """Resolve active configuration file path. Args: none. Returns: Config file path string."""
    if len(sys.argv) > 1 and sys.argv[1].endswith(".txt"):
        return f"configuration/{sys.argv[1]}"
    return "configuration/config.txt"


def update_config_value(file_path: str, key: str, new_value: str) -> None:
    """Set or append a key-value entry in config file. Args: file_path config file path, key setting name, new_value setting value. Returns: None."""
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
    """Prompt until a valid option is chosen. Args: prompt input message, options accepted values. Returns: Selected option in lowercase."""
    valid = {value.lower() for value in options}
    while True:
        value = input(prompt).strip().lower()
        if value in valid:
            return value
        print(f"Invalid choice. Available: {', '.join(options)}")


def _prompt_color(prompt: str, forbidden: str | None = None) -> str:
    """Prompt until a valid color is entered. Args: prompt input message, forbidden optional disallowed color. Returns: Selected color name."""
    while True:
        color = input(prompt).strip().lower()
        available_colors = Colors.get_available_colors()
        if color not in available_colors:
            print(f"Invalid color. Available: {', '.join(available_colors)}")
            continue
        if forbidden is not None and color == forbidden:
            print("Wall and flag color must be different.")
            continue
        return color


def _write_runtime_setting(maze_gen: MazeGenerator, key: str,
                           value: str) -> None:
    """Apply runtime setting and persist to config. Args: maze_gen active generator, key setting name, value setting value. Returns: None."""
    maze_gen.settings[key] = value
    setattr(maze_gen, key, value)
    update_config_value(_config_path(), key, value)


def _regenerate(maze_gen: MazeGenerator) -> None:
    """Regenerate maze and refresh output artifacts. Args: maze_gen active generator. Returns: None."""
    maze_gen.generate()
    maze_gen.output_to_file()
    maze_gen.write_path("configuration/gen_path.txt")


def _rebuild_generator(maze_gen: MazeGenerator,
                       updates: dict[str, str]) -> MazeGenerator:
    """Create a new generator with updated settings. Args: maze_gen current generator, updates setting overrides. Returns: Rebuilt maze generator instance."""
    settings = dict(maze_gen.settings)
    settings.update(updates)
    new_generator = MazeGenerator.create_generator(settings)
    _regenerate(new_generator)

    config = _config_path()
    for key, value in updates.items():
        update_config_value(config, key, value)
    return new_generator


def _print_corner(wall_code: str, reset_code: str) -> None:
    """Print one maze corner glyph. Args: wall_code wall ANSI code, reset_code ANSI reset code. Returns: None."""
    print(wall_code + "█" + reset_code, end="")


def _print_horizontal_wall(
    r: int,
    c: int,
    H: int,
    W: int,
    grid: list[list],
    wall_code: str,
    flag_code: str,
    reset_code: str,
    SOUTH: int,
    logo_cells: set,
) -> None:
    """Print one horizontal wall segment. Args: r render row, c render column, H maze height, W maze width, grid maze cells, wall_code wall ANSI code, flag_code flag ANSI code, reset_code ANSI reset code, SOUTH south-wall bitmask, logo_cells reserved logo cells. Returns: None."""
    if r == 0 or r == 2 * H:
        print(wall_code + "███" + reset_code, end="")
    else:
        cell_row = r // 2 - 1
        cell_col = c // 2
        cell_above = (cell_col, cell_row)
        cell_below = (cell_col, cell_row + 1)

        if cell_above in logo_cells and cell_below in logo_cells:
            print(flag_code + "███" + reset_code, end="")
        elif grid[cell_col][cell_row] & SOUTH:
            print(wall_code + "███" + reset_code, end="")
        else:
            print("   ", end="")


def _print_vertical_wall(
    r: int,
    c: int,
    W: int,
    grid: list[list],
    wall_code: str,
    flag_code: str,
    reset_code: str,
    EAST: int,
    logo_cells: set,
) -> None:
    """Print one vertical wall segment. Args: r render row, c render column, W maze width, grid maze cells, wall_code wall ANSI code, flag_code flag ANSI code, reset_code ANSI reset code, EAST east-wall bitmask, logo_cells reserved logo cells. Returns: None."""
    if c == 0 or c == 2 * W:
        print(wall_code + "█" + reset_code, end="")
    else:
        cell_row = r // 2
        cell_col = c // 2 - 1
        cell_left = (cell_col, cell_row)
        cell_right = (cell_col + 1, cell_row)

        if cell_left in logo_cells and cell_right in logo_cells:
            print(flag_code + "█" + reset_code, end="")
        elif grid[cell_col][cell_row] & EAST:
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
    fill: bool,
    wall_code: str,
    visited: Any
) -> None:
    """Print one cell interior with markers and colors. Args: r render row, c render column, logo_cells reserved logo cells, solution_cells solved path cells, path show-path flag, flag_code flag ANSI code, reset_code ANSI reset code, path_code path ANSI code, entry entry cell, exit exit cell, fill fill-unknown flag, wall_code wall ANSI code, visited visited cells. Returns: None."""
    cell_row = r // 2
    cell_col = c // 2
    if fill is True and not (cell_col, cell_row) in visited:
        print(wall_code + "███" + reset_code, end="")
    elif (path is True) and ((cell_col, cell_row) in solution_cells):
        print(path_code + " ★ " + reset_code, end="")
    elif (cell_col, cell_row) in logo_cells:
        print(flag_code + "███" + reset_code, end="")
    elif (cell_col, cell_row) == entry:
        print(flag_code + " E " + reset_code, end="")
    elif (cell_col, cell_row) == exit:
        print(flag_code + " X " + reset_code, end="")
    else:
        print("   ", end="")


def show_options(maze_gen: MazeGenerator, path: bool, s: list) -> None:
    """Display interactive menu and handle commands. Args: maze_gen active generator, path whether path is visible, s solved cell list. Returns: None."""
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
        print("9. Animate generation algorithm")
        print("10. Quit")
        choice = int(input("Choice? (1-10): "))
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
                maze_gen = _safe_rebuild(maze_gen, {"shape": shape}, path, s)
            case 7:
                generation_algorithm = _prompt_choice(
                    "Enter a generation algorithm "
                    f"({', '.join(helper.generation_algorithms)}): ",
                    helper.generation_algorithms,
                )
                maze_gen = _safe_rebuild(
                    maze_gen,
                    {"generation_algorithm": generation_algorithm},
                    path, s
                )
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
                animate_generation(maze_gen, path, s)
                display_terminal(maze_gen, path)
            case 10:
                sys.exit()
            case _:
                print("Error! Invalid choice.")
                show_options(maze_gen, path, s)
    except ValueError:
        print("Error! Invalid choice.")
        show_options(maze_gen, path, s)


def _safe_rebuild(maze_gen: MazeGenerator, updates: dict[str, str],
                  path: bool, s: list) -> MazeGenerator:
    """Rebuild generator with guarded error handling. Args: maze_gen current generator, updates setting overrides, path current path-visibility flag, s solved cell list. Returns: Generator to continue displaying."""
    try:
        new_generator = _rebuild_generator(maze_gen, updates)
        clear_terminal()
        display_terminal(new_generator, path)
        return new_generator
    except Exception as e:
        print(f"\nError: {e}")
        input("Press Enter to continue...")
        clear_terminal()
        display_terminal(maze_gen, path)
        return maze_gen


def draw_maze(maze_gen: MazeGenerator, path: bool, s: list, f: bool) -> None:
    """Render maze grid in terminal. Args: maze_gen generator to render, path show-path flag, s solved cell list, f fill-unvisited flag. Returns: None."""
    H = maze_gen.height
    W = maze_gen.width
    EAST = 2
    SOUTH = 4
    grid = maze_gen.maze
    logo_cells = maze_gen.logo_cells
    entry = maze_gen.entry
    exit = maze_gen.exit
    visited = maze_gen.visited
    solution_set = set(s) if s else set()

    wall_code = Colors.get_ansi_escape(maze_gen.wall_color)
    flag_code = Colors.get_ansi_escape(maze_gen.flag_color)
    reset_code = Colors.get_reset_escape()

    explicit_path_color = getattr(maze_gen, "path_color", None)
    if explicit_path_color and Colors.is_valid_color(explicit_path_color):
        path_code = Colors.get_ansi_escape(explicit_path_color)
    else:
        path_code = Colors.get_complementary_escape(maze_gen.wall_color)

    for r in range(2 * H + 1):
        for c in range(2 * W + 1):
            if r % 2 == 0 and c % 2 == 0:
                _print_corner(wall_code, reset_code)
            elif r % 2 == 0 and c % 2 == 1:
                _print_horizontal_wall(
                    r, c, H, W, grid, wall_code, flag_code, reset_code, SOUTH,
                    logo_cells
                )
            elif r % 2 == 1 and c % 2 == 0:
                _print_vertical_wall(
                    r, c, W, grid, wall_code, flag_code, reset_code,
                    EAST, logo_cells
                )
            else:
                _print_cell_interior(
                    r, c, logo_cells, solution_set,
                    path, flag_code, reset_code, path_code,
                    entry, exit, f, wall_code, visited
                )
        print()


def animate_generation(m: MazeGenerator, path: bool, s: list) -> None:
    """Animate maze generation over recorded steps. Args: m maze generator to animate, path show-path flag, s solved cell list. Returns: None."""
    animation = m.generation_path
    m.visited.clear()
    m.reset_maze()
    fill = True
    for cell, value, _ in animation:
        x, y = cell
        m.maze[x][y] = value
        m.visited.add((x, y))
        draw_maze(m, path, s, fill)
        time.sleep(0.02)
        clear_terminal()
    fill = False


def animate_solver(m: MazeGenerator, path: bool, s: list) -> None:
    """Animate solver progression in terminal view. Args: m maze generator to animate, path show-path flag, s solved cell list. Returns: None."""
    pass


def display_terminal(maze_gen: MazeGenerator, path: bool) -> None:
    """Render maze grid in terminal. Args: maze_gen generator to render, path show-path flag, s solved cell list, f fill-unvisited flag. Returns: None."""
    solution_cells = [
        cell for cell, _, sol in maze_gen.generation_path if sol
    ]
    draw_maze(maze_gen, path, solution_cells, False)
    show_options(maze_gen, path, solution_cells)
