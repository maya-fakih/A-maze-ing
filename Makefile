.PHONY: all build_mlx clean fclean re run

MLX_DIR = minilibx-linux
MLX_LIB = $(MLX_DIR)/libmlx.a

C_SRCS = project/maze_displayer/minilibx_display/main.c \
         project/maze_displayer/minilibx_display/mlx_helper_1.c \
         project/maze_displayer/minilibx_display/mlx_helper_2.c \
         project/maze_displayer/minilibx_display/mlx_parser.c \
         project/maze_displayer/minilibx_display/mlx_display.c

C_OBJS = project/maze_displayer/minilibx_display/main.o \
         project/maze_displayer/minilibx_display/mlx_helper_1.o \
         project/maze_displayer/minilibx_display/mlx_helper_2.o \
         project/maze_displayer/minilibx_display/mlx_parser.o \
         project/maze_displayer/minilibx_display/mlx_display.o

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

clean:
	rm -f $(C_OBJS)

fclean: clean
	rm -f $(TARGET)
	cd $(MLX_DIR) && make clean && cd ..

re: fclean all

run: all
	python3 a_maze_ing.py config.txt
