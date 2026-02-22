# MiniLibX Renderer (A to Z)

This folder contains the C-based graphical renderer for the maze project, built on MiniLibX.
It loads files produced by the Python side, opens a window, animates maze generation, and provides runtime controls through a side panel.

## A. At a Glance

- Renders maze in a window (`MiniLibX`).
- Animates generation from `configuration/maze_gen.txt`.
- Displays logo cells, entry/exit, and optional solution path.
- Provides clickable buttons to regenerate and cycle settings.
- Reads/writes settings in `configuration/<config>.txt`.

## B. Build and Run

From repository root:

```bash
make
python3 a_maze_ing.py config.txt
```

When `DISPLAY_MODE=minilibx`, Python launches:

```bash
project/maze_displayer/minilibx_display/main.exe <config.txt> maze_gen.txt <output file> logo.txt
```

## C. Folder Contents

- `main.c`: program entrypoint, file opening, app initialization, event loop start.
- `mlx_parser.c`: parse config, maze output, generation path, logo cells.
- `mlx_display.c`: rendering, animation, button UI, regeneration logic, config updates.
- `mlx_helper_1.c`: shared helpers (`error`, `trim`).
- `mlx_helper_2.c`: parsing helpers (`is_comment_line`, `find_value`, `parse_line`, `fill_grid`, `parse_coordinates`).
- `mlx_helper.h`: structs, constants, function prototypes.

## D. Input Files and Contracts

The executable expects 4 arguments:

1. `config filename` (inside `configuration/`)
2. `generation path filename` (inside `configuration/`, now `maze_gen.txt`)
3. `maze output path` (full/relative path like `output/output_maze.txt`)
4. `logo filename` (inside `configuration/`)

### 1. Config file

Parsed keys include:
- `width`, `height`
- `shape`
- `wall_color`, `flag_color`, `path_color`
- `generation_algorithm`, `solver_algorithm`

Defaults are set in `set_default_config()` in `mlx_parser.c`.

### 2. Maze output file

Expected layout:
- `height` grid lines, each containing hex wall cells (`0`..`F`)
- blank line
- `entry` line: `x,y`
- `exit` line: `x,y`
- solution directions line (`NSEW...`)

### 3. Generation file (`maze_gen.txt`)

Each line is parsed by `parse_line()` as:

```text
x y value is_solution
```

- `x y`: cell coordinates
- `value`: cell wall mask (int representation of hex bit mask)
- `is_solution`: `True` / `False`

### 4. Logo file

Each line: `x y`

## E. Core Data Structures

From `mlx_helper.h`:

- `t_point`: integer coordinates.
- `t_cell`: generation-step record (`point`, `value`, `is_sol`).
- `t_config`: runtime render/config settings.
- `t_maze`: parsed maze state (grid, entry, exit, solution, generation list, logo cells).
- `t_app`: global runtime state (config + maze + mlx handles + animation state + file paths).
- `t_button`: button geometry and label.

## F. Startup Flow

1. `main()` validates args and opens files.
2. `init_app()`:
   - parses settings (`parse_settings`)
   - parses generation list (`parse_path`)
   - parses logo list (`parse_logo_cells`)
   - parses output maze (`parse_output`)
   - initializes animation state: `phase=0`, `anim_index=0`, `frame=0`
3. `draw_maze()`:
   - calls `init_graphics()`
   - starts first generation step with `animate_generation()`
   - installs hooks (`mlx_loop_hook`, `mlx_mouse_hook`, close-window hook)
   - enters `mlx_loop()`

## G. Rendering Model

The renderer draws into an off-screen image (`t_img`) and then blits it to the window.

Key drawing utilities:
- `put_pixel()`
- `fill_rect()`
- `draw_square()`
- `draw_cell_by_bits()` (draws walls by bitmask)
- `draw_star_marker()` (used for path markers and generation star overlays)

Color conversion is centralized in `color_from_name()`.

## H. Animation Phases

Current phase usage:

- `phase == 0`: generation animation
- `phase == 2`: steady/final render

Generation flow (`animate_generation()`):

1. On first frame, `draw_generation_base()` paints all cells as closed (`0xF`) + logo cells.
2. For each step in `maze.gen_path`:
   - draw cell with recorded `cell.value`
   - draw star marker in `wall_color` on explored cell (animation-only)
