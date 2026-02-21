/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   mlx_display.c                                      :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: aabi-mou <aabi-mou@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/02/18 18:09:11 by aabi-mou          #+#    #+#             */
/*   Updated: 2026/02/20 23:49:00 by codex             ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <mlx_helper.h>
#include <X11/Xlib.h>

typedef struct s_mlx_win
{
	Window	window;
	void	*gc;
	void	*next;
}	t_mlx_win;

typedef struct s_mlx_xvar
{
	Display	*display;
	Window	root;
}	t_mlx_xvar;

static const char	*g_wall_colors[] = {"blue", "red", "green", "cyan",
	"orange", "grey", "magenta", "yellow", "light_blue", "light_cyan",
	"light_green"};
static const char	*g_flag_colors[] = {"yellow", "magenta", "orange", "green",
	"blue", "red", "cyan", "light_yellow", "light_magenta", "light_red"};
static const char	*g_path_colors[] = {"green", "cyan", "yellow", "magenta",
	"orange", "red", "blue", "light_green", "light_cyan", "light_magenta"};
static const char	*g_shapes[] = {"square", "heart", "flower", "star"};
static const char	*g_generation_algorithms[] = {"dfs", "bfs",
	"prim", "huntkill"};
static const char	*g_solver_algorithms[] = {"dfs", "bfs", "a*", "ucs"};
static const char	*g_button_labels[] = {"Regenerate maze",
	"Show / hide path", "Change wall color", "Change flag color",
	"Change path color", "Change shape", "Change generation algo",
	"Change solver algo"};
static const int	g_button_colors[] = {0x5E2CA5, 0x5E2CA5, 0x5E2CA5,
	0x5E2CA5, 0x5E2CA5, 0x5E2CA5, 0x5E2CA5, 0x5E2CA5};

/* Execute index_of_value. */
static int	index_of_value(const char *value, const char **options, int count)
{
	int	i;

	i = 0;
	while (i < count)
	{
		if (value && strcasecmp(value, options[i]) == 0)
			return (i);
		i++;
	}
	return (0);
}

static const char	*next_value(const char *current, const char **options, int count)
{
	int	idx;

	idx = index_of_value(current, options, count);
	return (options[(idx + 1) % count]);
}

/* Execute build_buttons. */
static void	build_buttons(t_app *app, t_button *btns)
{
	int	i;

	btns[0].x = app->panel_x + PANEL_MARGIN;
	btns[0].y = PANEL_MARGIN;
	btns[0].w = app->panel_width - (PANEL_MARGIN * 2);
	btns[0].h = BTN_HEIGHT;
	btns[0].color = g_button_colors[0];
	btns[0].label = g_button_labels[0];
	i = 1;
	while (i < BTN_COUNT)
	{
		btns[i].x = btns[0].x;
		btns[i].y = btns[i - 1].y + BTN_HEIGHT + BTN_GAP;
		btns[i].w = btns[0].w;
		btns[i].h = BTN_HEIGHT;
		btns[i].color = g_button_colors[i];
		btns[i].label = g_button_labels[i];
		i++;
	}
}

