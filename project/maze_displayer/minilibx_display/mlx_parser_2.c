/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   mlx_parser_2.c                                     :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: aabi-mou <aabi-mou@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/02/24 02:48:59 by aabi-mou          #+#    #+#             */
/*   Updated: 2026/02/24 03:05:28 by aabi-mou         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <mlx_helper.h>

static void	fill_logo_cells(FILE *f, t_point *cells, int *count)
{
	int		i;
	int		x;
	int		y;
	char	line[256];

	i = 0;
	rewind(f);
	while (fgets(line, sizeof(line), f) != NULL)
	{
		if (sscanf(line, "%d %d", &x, &y) == 2)
		{
			cells[i].x = x;
			cells[i].y = y;
			i++;
		}
	}
	*count = i;
}

void	validate_non_white_colors(t_config *settings)
{
	if (color_from_name(settings->wall_color, -1) == WHITE_BG)
		error("Error: WALL_COLOR cannot be white in MiniLibX display.");
	if (color_from_name(settings->flag_color, -1) == WHITE_BG)
		error("Error: FLAG_COLOR cannot be white in MiniLibX display.");
}

void	set_default_config(t_config *settings)
{
	settings->width = 20;
	settings->height = 20;
	settings->shape = strdup("square");
	settings->wall_color = strdup("blue");
	settings->flag_color = strdup("grey");
	settings->path_color = strdup("green");
	settings->generation_algorithm = strdup("dfs");
	settings->solver_algorithm = strdup("bfs");
	settings->cell_size = 30;
	settings->animation_speed = 5;
}

t_cell	*parse_path(FILE *f, int *count)
{
	t_cell	*path;
	int		i;
	char	line[256];

	i = 0;
	rewind(f);
	while (fgets(line, sizeof(line), f) != NULL)
		i++;
	path = (t_cell *)malloc(sizeof(t_cell) * (i + 1));
	if (!path)
		return (NULL);
	rewind(f);
	i = 0;
	while (fgets(line, sizeof(line), f) != NULL)
	{
		parse_line(&path[i], line);
		i++;
	}
	*count = i;
	return (path);
}

t_point	*parse_logo_cells(FILE *f, int *count)
{
	t_point	*cells;
	int		cell_count;
	int		x;
	int		y;
	char	line[256];

	cell_count = 0;
	rewind(f);
	while (fgets(line, sizeof(line), f) != NULL)
	{
		if (sscanf(line, "%d %d", &x, &y) == 2)
			cell_count++;
	}
	cells = (t_point *)malloc(sizeof(t_point) * (cell_count + 1));
	if (!cells)
		return (NULL);
	fill_logo_cells(f, cells, count);
	return (cells);
}
