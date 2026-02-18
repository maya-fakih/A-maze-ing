/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   mlx_parser.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: aabi-mou <aabi-mou@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/02/18 18:04:45 by aabi-mou          #+#    #+#             */
/*   Updated: 2026/02/18 18:06:12 by aabi-mou         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <mlx_helper.h>

t_config	*parse_settings(FILE *f)
{
	t_config	*settings;
	char		line[256];
	char		*value;

	settings = (t_config *)malloc(sizeof(t_config));
	if (!settings)
		return (NULL);
	while (fgets(line, sizeof(line), f) != NULL)
	{
		if (is_comment_line(line))
			continue ;
		if (strcasestr(line, "width") != NULL)
		{
			value = find_value(line);
			settings->width = atoi(value);
		}
		else if (strcasestr(line, "height") != NULL)
		{
			value = find_value(line);
			settings->height = atoi(value);
		}
		else if (strcasestr(line, "shape") != NULL)
		{
			value = find_value(line);
			settings->shape = value;
		}
		else if (strcasestr(line, "wall_color") != NULL)
		{
			value = find_value(line);
			settings->wall_color = value;
		}
		else if (strcasestr(line, "flag_color") != NULL)
		{
			value = find_value(line);
			settings->flag_color = value;
		}
	}
	if (settings->shape == NULL)
		settings->shape = "square";
	if (settings->wall_color == NULL)
		settings->wall_color = "blue";
	if (settings->flag_color == NULL)
		settings->flag_color = "grey";
	settings->cell_size = 20;
	settings->animation_speed = 5;
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
	maze->gen_path = path;
	maze->gen_total_steps = steps;
	maze->width = width;
	maze->height = height;
	maze->grid = fill_grid(f, width, height);
	fgets(line, sizeof(line), f);
	if (fgets(line, sizeof(line), f) != NULL)
		maze->entry = parse_coordinates(line);
	if (fgets(line, sizeof(line), f) != NULL)
		maze->exit = parse_coordinates(line);
	if (fgets(line, sizeof(line), f) != NULL)
	{
		len = strlen(line);
		if (line[len - 1] == '\n')
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