/* Execute color_from_name. */
int	color_from_name(const char *name, int fallback)
{
	if (!name)
		return (fallback);
	if (strcasecmp(name, "black") == 0)
		return (0x1E1E1E);
	if (strcasecmp(name, "white") == 0)
		return (0xFFFFFF);
	if (strcasecmp(name, "red") == 0)
		return (0xE53935);
	if (strcasecmp(name, "green") == 0)
		return (0x43A047);
	if (strcasecmp(name, "yellow") == 0)
		return (0xFDD835);
	if (strcasecmp(name, "blue") == 0)
		return (0x1E88E5);
	if (strcasecmp(name, "magenta") == 0)
		return (0xD81B60);
	if (strcasecmp(name, "cyan") == 0)
		return (0x00ACC1);
	if (strcasecmp(name, "orange") == 0)
		return (0xFB8C00);
	if (strcasecmp(name, "grey") == 0 || strcasecmp(name, "gray") == 0)
		return (0x6D6D6D);
	if (strcasecmp(name, "bright_white") == 0
		|| strcasecmp(name, "light_white") == 0)
		return (0xFFFFFF);
	if (strcasecmp(name, "light_red") == 0
		|| strcasecmp(name, "bright_red") == 0)
		return (0xFF6B6B);
	if (strcasecmp(name, "light_green") == 0
		|| strcasecmp(name, "bright_green") == 0)
		return (0x72D572);
	if (strcasecmp(name, "light_yellow") == 0
		|| strcasecmp(name, "bright_yellow") == 0)
		return (0xFFE66D);
	if (strcasecmp(name, "light_blue") == 0
		|| strcasecmp(name, "bright_blue") == 0)
		return (0x6CB6FF);
	if (strcasecmp(name, "light_magenta") == 0
		|| strcasecmp(name, "bright_magenta") == 0)
		return (0xF062C0);
	if (strcasecmp(name, "light_cyan") == 0
		|| strcasecmp(name, "bright_cyan") == 0)
		return (0x67E8F9);
	if (strcasecmp(name, "bright_black") == 0)
		return (0x7A7A7A);
	return (fallback);
}

static const char	*next_distinct_color(const char *current, const char **options,
	int count, const char *forbidden)
{
	int		i;
	int		idx;
	int		next;
	int		forbidden_color;

	idx = index_of_value(current, options, count);
	forbidden_color = color_from_name(forbidden, -2);
	i = 1;
	while (i <= count)
	{
		next = (idx + i) % count;
		if (!forbidden || color_from_name(options[next], -1) != forbidden_color)
			return (options[next]);
		i++;
	}
	return (options[idx]);
}

/* Execute set_config_color. */
static void	set_config_color(char **field, const char *value)
{
	char	*copy;

	if (!field || !value)
		return ;
	copy = strdup(value);
	if (!copy)
		return ;
	free(*field);
	*field = copy;
}

/* Execute safe_flag_color. */
static int	safe_flag_color(t_app *app, int wall_color)
{
	int	flag_color;

	flag_color = color_from_name(app->config.flag_color, ENTRY_EXIT_FALLBACK);
	if (flag_color != wall_color)
		return (flag_color);
	if (wall_color == color_from_name("yellow", -1))
		return (color_from_name("blue", ENTRY_EXIT_FALLBACK));
	return (color_from_name("yellow", ENTRY_EXIT_FALLBACK));
}

/* Execute put_pixel. */
void	put_pixel(t_img *img, int x, int y, int color)
{
	char	*dst;

	if (x < 0 || y < 0)
		return ;
	dst = img->addr + (y * img->line_len + x * (img->bpp / 8));
	*(unsigned int *)dst = color;
}

/* Execute fill_rect. */
static void	fill_rect(t_app *app, int x, int y, int w, int h, int color)
{
	int	px;
	int	py;

	py = y;
	while (py < y + h)
	{
		px = x;
		while (px < x + w)
		{
			put_pixel(&app->img, px, py, color);
			px++;
		}
		py++;
	}
}

/* Execute draw_square. */
void	draw_square(t_app *app, int gx, int gy, int color)
{
	int	px;
	int	py;
	int	x;
	int	y;

	px = gx * app->config.cell_size;
	py = gy * app->config.cell_size;
	y = 0;
	while (y < app->config.cell_size)
	{
		x = 0;
		while (x < app->config.cell_size)
		{
			put_pixel(&app->img, px + x, py + y, color);
			x++;
		}
		y++;
	}
}

/* Draw a small star-shaped marker centered in the cell. This draws directly
   into the image buffer so it persists when the image is blitted to the
   window. The marker scales with cell_size. */
