from project.parsing import parsing as helper
import sys
import os
from mazegen.generators.maze_generator import MazeGenerator
from project.maze_displayer.ascii_display import display_terminal
import subprocess


def parse_input(argv: list[str]) -> dict:
    # validate number of arguments: only script name and config text file
    if (len(argv) != 2):
        raise helper.ParsingError("Invalid arguments "
                                  "given to program!\n"
                                  "Usage: python3 a_maze_ing.py"
                                  "config.txt")
    # make sure file name provided is a text file
    if not argv[1].endswith(".txt"):
        raise helper.ParsingError("Invalid file type given to program!\n"
                                  "Config file must be a text file.")
    # open config file and parse settings
    path_name = f"configuration/{argv[1]}"
    config_file = open(path_name, "r")
    settings_dict = helper.parse_settings(config_file)
    config_file.close()
    return settings_dict


def clear_terminal() -> None:
    os.system('cls' if os.name == 'nt' else 'clear')


def display_maze(maze_gen: MazeGenerator) -> None:
    try:
        print("Maze display options:\n")
        print("1 - Display using terminal ascii render")
        print("2 - Display using MiniLibX library\n")
        option = int(input("Please enter your choice (1-2): "))
        match option:
            case 1:
                clear_terminal()
                display_terminal(maze_gen, False)
            case 2:
                clear_terminal()
                # Run compiled C MiniLibX program
                subprocess.run(["./mlx_display", f"{maze_gen.output_file}"])
            case _:
                raise helper.ParsingError("Invalid choice!")
    except helper.ParsingError:
        print("Invalid choice!")


if __name__ == "__main__":
    try:
        print("=== A-MAZE-ING ===\n")
        # parse configuration file, error message / dict
        # contaning key=settings and values
        settings = parse_input(sys.argv)
        # print(settings)
        # create the correct instance of the maze
        # generator class
        maze_generator = MazeGenerator.create_generator(settings)
        # generate the maze
        maze_generator.generate()
        maze_generator.output_to_file()
        # solve the maze
        # display options function
        display_maze(maze_generator)
    except helper.ParsingError as e:
        print(e)
    except FileNotFoundError:
        print("Config file not found!\n"
              "Remember to add config.txt file for maze generation settings.")
    except ValueError:
        print("Error in settings value type!\n"
              "Make sure value of your settings are valid.")
    except Exception as e:
        print(e)
