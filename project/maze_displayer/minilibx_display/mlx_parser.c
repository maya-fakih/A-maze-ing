/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   mlx_parser.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: aabi-mou <aabi-mou@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/02/18 18:04:45 by aabi-mou          #+#    #+#             */
/*   Updated: 2026/02/20 23:49:00 by codex             ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <mlx_helper.h>

/* Execute validate_non_white_colors. */
static void	validate_non_white_colors(t_config *settings)
{
	if (color_from_name(settings->wall_color, -1) == WHITE_BG)
		error("Error: WALL_COLOR cannot be white in MiniLibX display.");
	if (color_from_name(settings->flag_color, -1) == WHITE_BG)
		error("Error: FLAG_COLOR cannot be white in MiniLibX display.");
}

/* Execute set_default_config. */
static void	set_default_config(t_config *settings)
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
	settings->animation_speed = 20;
}

/* Execute set_setting_value. */
static void	set_setting_value(t_config *settings, char *line)
{
	char	*value;

	value = find_value(line);
	if (!value)
		return ;
	if (strncasecmp(line, "width", 5) == 0)
		settings->width = atoi(value);
	else if (strncasecmp(line, "height", 6) == 0)
		settings->height = atoi(value);
	else if (strncasecmp(line, "shape", 5) == 0)
	{
		free(settings->shape);
		settings->shape = strdup(value);
	}
	else if (strncasecmp(line, "wall_color", 10) == 0)
	{
		free(settings->wall_color);
		settings->wall_color = strdup(value);
	}
	else if (strncasecmp(line, "flag_color", 10) == 0)
	{
		free(settings->flag_color);
		settings->flag_color = strdup(value);
	}
	else if (strncasecmp(line, "path_color", 10) == 0)
	{
		free(settings->path_color);
		settings->path_color = strdup(value);
	}
	else if (strncasecmp(line, "generation_algorithm", 20) == 0)
	{
		free(settings->generation_algorithm);
		settings->generation_algorithm = strdup(value);
	}
	else if (strncasecmp(line, "solver_algorithm", 16) == 0)
	{
		free(settings->solver_algorithm);
		settings->solver_algorithm = strdup(value);
	}
	free(value);
}

t_config	*parse_settings(FILE *f)
{
	t_config	*settings;
	char		line[256];
	char		*trimmed;

	settings = (t_config *)malloc(sizeof(t_config));
	if (!settings)
		return (NULL);
	set_default_config(settings);
	rewind(f);
	while (fgets(line, sizeof(line), f) != NULL)
	{
		trimmed = trim(line);
		if (!trimmed || trimmed[0] == '\0' || is_comment_line(trimmed))
			continue ;
		set_setting_value(settings, trimmed);
	}
	if (settings->wall_color && settings->flag_color
		&& color_from_name(settings->wall_color, -1)
		== color_from_name(settings->flag_color, -2))
	{
		free(settings->flag_color);
		if (strcasecmp(settings->wall_color, "yellow") == 0)
			settings->flag_color = strdup("blue");
		else
			settings->flag_color = strdup("yellow");
	}
	validate_non_white_colors(settings);
	return (settings);
}

t_maze	*parse_output(FILE *f, t_cell *path, int steps, int width, int height)
{
	t_maze	*maze;
	char	line[256];
	size_t	len;

	maze = (t_maze *)malloc(sizeof(t_maze));
	if (!maze)
		return (NULL);
	memset(maze, 0, sizeof(t_maze));
	maze->gen_path = path;
	maze->gen_total_steps = steps;
	maze->width = width;
	maze->height = height;
	rewind(f);
	maze->grid = fill_grid(f, width, height);
	fgets(line, sizeof(line), f);
	if (fgets(line, sizeof(line), f) != NULL)
		maze->entry = parse_coordinates(line);
	if (fgets(line, sizeof(line), f) != NULL)
		maze->exit = parse_coordinates(line);
	if (fgets(line, sizeof(line), f) != NULL)
	{
		len = strlen(line);
		if (len > 0 && line[len - 1] == '\n')
			line[len - 1] = '\0';
		maze->solution = (char *)malloc(strlen(line) + 1);
		if (maze->solution)
		{
			strcpy(maze->solution, line);
			maze->solution_len = strlen(line);
		}
	}
	return (maze);
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
	int		i;
	int		x;
	int		y;
	char	line[256];

	i = 0;
	rewind(f);
	while (fgets(line, sizeof(line), f) != NULL)
	{
		if (sscanf(line, "%d %d", &x, &y) == 2)
			i++;
	}
	cells = (t_point *)malloc(sizeof(t_point) * (i + 1));
	if (!cells)
		return (NULL);
	rewind(f);
	i = 0;
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
	return (cells);
}