/* Execute draw_star_marker. */
static void	draw_star_marker(t_app *app, int gx, int gy, int color)
{
	int	cx;
	int	cy;
	int	size;
	int	i;

	size = app->config.cell_size;
	cx = gx * size + size / 2;
	cy = gy * size + size / 2;

	/* simple 5-point star like marker using lines */
	put_pixel(&app->img, cx, cy, color);
	for (i = 1; i <= (size / 6 + 1); i++)
	{
		put_pixel(&app->img, cx + i, cy, color);
		put_pixel(&app->img, cx - i, cy, color);
		put_pixel(&app->img, cx, cy + i, color);
		put_pixel(&app->img, cx, cy - i, color);
		put_pixel(&app->img, cx + i, cy + i, color);
		put_pixel(&app->img, cx - i, cy - i, color);
		put_pixel(&app->img, cx + i, cy - i, color);
		put_pixel(&app->img, cx - i, cy + i, color);
	}
}

/* Execute wall_thickness. */
static int	wall_thickness(t_app *app)
{
	int	thickness;

	thickness = app->config.cell_size / 6;
	if (thickness < 1)
		thickness = 1;
	return (thickness);
}

/* Execute draw_cell_by_bits. */
static void	draw_cell_by_bits(t_app *app, int gx, int gy, int bits, int wall_color)
{
	int	px;
	int	py;
	int	size;
	int	t;

	px = gx * app->config.cell_size;
	py = gy * app->config.cell_size;
	size = app->config.cell_size;
	t = wall_thickness(app);
	draw_square(app, gx, gy, WHITE_BG);
	if (bits & 0x1)
		fill_rect(app, px, py, size, t, wall_color);
	if (bits & 0x2)
		fill_rect(app, px + size - t, py, t, size, wall_color);
	if (bits & 0x4)
		fill_rect(app, px, py + size - t, size, t, wall_color);
	if (bits & 0x8)
		fill_rect(app, px, py, t, size, wall_color);
}

/* Execute draw_static_maze. */
void	draw_static_maze(t_app *app)
{
	int	x;
	int	y;
	int	wall_color;
	int	flag_color;
	int	i;
	int	lx;
	int	ly;

	wall_color = color_from_name(app->config.wall_color, 0x2B2B2B);
	flag_color = safe_flag_color(app, wall_color);
	fill_rect(app, 0, 0, app->window_width, app->window_height, WHITE_BG);
	y = 0;
	while (y < app->maze.height)
	{
		x = 0;
		while (x < app->maze.width)
		{
			if (app->maze.grid[y][x] == '0')
				draw_cell_by_bits(app, x, y, 0x0, wall_color);
			else if (app->maze.grid[y][x] == '1')
				draw_cell_by_bits(app, x, y, 0x1, wall_color);
			else if (app->maze.grid[y][x] == '2')
				draw_cell_by_bits(app, x, y, 0x2, wall_color);
			else if (app->maze.grid[y][x] == '3')
				draw_cell_by_bits(app, x, y, 0x3, wall_color);
			else if (app->maze.grid[y][x] == '4')
				draw_cell_by_bits(app, x, y, 0x4, wall_color);
			else if (app->maze.grid[y][x] == '5')
				draw_cell_by_bits(app, x, y, 0x5, wall_color);
			else if (app->maze.grid[y][x] == '6')
				draw_cell_by_bits(app, x, y, 0x6, wall_color);
			else if (app->maze.grid[y][x] == '7')
				draw_cell_by_bits(app, x, y, 0x7, wall_color);
			else if (app->maze.grid[y][x] == '8')
				draw_cell_by_bits(app, x, y, 0x8, wall_color);
			else if (app->maze.grid[y][x] == '9')
				draw_cell_by_bits(app, x, y, 0x9, wall_color);
			else if (app->maze.grid[y][x] == 'A')
				draw_cell_by_bits(app, x, y, 0xA, wall_color);
			else if (app->maze.grid[y][x] == 'B')
				draw_cell_by_bits(app, x, y, 0xB, wall_color);
			else if (app->maze.grid[y][x] == 'C')
				draw_cell_by_bits(app, x, y, 0xC, wall_color);
			else if (app->maze.grid[y][x] == 'D')
				draw_cell_by_bits(app, x, y, 0xD, wall_color);
			else if (app->maze.grid[y][x] == 'E')
				draw_cell_by_bits(app, x, y, 0xE, wall_color);
			else if (app->maze.grid[y][x] == 'F')
				draw_square(app, x, y, wall_color);
			else
				draw_cell_by_bits(app, x, y, 0xF, wall_color);
			x++;
		}
		y++;
	}
	i = 0;
	while (i < app->maze.logo_count)
	{
		lx = app->maze.logo_cells[i].x;
		ly = app->maze.logo_cells[i].y;
		if (lx >= 0 && ly >= 0 && lx < app->maze.width && ly < app->maze.height)
			draw_square(app, lx, ly, flag_color);
		i++;
	}
}

