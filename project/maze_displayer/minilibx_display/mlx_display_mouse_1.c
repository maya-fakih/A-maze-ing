/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   mlx_display_mouse_1.c                              :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: aabi-mou <aabi-mou@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/02/24 04:25:00 by aabi-mou          #+#    #+#             */
/*   Updated: 2026/02/24 15:57:29 by aabi-mou         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <mlx_helper.h>

static const char	*g_wall_options[11] = {"blue", "red", "green", "cyan",
	"orange", "grey", "magenta", "yellow", "light_blue", "light_cyan",
	"light_green"};
static const char	*g_flag_options[10] = {"yellow", "magenta", "orange",
	"green", "blue", "red", "cyan", "light_yellow", "light_magenta",
	"light_red"};
static const char	*g_path_options[10] = {"green", "cyan", "yellow",
	"magenta", "orange", "red", "blue", "light_green", "light_cyan",
	"light_magenta"};

const char	*next_option(const char *current, const char **options,
		int count, const char *forbidden)
{
	int	cur;
	int	i;

	cur = 0;
	while (cur < count && (!current || strcasecmp(current, options[cur]) != 0))
		cur++;
	if (cur >= count)
		cur = 0;
	i = 1;
	while (i <= count)
	{
		if (!forbidden || color_from_name(options[(cur + i) % count],
				-1) != color_from_name(forbidden, -2))
			return (options[(cur + i) % count]);
		i++;
	}
	return (options[cur]);
}

static void	set_config_color(char **field, const char *value)
{
	char	*copy;

	copy = strdup(value);
	if (!copy)
		return ;
	free(*field);
	*field = copy;
}

static const char	*get_next_color_for_idx(t_app *app, int idx)
{
	if (idx == 2)
		return (next_option(app->config.wall_color, g_wall_options, 11,
				app->config.flag_color));
	if (idx == 3)
		return (next_option(app->config.flag_color, g_flag_options, 10,
				app->config.wall_color));
	if (idx == 4)
		return (next_option(app->config.path_color, g_path_options, 10, NULL));
	return (NULL);
}

void	apply_color_update(t_app *app, int idx)
{
	const char	*next;

	next = get_next_color_for_idx(app, idx);
	if (!next)
		return ;
	if (idx == 2)
	{
		update_config_value(app->config_file, "WALL_COLOR", next);
		set_config_color(&app->config.wall_color, next);
	}
	if (idx == 3)
	{
		update_config_value(app->config_file, "FLAG_COLOR", next);
		set_config_color(&app->config.flag_color, next);
	}
	if (idx == 4)
	{
		update_config_value(app->config_file, "PATH_COLOR", next);
		set_config_color(&app->config.path_color, next);
	}
}