3. When steps are exhausted:
   - switch to `phase=2`
   - redraw final scene via `redraw_base_scene()` (star overlay disappears)

Update loop (`update()`):
- increments `frame`
- every `animation_speed` ticks, advances generation if `phase==0`
- blits image + draws right-side panel

## I. Static Scene and Path

`redraw_base_scene()`:
- calls `draw_static_maze()`
- optionally overlays solution stars if `show_path` is enabled

`draw_static_maze()`:
- decodes each hex grid character and draws matching wall pattern
- paints logo cells in `flag_color` (with conflict-safe fallback)

`draw_solution_until()`:
- starts at entry
- follows solution string (`N/S/E/W`)
- paints star markers with `path_color`

## J. Button Panel and Runtime Controls

Buttons are created by `build_buttons()` and handled by `mouse_hook()` + `on_button_click()`.

Actions:
- Regenerate maze
- Show/hide solution path
- Cycle wall color
- Cycle flag color
- Cycle path color
- Cycle shape
- Cycle generation algorithm
- Cycle solver algorithm

Panel also prints current settings (wall/flag/path/shape/gen/solver).

## K. Regeneration Path

`regenerate_maze()` in `mlx_display.c`:

1. Runs Python headless:
   - `AMAZE_NO_DISPLAY=1 DISPLAY= python3 a_maze_ing.py <config>`
2. Reloads all files with `reload_from_files()`
3. Resets animation state (`phase=0`, `anim_index=0`, `frame=0`)
4. Restarts generation animation immediately

## L. Config File Mutation

`update_config_value()` edits `configuration/<config>.txt` by:
- rewriting to temp file
- replacing/adding target key
- renaming temp file back

Used by button actions when cycling values.

## M. Memory and Cleanup

`free_maze()` frees:
- `maze.grid`
- `maze.solution`
- `maze.gen_path`
- `maze.logo_cells`

`reload_from_files()` frees previous dynamic config strings and maze allocations before swapping new state in.

## N. Color Rules

- Wall and flag colors are forced to be distinct (both on parse and runtime safety path).
- White wall/flag are rejected for MiniLibX parsing.
- Named aliases like `gray/grey`, `light_*`, `bright_*` are supported in `color_from_name()`.

## O. Window/Layout

`init_graphics()` computes:
- maze pixel area: `maze.width * cell_size`, `maze.height * cell_size`
- fixed side panel width: `360`
- minimum window height: `640`

Window is centered via X11 internals in `center_window()`.

## P. Error Handling

Fatal parse/open/setup errors call `error()` (prints message and exits).
Input validation failures are generally detected early in `main.c` / parser layer.

## Q. Known Constraints

- Drawing assumes grid chars are uppercase hex (`0`..`F`).
- `animation_speed` currently comes from defaults (not read from config key).
- `animate_solution()` exists but generation->final flow currently jumps directly to phase 2 final render.

## R. Typical Dev Workflow

1. Edit C files in this folder.
2. Rebuild:
   ```bash
   make
   ```
3. Run:
   ```bash
   python3 a_maze_ing.py config.txt
   ```
4. Click panel actions to verify runtime behavior.

## S. Function Map (Quick Index)

- Setup: `main`, `init_app`, `copy_runtime_paths`, `init_graphics`
- Parsing: `parse_settings`, `parse_output`, `parse_path`, `parse_logo_cells`
- Rendering: `draw_static_maze`, `draw_cell_by_bits`, `draw_star_marker`
- Animation: `animate_generation`, `update`, `draw_generation_base`
- UI: `draw_button_panel`, `mouse_hook`, `on_button_click`
- Regeneration: `regenerate_maze`, `reload_from_files`

## T. Troubleshooting

- "Error opening ... file":
  check filenames passed from Python and ensure files exist under `configuration/` and `output/`.
- Empty or broken maze render:
  verify output file format (grid + blank line + entry + exit + solution).
- No generation animation:
  confirm `maze_gen.txt` is generated and non-empty.
- Colors look wrong:
  verify `wall_color`, `flag_color`, `path_color` values map in `color_from_name()`.

## U. Summary

This renderer is a file-driven MiniLibX visualization layer:
- Python generates maze artifacts.
- C parser loads artifacts into runtime structs.
- MLX draws a pixel-buffer view + control panel.
- Generation playback is now sourced from `maze_gen.txt`.
- UI controls can mutate config and trigger full regenerate/reload cycles.
