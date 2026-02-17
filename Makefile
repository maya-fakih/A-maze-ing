.PHONY: all build_mlx clean

all: build_mlx

build_mlx:
	cd minilibx-linux && ./configure && make && cd ..
	gcc -I./minilibx-linux \
		project/maze_displayer/mlx_display.c \
		-L./minilibx-linux -lmlx -lX11 -lXext \
		-o project/maze_displayer/mlx_display.exe

clean:
	rm -f project/maze_displayer/mlx_display.exe
	cd minilibx-linux && make clean