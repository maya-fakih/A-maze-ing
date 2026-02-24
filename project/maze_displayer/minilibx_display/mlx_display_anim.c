/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   mlx_display_anim.c                                 :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: aabi-mou <aabi-mou@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/02/24 04:25:00 by aabi-mou          #+#    #+#             */
/*   Updated: 2026/02/24 03:06:50 by aabi-mou         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <mlx_helper.h>

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
	draw_star_marker(app, x, y, path_color);
}

void	redraw_base_scene(t_app *app)
{
	draw_static_maze(app);
	if (app->show_path && app->phase >= 2)
		draw_solution_until(app, app->maze.solution_len);
}

void	animate_generation(t_app *app)
{
	t_cell	cell;

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
	draw_cell_by_bits(app, cell.point.x, cell.point.y, cell.value);
	draw_star_marker(app, cell.point.x, cell.point.y,
		color_from_name(app->config.wall_color, 0x2B2B2B));
	app->anim_index++;
}

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
