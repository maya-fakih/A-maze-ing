# mazegen

Reusable Python package for generating and solving mazes.

## Requirements

- Python 3.10+
- No external runtime dependencies (`dependencies = []` in `pyproject.toml`)

## Install

From the repository root:

```bash
pip install -e ./mazegen
```

## Basic usage

```python
from mazegen.generators.maze_generator import MazeGenerator

settings = {
    "width": 35,
    "height": 35,
    "entry": (1, 1),
    "exit": (33, 33),
    "generation_algorithm": "dfs",   # dfs | bfs | prim | huntkill
    "solver_algorithm": "a*",        # bfs | a* | ucs
    "shape": "square",               # square | heart | flower | star
    "perfect": True,
}

generator = MazeGenerator.create_generator(settings)
generator.generate()
```

## Custom parameters

You can pass behavior through the `settings` dictionary.

Required:

- `width`
- `height`
- `entry` as `(x, y)`
- `exit` as `(x, y)`

Common optional parameters:

- `generation_algorithm`: `dfs`, `bfs`, `prim`, `huntkill`
- `solver_algorithm`: `bfs`, `a*`, `ucs`
- `shape`: `square`, `heart`, `flower`, `star`
- `perfect`: `True`/`False`
- `output_file`, `display_mode`, `wall_color`, `flag_color`, `path_color`

Note: seed-based deterministic generation is not currently exposed as a package setting.

## Access generated maze and solution

After `generator.generate()`:

- `generator.maze` -> maze grid (`list[list[int]]`, bitmask walls per cell)
- `generator.solution` -> solution directions (`list[str]`, e.g. `['E', 'E', 'S', ...]`)
- `generator.entry` / `generator.exit` -> start and goal coordinates
- `generator.generation_path` -> step-by-step generation/animation data

Example:

```python
print(f"maze size: {len(generator.maze)} x {len(generator.maze[0])}")
print("first 10 solution moves:", generator.solution[:10])
```
