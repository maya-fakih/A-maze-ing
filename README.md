*This project has been created as part of the 42 curriculum by aabi-mou, mfakih*

# Description

# Instructions

# Resources

# Config file / additional features

# Maze generation algorithms
---

## 1. Wilson's Algorithm
Type: Uniform spanning‑tree generator.

How it works: Starts with one random cell visited. Repeatedly performs a loop‑erased random walk from an unvisited cell until it hits the visited maze, carving the walk's path. Continues until all cells are visited.

Perfect mazes: Produces exactly one unique path between any two cells.

Obstacle handling: Naturally walks around pre‑placed walls.

YouTube explanation: [Wilson's Algorithm – Maze Generation by Computerphile](https://www.reddit.com/r/proceduralgeneration/comments/g2160z/processing_maze_generation_using_wilsons_algorithm/)

## 2. Randomized Prim's Algorithm (Non‑Perfect Mazes)
Type: Greedy, tree‑growing algorithm with optional loops.

How it works: Begins with a random cell in the maze. Maintains a list of frontier walls. Repeatedly picks a random wall from the list; if the cell beyond is unvisited, carves a passage and adds its walls to the list. Can be configured to occasionally add extra passages (creating loops) for non‑perfect mazes.

Perfect mazes: Only if extra passages are disabled (default: disabled when PERFECT=True).

Texture: Branchy, organic, with natural‑looking dead‑ends and optional loops.

Blog explanation: [Randomized Prim's Maze Generation – The Coding Train](https://weblog.jamisbuck.org/2011/1/10/maze-generation-prim-s-algorithm)

## 3. CSP‑Based Backtracking (Constrained Mazes)
Type: Constraint‑propagation with backtracking.

How it works: Treats each cell as a variable with domain 0–F (wall bitmask). Uses forward checking and MRV (Minimum Remaining Values) heuristic to assign values while enforcing: wall‑coherence between neighbors, corridor‑width ≤ 2 cells, and connectivity around the "42" block.

Perfect mazes: Configurable via connectivity constraint.

Strengths: Highly flexible for custom shapes, patterns, and hard constraints.

Time complexity: Exponential in worst case, but heuristics keep it manageable for moderate sizes.

YouTube explanation: CSP Backtracking – Maze Generation (general CSP tutorials)

## 4. Good reference for showing many different algs

This is the best reference i could find for prims and the csp though the codes vary ours will include multiple optimizations to match the vision we discussed before but they show a good basis on how we will have our codes working together also checking each technique seperately will make it way easier to understand the combinations we will have espescially in the csp since it will be very complex to create shapes.. 
Youtube link: [11 algorithms to generate mazes in python](https://www.youtube.com/watch?v=U3meEXvYFsc)

# Reusable parts

# Roles

# Planning and future improvements