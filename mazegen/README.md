You must provide a short documentation describing how to:
- Instantiate and use your generator, with at least a basic example.
- Pass custom parameters (e.g., size, seed).
- Access the generated structure, and access at least a solution


NOTE FOR TEAM:
to test this version which only for now supports the basic_generator...
cd mazegen
python3 testing.py

note that you can change maze conditions as you want to test

the mazes are randomly creating branches yet the perfect is not working in all cases so we need to update it...
its probably not in the part of the random walk rather the issue is from the rest of the maze where we are randomly filling it using prims alg...

this will either be patched in the next update or we will have a seperate generator tthat generates perfect that will be a simple wilsons spanning trees so that we can have references online....