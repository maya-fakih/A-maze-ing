/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   mlx_helper.h                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: aabi-mou <aabi-mou@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/02/18 18:12:47 by aabi-mou          #+#    #+#             */
/*   Updated: 2026/02/18 18:41:21 by aabi-mou         ###   ########.fr       */
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
	int			phase;
	int			anim_index;
	int			frame;
}				t_app;

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
void			init_graphics(t_app *app);
t_app			*init_app(FILE *config_file, FILE *path_file,
					FILE *output_file);
void			draw_maze(t_app *app);
#endif
