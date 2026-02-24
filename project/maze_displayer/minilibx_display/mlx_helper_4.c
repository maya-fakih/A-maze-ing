/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   mlx_helper_4.c                                     :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: aabi-mou <aabi-mou@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/02/24 02:31:56 by aabi-mou          #+#    #+#             */
/*   Updated: 2026/02/24 03:05:17 by aabi-mou         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <mlx_helper.h>

static char	*return_value(char *line, int size, int start)
{
	char	*val;
	char	*trimmed_val;
	int		i;

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

char	*find_value(char *line)
{
	int		i;
	int		start;
	int		size;
	char	*val;

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
	val = return_value(line, size, start);
	return (val);
}
