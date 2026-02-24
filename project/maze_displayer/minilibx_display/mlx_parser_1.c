/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   mlx_parser_1.c                                     :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: aabi-mou <aabi-mou@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/02/24 01:18:11 by aabi-mou          #+#    #+#             */
/*   Updated: 2026/02/24 03:05:23 by aabi-mou         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <mlx_helper.h>

static void	set_visual_value(t_config *settings, char *line, char *value)
{
	if (strncasecmp(line, "shape", 5) == 0)
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
}

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
	else
		set_visual_value(settings, line, value);
	free(value);
}

static void	ensure_distinct_flag_color(t_config *settings)
{
	if (settings->wall_color && settings->flag_color
		&& color_from_name(settings->wall_color,
			-1) == color_from_name(settings->flag_color, -2))
	{
		free(settings->flag_color);
		if (strcasecmp(settings->wall_color, "yellow") == 0)
			settings->flag_color = strdup("blue");
		else
			settings->flag_color = strdup("yellow");
	}
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
		if (trimmed && trimmed[0] != '\0' && !is_comment_line(trimmed))
			set_setting_value(settings, trimmed);
	}
	ensure_distinct_flag_color(settings);
	validate_non_white_colors(settings);
	return (settings);
}
