import sys
import os
import subprocess
from project.parsing import parsing as helper
from mazegen.errors import InitializationError
from mazegen.generators.maze_generator import MazeGenerator
from project.maze_displayer.ascii_display.ascii_display import display_terminal


def parse_input(argv: list[str]) -> dict:
    # validate number of arguments: script + config file
    if len(argv) != 2:
        raise helper.ParsingError("Invalid arguments "
                                  "given to program!\n"
                                  "Usage: python3 a_maze_ing.py"
                                  " config.txt")
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


# def clear_terminal() -> None:
#     os.system('cls' if os.name == 'nt' else 'clear')


def display_maze(maze_gen: MazeGenerator) -> None:
    match maze_gen.display_mode:
        case "ascii":
            print("=== A-MAZE-ING ===\n")
            display_terminal(maze_gen, False)
        case "minilibx":
            # Run compiled C MiniLibX program
            # give it the config and output file
            try:
                subprocess.run(["project/maze_displayer/minilibx_display/main.exe",
                                f"{sys.argv[1]}",
                                "gen_path.txt",
                                f"{maze_gen.output_file}",
                                "logo.txt"],
                               check=True)
            except FileNotFoundError:
                print("Error! Minilibx program not found.")
            except subprocess.CalledProcessError:
                print("Error! Minilibx program execution failed.")


if __name__ == "__main__":
    try:
        # parse configuration file, error message / dict
        # contaning key=settings and values
        settings = parse_input(sys.argv)
        # print(settings)
        # create the correct instance of the maze
        # generator class
        maze_generator = MazeGenerator.create_generator(settings)
        # generate the maze
        maze_generator.generate()
        # solve the maze
        maze_generator.output_to_file()
        maze_generator.write_path("configuration/gen_path.txt")
        if maze_generator.display_mode == "minilibx":
            maze_generator.write_logo_cells("configuration/logo.txt")
        display_maze(maze_generator)
        # # display options function
        # if os.environ.get("AMAZE_NO_DISPLAY") != "1":
        #     display_maze(maze_generator)
    except helper.ParsingError as e:
        print(e)
    except FileNotFoundError:
        print("Config file not found!\n"
              "Remember to add config.txt file for maze generation settings.")
    except ValueError:
        print("Error in settings value type!\n"
              "Make sure value of your settings are valid.")
    except InitializationError as e:
        print(e)
 