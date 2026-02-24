/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   mlx_display_mouse_3.c                              :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: aabi-mou <aabi-mou@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/02/24 15:54:30 by aabi-mou          #+#    #+#             */
/*   Updated: 2026/02/24 15:57:35 by aabi-mou         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <mlx_helper.h>

void	apply_shape_change(t_app *app)
{
	const char	*next;
	const char	*shape_options[4] = {"square", "heart", "flower", "star"};

	next = next_option(app->config.shape, shape_options, 4, NULL);
	if (!next)
		return ;
	update_config_value(app->config_file, "SHAPE", next);
	free(app->config.shape);
	app->config.shape = strdup(next);
}

int	mouse_hook(int button, int x, int y, void *param)
{
	t_app		*app;
	t_button	btns[BTN_COUNT];
	int			i;

	if (button != 1)
		return (0);
	app = (t_app *)param;
	build_buttons(app, btns);
	i = 0;
	while (i < BTN_COUNT)
	{
		if (x >= btns[i].x && x <= btns[i].x + btns[i].w && y >= btns[i].y
			&& y <= btns[i].y + btns[i].h)
		{
			apply_click(app, i);
			mlx_put_image_to_window(app->mlx, app->win, app->img.img, 0, 0);
			draw_button_panel(app);
			return (0);
		}
		i++;
	}
	return (0);
}
