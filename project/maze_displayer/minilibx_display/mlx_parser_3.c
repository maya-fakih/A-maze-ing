/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   mlx_parser_3.c                                     :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: aabi-mou <aabi-mou@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/02/24 03:45:00 by aabi-mou          #+#    #+#             */
/*   Updated: 2026/02/24 03:05:31 by aabi-mou         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <mlx_helper.h>

static void	parse_solution_line(t_maze *maze, char *line)
{
	size_t	len;

	len = strlen(line);
	if (len > 0 && line[len - 1] == '\n')
		line[len - 1] = '\0';
	maze->solution = strdup(line);
	if (maze->solution)
		maze->solution_len = strlen(line);
}

t_maze	*parse_output(FILE *f, t_parse_opts *opts)
{
	t_maze	*maze;
	char	line[256];

	if (!opts)
		return (NULL);
	maze = (t_maze *)malloc(sizeof(t_maze));
	if (!maze)
		return (NULL);
	memset(maze, 0, sizeof(t_maze));
	maze->gen_path = opts->path;
	maze->gen_total_steps = opts->steps;
	maze->width = opts->width;
	maze->height = opts->height;
	rewind(f);
	maze->grid = fill_grid(f, maze->width, maze->height);
	fgets(line, sizeof(line), f);
	if (fgets(line, sizeof(line), f) != NULL)
		maze->entry = parse_coordinates(line);
	if (fgets(line, sizeof(line), f) != NULL)
		maze->exit = parse_coordinates(line);
	if (fgets(line, sizeof(line), f) != NULL)
		parse_solution_line(maze, line);
	return (maze);
}