/* Execute draw_solution_until. */
static void	draw_solution_until(t_app *app, int steps)
{
	int	i;
	int	x;
	int	y;
	int	path_color;

	x = app->maze.entry.x;
	y = app->maze.entry.y;
	path_color = color_from_name(app->config.path_color, MAZE_PATH_COLOR);
	i = 0;
	while (i < steps && i < app->maze.solution_len)
	{
		/* draw a small star marker instead of filling whole cell */
		draw_star_marker(app, x, y, path_color);
		if (app->maze.solution[i] == 'N')
			y--;
		else if (app->maze.solution[i] == 'S')
			y++;
		else if (app->maze.solution[i] == 'E')
			x++;
		else if (app->maze.solution[i] == 'W')
			x--;
		i++;
	}
	/* draw marker for final cell */
	draw_star_marker(app, x, y, path_color);
}

/* Execute draw_generation_base. */
static void	draw_generation_base(t_app *app)
{
	int	x;
	int	y;
	int	wall_color;
	int	flag_color;
	int	i;
	int	lx;
	int	ly;

	wall_color = color_from_name(app->config.wall_color, 0x2B2B2B);
	flag_color = safe_flag_color(app, wall_color);
	fill_rect(app, 0, 0, app->window_width, app->window_height, WHITE_BG);
	y = 0;
	while (y < app->maze.height)
	{
		x = 0;
		while (x < app->maze.width)
		{
			draw_cell_by_bits(app, x, y, 0xF, wall_color);
			x++;
		}
		y++;
	}
	i = 0;
	while (i < app->maze.logo_count)
	{
		lx = app->maze.logo_cells[i].x;
		ly = app->maze.logo_cells[i].y;
		if (lx >= 0 && ly >= 0 && lx < app->maze.width && ly < app->maze.height)
			draw_square(app, lx, ly, flag_color);
		i++;
	}
}

/* Execute redraw_base_scene. */
void	redraw_base_scene(t_app *app)
{
	draw_static_maze(app);
	if (app->show_path && app->phase >= 2)
		draw_solution_until(app, app->maze.solution_len);
}

/* Execute animate_generation. */
void	animate_generation(t_app *app)
{
	t_cell	cell;
	int		wall_color;

	if (app->anim_index == 0)
		draw_generation_base(app);
	if (app->anim_index >= app->maze.gen_total_steps)
	{
		app->phase = 2;
		app->anim_index = 0;
		redraw_base_scene(app);
		return ;
	}
	cell = app->maze.gen_path[app->anim_index];
	wall_color = color_from_name(app->config.wall_color, 0x2B2B2B);
	draw_cell_by_bits(app, cell.point.x, cell.point.y, cell.value, wall_color);
	draw_star_marker(app, cell.point.x, cell.point.y, wall_color);
	app->anim_index++;
}

/* Execute animate_solution. */
void	animate_solution(t_app *app)
{
	if (app->anim_index >= app->maze.solution_len)
	{
		app->phase = 2;
		return ;
	}
	if (app->show_path)
		draw_solution_until(app, app->anim_index);
	app->anim_index++;
}

