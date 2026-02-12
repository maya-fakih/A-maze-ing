from project.parsing import parsing as helper
import sys
from mazegen import MazeGenerator

if __name__ == "__main__":
    try:
        # validate number of arguments: only script name and config text file
        if (len(sys.argv) != 2):
            raise helper.ParsingError("Invalid arguments "
                                      "given to program!\n"
                                      "Usage: python3 a_maze_ing.py"
                                      "config.txt")
        # make sure file name provided is a text file
        if not sys.argv[1].endswith(".txt"):
            raise helper.ParsingError("Invalid file type given to program!\n"
                                      "Config file must be a text file.")
        # open config file and parse settings
        path_name = f"configuration/{sys.argv[1]}"
        config_file = open(path_name, "r")
        settings_dict = helper.parse_settings(config_file)
        config_file.close()
        print(settings_dict)
        # IMPORTANT NOTE FOR AGNESS!!!!
        # we have to add a function that creates the correct maze class based
        # on the flags
        # so if perfect use the class PerfectGenerator....
        maze_generator = MazeGenerator(settings_dict)
        # maze_generator.generate()
        # maze_generator.write_to_file(settings_dict.get('output_file'))
    except helper.ParsingError as e:
        print(e)
    except FileNotFoundError:
        print("Config file not found!\n"
              "Remember to add config.txt file for maze generation settings.")
    except ValueError:
        print("Error in settings value type!\n"
              "Make sure value of your settings are valid.")
