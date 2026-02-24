/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   mlx_display_buttons.c                              :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: aabi-mou <aabi-mou@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/02/24 04:25:00 by aabi-mou          #+#    #+#             */
/*   Updated: 2026/02/24 03:06:35 by aabi-mou         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <mlx_helper.h>

void	build_buttons(t_app *app, t_button *btns)
{
	int			i;
	const char	*labels[BTN_COUNT];

	labels[0] = "Regenerate maze";
	labels[1] = "Show / hide path";
	labels[2] = "Change wall color";
	labels[3] = "Change flag color";
	labels[4] = "Change path color";
	labels[5] = "Change shape";
	labels[6] = "Change generation algo";
	labels[7] = "Change solver algo";
	btns[0] = (t_button){app->panel_x + PANEL_MARGIN, PANEL_MARGIN,
		app->panel_width - (PANEL_MARGIN * 2), BTN_HEIGHT, 0x5E2CA5, labels[0]};
	i = 1;
	while (i < BTN_COUNT)
	{
		btns[i] = btns[0];
		btns[i].y = btns[i - 1].y + BTN_HEIGHT + BTN_GAP;
		btns[i].label = labels[i];
		i++;
	}
}

static void	draw_buttons(t_app *app, t_button *btns)
{
	int		i;
	t_rect	r;

	i = 0;
	mlx_set_font(app->mlx, app->win, "10x20");
	while (i < BTN_COUNT)
	{
		r = (t_rect){btns[i].x, btns[i].y, btns[i].w, btns[i].h, btns[i].color};
		fill_rect(app, &r);
		mlx_string_put(app->mlx, app->win, btns[i].x + BTN_LABEL_XPAD, btns[i].y
			+ BTN_LABEL_YPAD, 0xFFFFFF, (char *)btns[i].label);
		i++;
	}
}

static void	draw_info(t_app *app, t_button *btns)
{
	char	info[160];
	int		y;

	y = btns[BTN_COUNT - 1].y + BTN_HEIGHT + BTN_GAP + 12;
	snprintf(info, sizeof(info), "Wall: %s | Flag: %s", app->config.wall_color,
		app->config.flag_color);
	mlx_string_put(app->mlx, app->win, btns[0].x, y, 0x1E1E1E, info);
	y += 18;
	snprintf(info, sizeof(info), "Path: %s | Shape: %s", app->config.path_color,
		app->config.shape);
	mlx_string_put(app->mlx, app->win, btns[0].x, y, 0x1E1E1E, info);
	y += 18;
	snprintf(info, sizeof(info), "Gen: %s | Solver: %s",
		app->config.generation_algorithm, app->config.solver_algorithm);
	mlx_string_put(app->mlx, app->win, btns[0].x, y, 0x1E1E1E, info);
}

void	draw_button_panel(t_app *app)
{
	t_button	btns[BTN_COUNT];

	build_buttons(app, btns);
	fill_rect(app, &(t_rect){app->panel_x, 0, app->panel_width,
		app->window_height, PANEL_BG});
	draw_buttons(app, btns);
	draw_info(app, btns);
}
