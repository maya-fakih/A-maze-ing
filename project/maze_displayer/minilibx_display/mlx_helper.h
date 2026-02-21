/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   mlx_helper.h                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: aabi-mou <aabi-mou@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/02/18 18:12:47 by aabi-mou          #+#    #+#             */
/*   Updated: 2026/02/21 13:45:21 by aabi-mou         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#ifndef MLX_HELPER_H
# define MLX_HELPER_H

# include <ctype.h>
# include <mlx.h>
# include <stdbool.h>
# include <stdio.h>
# include <stdlib.h>
# include <string.h>
# include <strings.h>

# define APP_TITLE "A-MAZE-ING"
# define WHITE_BG 0xFFFFFF
# define PANEL_BG 0xF2F2F2
# define MAZE_PATH_COLOR 0x00A870
# define ENTRY_EXIT_FALLBACK 0x1E88E5
# define GEN_STEP_COLOR 0x41B6E6
# define BTN_COUNT 8
# define BTN_HEIGHT 52
# define BTN_GAP 12
# define PANEL_MARGIN 16
# define BTN_LABEL_XPAD 12
# define BTN_LABEL_YPAD 32

// we need this for the coordinates
typedef struct s_point
{
	int			x;
	int			y;
}				t_point;

// Image buffer structure for MLX
typedef struct s_img
{
	void		*img;
	char		*addr;
	int			bpp;
	int			line_len;
	int			endian;
}				t_img;

typedef struct s_cell
{
	t_point		point;
	int			value;
	bool		is_sol;
}				t_cell;

// we need from config.txt: shape, wall_color, flag_color
// we will look for them and put them in variables when we find them,
// i will use a structure called config
typedef struct s_config
{
	int			width;
	int			height;
	char		*shape;
	char		*wall_color;
	char		*flag_color;
	char		*path_color;
	char		*generation_algorithm;
	char		*solver_algorithm;
	int			cell_size;
	int			animation_speed;
}				t_config;

// we need from maze.txt the 2D array -> maze
// entry, exit point and the solution -> we need to read
// all the lines and put them in variables
// Animation -> we need the self.path but how to get it?
typedef struct s_maze
{
	char		**grid;
	int			width;
	int			height;
	t_point		*logo_cells;
	int			logo_count;
	t_point		entry;
	t_point		exit;
	char		*solution;
	int			solution_len;
	t_cell		*gen_path;
	int			gen_total_steps;
}				t_maze;

// This structure holds everything needed to animate
typedef struct s_app
{
	t_config	config;
	t_maze		maze;
	void		*mlx;
	void		*win;
	t_img		img;
	int			window_width;
	int			window_height;
	int			maze_px_w;
	int			maze_px_h;
	int			panel_x;
	int			panel_width;
	int			phase;
	int			anim_index;
	int			frame;
	bool		show_path;
	char		config_file[256];
	char		path_file[256];
	char		output_file[256];
	char		logo_file[256];
}				t_app;

typedef struct s_button
{
	int			x;
	int			y;
	int			w;
	int			h;
	int			color;
	const char	*label;
}				t_button;

void			error(const char *s);
void			print_config(t_config *config);
void			print_cell(t_cell *cell);
void			print_path(t_cell *path, int count);
void			print_maze(t_maze *maze);
char			*trim(char *str);
bool			is_comment_line(const char *line);
char			*find_value(char *line);
t_config		*parse_settings(FILE *f);
void			parse_line(t_cell *path, char *line);
t_cell			*parse_path(FILE *f, int *count);
t_point			*parse_logo_cells(FILE *f, int *count);
char			**fill_grid(FILE *f, int w, int h);
t_point			parse_coordinates(const char *line);
t_maze			*parse_output(FILE *f, t_cell *path, int steps, int width,
					int height);
void			put_pixel(t_img *img, int x, int y, int color);
void			draw_square(t_app *app, int gx, int gy, int color);
void			draw_static_maze(t_app *app);
void			animate_generation(t_app *app);
void			animate_solution(t_app *app);
int				update(void *param);
int				close_window(t_app *app);
int				mouse_hook(int button, int x, int y, void *param);
void			init_graphics(t_app *app);
t_app			*init_app(FILE *config_file, FILE *path_file, FILE *output_file,
					FILE *logo_file, char **argv);
void			draw_maze(t_app *app);
int				color_from_name(const char *name, int fallback);
void			draw_button_panel(t_app *app);
void			redraw_base_scene(t_app *app);
void			reload_from_files(t_app *app);
int				update_config_value(const char *config_path, const char *key,
					const char *value);
#endif
