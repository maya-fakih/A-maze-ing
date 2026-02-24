/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   mlx_display_mouse.c                                :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: aabi-mou <aabi-mou@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/02/24 04:25:00 by aabi-mou          #+#    #+#             */
/*   Updated: 2026/02/24 04:25:00 by aabi-mou         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <mlx_helper.h>

static const char	*g_wall[11] = {"blue", "red", "green", "cyan", "orange",
	"grey", "magenta", "yellow", "light_blue", "light_cyan", "light_green"};
static const char	*g_flag[10] = {"yellow", "magenta", "orange", "green",
	"blue", "red", "cyan", "light_yellow", "light_magenta", "light_red"};
static const char	*g_path[10] = {"green", "cyan", "yellow", "magenta",
	"orange", "red", "blue", "light_green", "light_cyan", "light_magenta"};
static const char	*g_shape[4] = {"square", "heart", "flower", "star"};
static const char	*g_gen[4] = {"dfs", "bfs", "prim", "huntkill"};
static const char	*g_solver[4] = {"dfs", "bfs", "a*", "ucs"};

static const char	*next_option(const char *current, const char **options,
		int count, const char *forbidden)
{
	int	cur;
	int	i;

	cur = 0;
	while (cur < count && (!current || strcasecmp(current, options[cur]) != 0))
		cur++;
	if (cur >= count)
		cur = 0;
	i = 1;
	while (i <= count)
	{
		if (!forbidden || color_from_name(options[(cur + i) % count], -1)
			!= color_from_name(forbidden, -2))
			return (options[(cur + i) % count]);
		i++;
	}
	return (options[cur]);
}

static void	set_config_color(char **field, const char *value)
{
	char	*copy;

	copy = strdup(value);
	if (!copy)
		return ;
	free(*field);
	*field = copy;
}

static void	handle_color_click(t_app *app, int idx)
{
	const char	*next;

	next = NULL;
	if (idx == 2)
		next = next_option(app->config.wall_color, g_wall, 11,
				app->config.flag_color);
	if (idx == 3)
		next = next_option(app->config.flag_color, g_flag, 10,
				app->config.wall_color);
	if (idx == 4)
		next = next_option(app->config.path_color, g_path, 10, NULL);
	if (idx == 2)
		update_config_value(app->config_file, "WALL_COLOR", next);
	if (idx == 3)
		update_config_value(app->config_file, "FLAG_COLOR", next);
	if (idx == 4)
		update_config_value(app->config_file, "PATH_COLOR", next);
	if (idx == 2)
		set_config_color(&app->config.wall_color, next);
	if (idx == 3)
		set_config_color(&app->config.flag_color, next);
	if (idx == 4)
		set_config_color(&app->config.path_color, next);
	redraw_base_scene(app);
}

static void	apply_click(t_app *app, int idx)
{
	if (idx == 0)
		regenerate_maze(app);
	if (idx == 1)
	{
		app->show_path = !app->show_path;
		redraw_base_scene(app);
	}
	if (idx == 2 || idx == 3 || idx == 4)
		handle_color_click(app, idx);
	if (idx == 5)
		update_config_value(app->config_file, "SHAPE",
			next_option(app->config.shape, g_shape, 4, NULL));
	if (idx == 6)
		update_config_value(app->config_file, "GENERATION_ALGORITHM",
			next_option(app->config.generation_algorithm, g_gen, 4, NULL));
	if (idx == 7)
		update_config_value(app->config_file, "SOLVER_ALGORITHM",
			next_option(app->config.solver_algorithm, g_solver, 4, NULL));
	if (idx >= 5)
		regenerate_maze(app);
}

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
		if (x >= btns[i].x && x <= btns[i].x + btns[i].w && y >= btns[i].y
			&& y <= btns[i].y + btns[i].h)
		{
			apply_click(app, i);
			mlx_put_image_to_window(app->mlx, app->win, app->img.img, 0, 0);
			draw_button_panel(app);
			return (0);
		}
		i++;
	}
	return (0);
}
