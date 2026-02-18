/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   mlx_helper_2.c                                     :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: aabi-mou <aabi-mou@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/02/18 18:11:34 by aabi-mou          #+#    #+#             */
/*   Updated: 2026/02/18 18:12:38 by aabi-mou         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <mlx_helper.h>

// check if the current line is a comment
bool	is_comment_line(const char *line)
{
	if (!line)
		return (false);
	while (*line && isspace((unsigned char)*line))
		line++;
	return (*line == '#');
}

// find the value of a setting (what is after the =)
char	*find_value(char *line)
{
	int		i;
	int		start;
	int		size;
	char	*val;
	char	*trimmed_val;

	if (line == NULL)
		return (NULL);
	i = 0;
	while (line[i] && line[i] != '=')
		i++;
	if (line[i] != '=')
		return (NULL);
	i++;
	start = i;
	size = 0;
	while (line[i])
	{
		i++;
		size++;
	}
	val = (char *)malloc(sizeof(char) * (size + 1));
	if (!val)
		return (NULL);
	i = 0;
	while (line[start])
		val[i++] = line[start++];
	val[i] = '\0';
	trimmed_val = strdup(trim(val));
	return (trimmed_val);
}

void	parse_line(t_cell *path, char *line)
{
	int		x;
	int		y;
	int		maze_val;
	char	is_sol_str[10];

	if (sscanf(line, "%d %d %d %s", &x, &y, &maze_val, is_sol_str) == 4)
	{
		path->point.x = x;
		path->point.y = y;
		path->value = maze_val;
		path->is_sol = (strcmp(is_sol_str, "True") == 0);
	}
}

char	**fill_grid(FILE *f, int w, int h)
{
	int		i;
	int		j;
	char	**grid;
	char	line[256];

	grid = (char **)malloc(sizeof(char *) * h);
	if (!grid)
		return (NULL);
	i = 0;
	while (i < h)
	{
		grid[i] = (char *)malloc(sizeof(char) * (w + 1));
		if (!grid[i])
		{
			j = 0;
			while (j < i)
			{
				free(grid[j]);
				j++;
			}
			free(grid);
			return (NULL);
		}
		if (fgets(line, sizeof(line), f) == NULL)
		{
			j = 0;
			while (j <= i)
			{
				free(grid[j]);
				j++;
			}
			free(grid);
			return (NULL);
		}
		if (line[0] == '\n' || line[0] == '\0')
		{
			free(grid[i]);
			continue ;
		}
		j = 0;
		while (j < w && line[j] && line[j] != '\n')
		{
			grid[i][j] = line[j];
			j++;
		}
		grid[i][j] = '\0';
		i++;
	}
	return (grid);
}

t_point	parse_coordinates(const char *line)
{
	t_point	point;

	point.x = 0;
	point.y = 0;
	if (sscanf(line, "%d,%d", &point.x, &point.y) != 2)
	{
		printf("Error parsing coordinates: %s\n", line);
	}
	return (point);
}
