/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   mlx_display_scene.c                                :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: aabi-mou <aabi-mou@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/02/24 04:25:00 by aabi-mou          #+#    #+#             */
/*   Updated: 2026/02/24 03:07:39 by aabi-mou         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <mlx_helper.h>

static int	cell_bits(char ch)
{
	if (ch >= '0' && ch <= '9')
		return (ch - '0');
	if (ch >= 'A' && ch <= 'F')
		return (10 + (ch - 'A'));
	return (15);
}

void	draw_cell_by_bits(t_app *app, int gx, int gy, int bits)
{
	int	px;
	int	py;
	int	size;
	int	t;
	int	wall;

	px = gx * app->config.cell_size;
	py = gy * app->config.cell_size;
	size = app->config.cell_size;
	t = size / 6;
	if (t < 1)
		t = 1;
	wall = color_from_name(app->config.wall_color, 0x2B2B2B);
	draw_square(app, gx, gy, WHITE_BG);
	if (bits & 1)
		fill_rect(app, &(t_rect){px, py, size, t, wall});
	if (bits & 2)
		fill_rect(app, &(t_rect){px + size - t, py, t, size, wall});
	if (bits & 4)
		fill_rect(app, &(t_rect){px, py + size - t, size, t, wall});
	if (bits & 8)
		fill_rect(app, &(t_rect){px, py, t, size, wall});
}

static void	draw_logo_cells(t_app *app, int flag_color)
{
	int	x;
	int	y;
	int	i;

	i = 0;
	while (i < app->maze.logo_count)
	{
		x = app->maze.logo_cells[i].x;
		y = app->maze.logo_cells[i].y;
		if (x >= 0 && y >= 0 && x < app->maze.width && y < app->maze.height)
			draw_square(app, x, y, flag_color);
		i++;
	}
}

void	draw_static_maze(t_app *app)
{
	int	x;
	int	y;
	int	wall;
	int	flag;

	wall = color_from_name(app->config.wall_color, 0x2B2B2B);
	flag = color_from_name(app->config.flag_color, ENTRY_EXIT_FALLBACK);
	if (flag == wall)
		flag = color_from_name("yellow", ENTRY_EXIT_FALLBACK);
	fill_rect(app, &(t_rect){0, 0, app->window_width, app->window_height,
		WHITE_BG});
	y = 0;
	while (y < app->maze.height)
	{
		x = 0;
		while (x < app->maze.width)
		{
			draw_cell_by_bits(app, x, y, cell_bits(app->maze.grid[y][x]));
			x++;
		}
		y++;
	}
	draw_logo_cells(app, flag);
}

void	draw_generation_base(t_app *app)
{
	int	x;
	int	y;
	int	wall;
	int	flag;

	wall = color_from_name(app->config.wall_color, 0x2B2B2B);
	flag = color_from_name(app->config.flag_color, ENTRY_EXIT_FALLBACK);
	if (flag == wall)
		flag = color_from_name("yellow", ENTRY_EXIT_FALLBACK);
	fill_rect(app, &(t_rect){0, 0, app->window_width, app->window_height,
		WHITE_BG});
	y = 0;
	while (y < app->maze.height)
	{
		x = 0;
		while (x < app->maze.width)
		{
			draw_cell_by_bits(app, x, y, 15);
			x++;
		}
		y++;
	}
	draw_logo_cells(app, flag);
}