/* Execute update. */
int	update(void *param)
{
	t_app	*app;
	int		interval;

	app = (t_app *)param;
	interval = app->config.animation_speed;
	if (interval < 1)
		interval = 1;
	app->frame++;
	if (app->phase == 0 && (app->frame % interval) == 0)
		animate_generation(app);
	mlx_put_image_to_window(app->mlx, app->win, app->img.img, 0, 0);
	draw_button_panel(app);
	return (0);
}

/* Execute free_maze. */
static void	free_maze(t_app *app)
{
	int	y;

	y = 0;
	while (app->maze.grid && y < app->maze.height)
	{
		free(app->maze.grid[y]);
		y++;
	}
	free(app->maze.grid);
	free(app->maze.solution);
	free(app->maze.gen_path);
	free(app->maze.logo_cells);
	app->maze.grid = NULL;
	app->maze.solution = NULL;
	app->maze.gen_path = NULL;
	app->maze.logo_cells = NULL;
	app->maze.solution_len = 0;
	app->maze.logo_count = 0;
}

/* Execute reload_from_files. */
void	reload_from_files(t_app *app)
{
	FILE		*config_file;
	FILE		*path_file;
	FILE		*output_file;
	FILE		*logo_file;
	t_config	*cfg;
	t_maze		*maze;
	t_cell		*gen_path;
	t_point		*logo_cells;
	int			gen_steps;
	int			logo_count;

	config_file = fopen(app->config_file, "r");
	path_file = fopen(app->path_file, "r");
	output_file = fopen(app->output_file, "r");
	logo_file = fopen(app->logo_file, "r");
	if (!config_file || !path_file || !output_file || !logo_file)
	{
		if (config_file)
			fclose(config_file);
		if (path_file)
			fclose(path_file);
		if (output_file)
			fclose(output_file);
		if (logo_file)
			fclose(logo_file);
		return ;
	}
	cfg = parse_settings(config_file);
	if (!cfg)
	{
		fclose(config_file);
		fclose(path_file);
		fclose(output_file);
		fclose(logo_file);
		return ;
	}
	gen_path = parse_path(path_file, &gen_steps);
	if (!gen_path)
	{
		free(cfg);
		fclose(config_file);
		fclose(path_file);
		fclose(output_file);
		fclose(logo_file);
		return ;
	}
	logo_cells = parse_logo_cells(logo_file, &logo_count);
	if (!logo_cells)
	{
		free(cfg);
		free(gen_path);
		fclose(config_file);
		fclose(path_file);
		fclose(output_file);
		fclose(logo_file);
		return ;
	}
	maze = parse_output(output_file, gen_path, gen_steps, cfg->width, cfg->height);
	if (!maze)
	{
		free(cfg);
		free(gen_path);
		free(logo_cells);
		fclose(config_file);
		fclose(path_file);
		fclose(output_file);
		fclose(logo_file);
		return ;
	}
	maze->logo_cells = logo_cells;
	maze->logo_count = logo_count;
	free(app->config.shape);
	free(app->config.wall_color);
	free(app->config.flag_color);
	free(app->config.path_color);
	free(app->config.generation_algorithm);
	free(app->config.solver_algorithm);
	free_maze(app);
	app->config = *cfg;
	free(cfg);
	app->maze = *maze;
	free(maze);
	fclose(config_file);
	fclose(path_file);
	fclose(output_file);
	fclose(logo_file);
}

static const char	*cfg_basename(const char *path)
{
	const char	*base;

	base = strrchr(path, '/');
	if (!base)
		base = strrchr(path, '\\');
	if (!base)
		return (path);
	return (base + 1);
}

/* Execute regenerate_maze. */
static void	regenerate_maze(t_app *app)
{
	char	command[512];
	int	ret;

	snprintf(command, sizeof(command),
		"AMAZE_NO_DISPLAY=1 DISPLAY= python3 a_maze_ing.py %s >/dev/null 2>&1",
		cfg_basename(app->config_file));
	ret = system(command);
	if (ret != 0)
		return ;
	reload_from_files(app);
	app->phase = 0;
	app->anim_index = 0;
	app->frame = 0;
	animate_generation(app);
}

