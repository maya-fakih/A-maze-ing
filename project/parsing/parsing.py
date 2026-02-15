import webcolors
import io


# customized exception class for parsing errors
class ParsingError(Exception):
    def __init__(self, msg: str):
        self.msg = msg

    def __str__(self):
        return self.msg


mandatory_keys = ["width", "height", "entry", "exit"]
optional_keys = ["output_file", "perfect",
                 "wall_color", "flag_color", "solver_algorithm",
                 "shape", "generation_algorithm"]
generation_algorithms = ["prim", "dfs", "bfs", "huntkill"]
solver_algorithms = ["dfs", "bfs", "a*", "ucs"]
shapes = ["star", "heart", "square", "flower"]

#   Validate color name and ensure it is not black


def validate_color_name(name: str) -> bool:
    try:
        # Normalizes input and checks against CSS3 defined names
        webcolors.name_to_hex(name.lower())
        if (name == "black"):
            return False
        return True
    except ValueError:
        return False

# checks that all mandatory flags are present


def mandatory_flags_check(input_settings: dict):
    # determine which required keys are missing from the parsed settings
    missing = [k for k in mandatory_keys if k not in input_settings]
    if missing:
        valid = ", ".join(mandatory_keys)
        extra = ", ".join(optional_keys)
        raise ParsingError(
            "Error in file settings!\n"
            f"Missing mandatory settings: {', '.join(missing)}.\n"
            f"Required settings: {valid}.\n"
            f"Optional settings: {extra}."
        )

# validate values and convert to needed type


def validate_types(input_settings: dict) -> dict:
    for key, value in input_settings.items():
        if key == "height" or key == "width":
            d = {key: int(value)}
            input_settings.update(d)
        elif key == "perfect":
            if value == "true" or value == "false":
                d = {key: bool(value.capitalize())}
                input_settings.update(d)
            else:
                raise ParsingError("Invalid value for perfect setting\n"
                                   "Make sure the value is set to either "
                                   "true or false.")
        elif key == "generation_algorithm":
            if value not in generation_algorithms:
                valid = ", ".join(generation_algorithms)
                raise ParsingError(f"Invalid maze generation algorithm!\n"
                                   f"Supported algorithms: {valid}.")
        elif key == "solver_algorithm":
            if value not in solver_algorithms:
                valid = ", ".join(solver_algorithms)
                raise ParsingError(f"Invalid maze solver algorithm!\n"
                                   f"Supported algorithms: {valid}.")
        elif key == "shape":
            if value not in shapes:
                valid = ", ".join(shapes)
                raise ParsingError(f"Invalid shape!\n"
                                   f"Suuported shapes: {valid}.")
        elif key == "wall_color" or key == "flag_color":
            if (not validate_color_name(value)):
                raise ParsingError("Invalid color name!\n"
                                   "Enter an existing color name.")
        elif key == "output_file":
            if not value.endswith(".txt"):
                raise ParsingError("Error in output file format!\n"
                                   "Make sure your output file has a "
                                   ".txt extension.")
        elif key == "entry" or key == "exit":
            array = value.strip().split(",", 1)
            if len(array) != 2:
                raise ParsingError(
                    "Error in entry or exit coordinates!\n"
                    "Make sure you pass two coordinates separated by comma."
                )
            array[0] = int(array[0])
            array[1] = int(array[1])
            d = {key: tuple(array)}
            input_settings.update(d)
    return (input_settings)


# check that all keys are valid
def parse_settings(file: io.TextIOWrapper) -> dict:
    input_settings: dict = {}
    for line in file:
        line = line.strip().lower()
        if (not line or line.startswith("#")):
            continue
        array = line.split("=", 1)
        if len(array) != 2:
            raise ParsingError(
                "Error in file settings!\n"
                "Invalid line (missing '=')."
            )
        key = array[0].strip()
        val = array[1].strip()
        if (key not in mandatory_keys) and (key not in optional_keys):
            valid = ", ".join(mandatory_keys)
            raise ParsingError(
                "Error in file settings!\n"
                "No such configuration option.\n"
                f"Valid settings: {valid}."
            )
        d = {key: val}
        input_settings.update(d)
    # check that all madatory keys exists in input_settings keys
    mandatory_flags_check(input_settings)
    settings_dict = validate_types(input_settings)
    return (settings_dict)
