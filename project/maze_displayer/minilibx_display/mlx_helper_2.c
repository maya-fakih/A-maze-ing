/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   mlx_helper_2.c                                     :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: aabi-mou <aabi-mou@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/02/18 18:11:34 by aabi-mou          #+#    #+#             */
/*   Updated: 2026/02/24 03:05:12 by aabi-mou         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <mlx_helper.h>

static int	process_grid_row(FILE *f, char **grid, int i, int w)
{
	int		j;
	char	line[256];

	if (!grid[i])
		return (-1);
	if (fgets(line, sizeof(line), f) == NULL)
		return (-2);
	if (line[0] == '\n' || line[0] == '\0')
	{
		free(grid[i]);
		return (1);
	}
	j = 0;
	while (j < w && line[j] && line[j] != '\n')
	{
		grid[i][j] = line[j];
		j++;
	}
	grid[i][j] = '\0';
	return (0);
}

static void	free_grid_rows(char **grid, int n)
{
	int	i;

	if (!grid)
		return ;
	i = 0;
	while (i < n)
	{
		if (grid[i])
			free(grid[i]);
		i++;
	}
	free(grid);
}

static int	process_column(FILE *f, char **grid, int i, int w)
{
	int	rc;

	if (!grid[i])
	{
		free_grid_rows(grid, i);
		return (-1);
	}
	rc = process_grid_row(f, grid, i, w);
	if (rc == -1)
	{
		free_grid_rows(grid, i);
		return (-1);
	}
	if (rc == -2)
	{
		free_grid_rows(grid, i + 1);
		return (-1);
	}
	return (rc);
}

char	**fill_grid(FILE *f, int w, int h)
{
	int		i;
	char	**grid;
	int		rc;

	grid = (char **)malloc(sizeof(char *) * h);
	if (!grid)
		return (NULL);
	i = 0;
	while (i < h)
	{
		grid[i] = (char *)malloc(sizeof(char) * (w + 1));
		rc = process_column(f, grid, i, w);
		if (rc == -1)
			return (NULL);
		if (rc == 1)
			continue ;
		i++;
	}
	return (grid);
}