int	update_config_value(const char *config_path, const char *key,
	const char *value)
{
	FILE	*in;
	FILE	*out;
	char	line[512];
	char	tmp_path[320];
	char	*eq;
	char	key_buf[256];
	size_t	key_len;
	int		found;

	snprintf(tmp_path, sizeof(tmp_path), "%s.tmp", config_path);
	in = fopen(config_path, "r");
	out = fopen(tmp_path, "w");
	if (!in || !out)
	{
		if (in)
			fclose(in);
		if (out)
			fclose(out);
		return (1);
	}
	found = 0;
	while (fgets(line, sizeof(line), in))
	{
		eq = strchr(line, '=');
		if (!eq || is_comment_line(line))
		{
			fputs(line, out);
			continue ;
		}
		memset(key_buf, 0, sizeof(key_buf));
		key_len = (size_t)(eq - line);
		if (key_len >= sizeof(key_buf))
			key_len = sizeof(key_buf) - 1;
		memcpy(key_buf, line, key_len);
		strcpy(key_buf, trim(key_buf));
		if (strcasecmp(key_buf, key) == 0)
		{
			if (!found)
				fprintf(out, "%s=%s\n", key, value);
			found = 1;
		}
		else
			fputs(line, out);
	}
	if (!found)
		fprintf(out, "%s=%s\n", key, value);
	fclose(in);
	fclose(out);
	remove(config_path);
	rename(tmp_path, config_path);
	return (0);
}

/* Execute clicked_button. */
static int	clicked_button(t_button *btn, int x, int y)
{
	return (x >= btn->x && x <= btn->x + btn->w
		&& y >= btn->y && y <= btn->y + btn->h);
}

/* Execute on_button_click. */
static void	on_button_click(t_app *app, int btn_index)
{
	const char	*next;

	if (btn_index == 0)
		regenerate_maze(app);
	else if (btn_index == 1)
	{
		app->show_path = !app->show_path;
		redraw_base_scene(app);
	}
	else if (btn_index == 2)
	{
		next = next_distinct_color(app->config.wall_color, g_wall_colors, 11,
				app->config.flag_color);
		update_config_value(app->config_file, "WALL_COLOR", next);
		set_config_color(&app->config.wall_color, next);
		redraw_base_scene(app);
	}
	else if (btn_index == 3)
	{
		next = next_distinct_color(app->config.flag_color, g_flag_colors, 10,
				app->config.wall_color);
		update_config_value(app->config_file, "FLAG_COLOR", next);
		set_config_color(&app->config.flag_color, next);
		redraw_base_scene(app);
	}
	else if (btn_index == 4)
	{
		next = next_value(app->config.path_color, g_path_colors, 10);
		update_config_value(app->config_file, "PATH_COLOR", next);
		set_config_color(&app->config.path_color, next);
		redraw_base_scene(app);
	}
	else if (btn_index == 5)
	{
		next = next_value(app->config.shape, g_shapes, 4);
		update_config_value(app->config_file, "SHAPE", next);
		regenerate_maze(app);
	}
	else if (btn_index == 6)
	{
		next = next_value(app->config.generation_algorithm,
				g_generation_algorithms, 4);
		update_config_value(app->config_file, "GENERATION_ALGORITHM", next);
		regenerate_maze(app);
	}
	else if (btn_index == 7)
	{
		next = next_value(app->config.solver_algorithm, g_solver_algorithms, 4);
		update_config_value(app->config_file, "SOLVER_ALGORITHM", next);
		regenerate_maze(app);
	}
}

/* Execute mouse_hook. */
int	mouse_hook(int button, int x, int y, void *param)
{
	t_app		*app;
	t_button	btns[BTN_COUNT];
	int			i;

	if (button != 1)
		return (0);
	app = (t_app *)param;
	build_buttons(app, btns);
	i = 0;
	while (i < BTN_COUNT)
	{
		if (clicked_button(&btns[i], x, y))
		{
			on_button_click(app, i);
			mlx_put_image_to_window(app->mlx, app->win, app->img.img, 0, 0);
			draw_button_panel(app);
			break ;
		}
		i++;
	}
	return (0);
}

