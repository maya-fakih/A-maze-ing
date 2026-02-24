/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   mlx_helper_1.c                                     :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: aabi-mou <aabi-mou@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/02/18 18:10:22 by aabi-mou          #+#    #+#             */
/*   Updated: 2026/02/24 13:35:43 by aabi-mou         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <mlx_helper.h>

bool	is_comment_line(const char *line)
{
	if (!line)
		return (false);
	while (*line && isspace((unsigned char)*line))
		line++;
	return (*line == '#');
}

void	error(const char *s)
{
	printf("%s\n", s);
	exit(1);
}

char	*trim(char *str)
{
	char	*end;

	while (isspace((unsigned char)*str))
		str++;
	if (*str == 0)
		return (str);
	end = str + strlen(str) - 1;
	while (end > str && isspace((unsigned char)*end))
		end--;
	*(end + 1) = '\0';
	return (str);
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

int	open_file(FILE **f, char *arg)
{
	*f = fopen(arg, "r+");
	if (*f == NULL)
		return (0);
	return (1);
}
