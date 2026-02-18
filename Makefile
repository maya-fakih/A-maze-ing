# Makefile for A-MAZE-ING project
.PHONY: all build_mlx clean fclean re

# Directories and files
MLX_DIR = minilibx-linux
MLX_LIB = $(MLX_DIR)/libmlx.a

# Source files
C_SRCS = project/maze_displayer/main.c \
		 project/maze_displayer/mlx_helper_1.c \
		 project/maze_displayer/mlx_helper_2.c \
		 project/maze_displayer/mlx_parser.c \
		 project/maze_displayer/mlx_display.c

C_OBJS = project/maze_displayer/main.o \
		 project/maze_displayer/mlx_helper_1.o \
		 project/maze_displayer/mlx_helper_2.o \
		 project/maze_displayer/mlx_parser.o \
		 project/maze_displayer/mlx_display.o

# Compiler
CC = gcc
CFLAGS = -Wall -Wextra -Werror -I./$(MLX_DIR) -I./project/maze_displayer
LDFLAGS = -L./$(MLX_DIR) -lmlx -lX11 -lXext -lm

# Target executable
TARGET = project/maze_displayer/main.exe

# Default target
all: build_mlx $(TARGET)

# Build minilibx
$(MLX_LIB):
	cd $(MLX_DIR) && ./configure && make && cd ..

# Compile object files
project/maze_displayer/%.o: project/maze_displayer/%.c
	$(CC) $(CFLAGS) -c $< -o $@

# Link executable
$(TARGET): $(MLX_LIB) $(C_OBJS)
	$(CC) $(CFLAGS) $(C_OBJS) $(LDFLAGS) -o $@
	@echo "✓ Compiled main.exe"

# Build everything (minilibx + C program)
build_mlx: $(TARGET)

# Clean object files
clean:
	rm -f $(C_OBJS)

# Clean everything including executable
fclean: clean
	rm -f $(TARGET)
	cd $(MLX_DIR) && make clean && cd ..

# Rebuild from scratch
re: fclean all

.PHONY: run
run: all
	python3 a_maze_ing.py config.txt