/* Execute draw_button_panel. */
void	draw_button_panel(t_app *app)
{
	t_button	btns[BTN_COUNT];
	int			i;
	int			btn_txt_color;
	int			info_txt_color;
	int			info_y;
	char		info[160];

	build_buttons(app, btns);
	fill_rect(app, app->panel_x, 0, app->panel_width, app->window_height, PANEL_BG);
	i = 0;
	btn_txt_color = 0xFFFFFF;
	info_txt_color = 0x1E1E1E;
	mlx_set_font(app->mlx, app->win, "10x20");
	while (i < BTN_COUNT)
	{
		fill_rect(app, btns[i].x, btns[i].y, btns[i].w, btns[i].h, btns[i].color);
		mlx_string_put(app->mlx, app->win, btns[i].x + BTN_LABEL_XPAD,
			btns[i].y + BTN_LABEL_YPAD, btn_txt_color, (char *)btns[i].label);
		i++;
	}
	info_y = btns[BTN_COUNT - 1].y + BTN_HEIGHT + BTN_GAP + 12;
	snprintf(info, sizeof(info), "Wall: %s | Flag: %s",
		app->config.wall_color, app->config.flag_color);
	mlx_string_put(app->mlx, app->win, btns[0].x, info_y, info_txt_color, info);
	info_y += 18;
	snprintf(info, sizeof(info), "Path: %s | Shape: %s",
		app->config.path_color, app->config.shape);
	mlx_string_put(app->mlx, app->win, btns[0].x, info_y, info_txt_color, info);
	info_y += 18;
	snprintf(info, sizeof(info), "Gen: %s | Solver: %s",
		app->config.generation_algorithm, app->config.solver_algorithm);
	mlx_string_put(app->mlx, app->win, btns[0].x, info_y, info_txt_color, info);
	info_y += 18;
	mlx_string_put(app->mlx, app->win, btns[0].x, info_y, info_txt_color,
		(char *)"Click buttons to cycle list options");
}

/* Execute close_window. */
int	close_window(t_app *app)
{
	mlx_destroy_window(app->mlx, app->win);
	exit(0);
}

/* Execute center_window. */
static void	center_window(t_app *app)
{
	t_mlx_xvar	*xvar;
	t_mlx_win	*win;
	int			screen_w;
	int			screen_h;
	int			pos_x;
	int			pos_y;

	xvar = (t_mlx_xvar *)app->mlx;
	win = (t_mlx_win *)app->win;
	mlx_get_screen_size(app->mlx, &screen_w, &screen_h);
	pos_x = (screen_w - app->window_width) / 2;
	pos_y = (screen_h - app->window_height) / 2;
	if (pos_x < 0)
		pos_x = 0;
	if (pos_y < 0)
		pos_y = 0;
	XMoveWindow(xvar->display, win->window, pos_x, pos_y);
	XFlush(xvar->display);
}

/* Execute init_graphics. */
void	init_graphics(t_app *app)
{
	app->maze_px_w = app->maze.width * app->config.cell_size;
	app->maze_px_h = app->maze.height * app->config.cell_size;
	app->panel_width = 360;
	app->panel_x = app->maze_px_w;
	app->window_width = app->maze_px_w + app->panel_width;
	app->window_height = app->maze_px_h;
	if (app->window_height < 640)
		app->window_height = 640;
	app->mlx = mlx_init();
	app->win = mlx_new_window(app->mlx, app->window_width, app->window_height,
			APP_TITLE);
	app->img.img = mlx_new_image(app->mlx, app->window_width, app->window_height);
	app->img.addr = mlx_get_data_addr(app->img.img, &app->img.bpp,
			&app->img.line_len, &app->img.endian);
	center_window(app);
	/* Register a handler so clicking the window close button (X) will exit */
	mlx_hook(app->win, 17, 0, (int (*)(void *))close_window, app);
}
