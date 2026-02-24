.PHONY: all build_mlx clean fclean re run install debug lint

MLX_DIR = minilibx-linux
MLX_LIB = $(MLX_DIR)/libmlx.a

C_SRCS = $(wildcard project/maze_displayer/minilibx_display/*.c)
C_OBJS = $(C_SRCS:.c=.o)

CC = gcc
CFLAGS = -Wall -Wextra -Werror -I./$(MLX_DIR) -I./project/maze_displayer/minilibx_display
LDFLAGS = -L./$(MLX_DIR) -lmlx -lX11 -lXext -lm

TARGET = project/maze_displayer/minilibx_display/main.exe

all: build_mlx $(TARGET)

$(MLX_LIB):
	cd $(MLX_DIR) && ./configure && make && cd ..

project/maze_displayer/minilibx_display/%.o: project/maze_displayer/minilibx_display/%.c
	$(CC) $(CFLAGS) -c $< -o $@

$(TARGET): $(MLX_LIB) $(C_OBJS)
	$(CC) $(CFLAGS) $(C_OBJS) $(LDFLAGS) -o $@

build_mlx: $(TARGET)

install:
	python3 -m pip install mypy
	python3 -m pip install flake8

clean:
	rm -f $(C_OBJS)
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type d -name .mypy_cache -exec rm -rf {} +

fclean: clean
	rm -f $(TARGET)
	cd $(MLX_DIR) && make clean && cd ..

re: fclean all

run: all
	python3 a_maze_ing.py config.txt

debug: all
	python3 -m pdb a_maze_ing.py config.txt

lint:
	flake8 .
	mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs
