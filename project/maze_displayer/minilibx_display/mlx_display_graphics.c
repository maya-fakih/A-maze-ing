/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   mlx_display_graphics.c                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: aabi-mou <aabi-mou@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/02/24 04:25:00 by aabi-mou          #+#    #+#             */
/*   Updated: 2026/02/24 03:04:58 by aabi-mou         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <X11/Xlib.h>
#include <mlx_helper.h>

typedef struct s_mlx_win
{
	Window	window;
	void	*gc;
	void	*next;
}			t_mlx_win;

typedef struct s_mlx_xvar
{
	Display	*display;
	Window	root;
}			t_mlx_xvar;

int	close_window(t_app *app)
{
	mlx_destroy_window(app->mlx, app->win);
	exit(0);
}

static void	center_window(t_app *app)
{
	t_mlx_xvar	*xvar;
	t_mlx_win	*win;
	int			screen_w;
	int			screen_h;

	xvar = (t_mlx_xvar *)app->mlx;
	win = (t_mlx_win *)app->win;
	mlx_get_screen_size(app->mlx, &screen_w, &screen_h);
	XMoveWindow(xvar->display, win->window, (screen_w - app->window_width) / 2,
		(screen_h - app->window_height) / 2);
	XFlush(xvar->display);
}

void	init_graphics(t_app *app)
{
	app->maze_px_w = app->maze.width * app->config.cell_size;
	app->maze_px_h = app->maze.height * app->config.cell_size;
	app->panel_width = 360;
	app->panel_x = app->maze_px_w;
	app->window_width = app->maze_px_w + app->panel_width;
	app->window_height = app->maze_px_h;
	if (app->window_height < 640)
		app->window_height = 640;
	app->mlx = mlx_init();
	app->win = mlx_new_window(app->mlx, app->window_width, app->window_height,
			APP_TITLE);
	app->img.img = mlx_new_image(app->mlx, app->window_width,
			app->window_height);
	app->img.addr = mlx_get_data_addr(app->img.img, &app->img.bpp,
			&app->img.line_len, &app->img.endian);
	center_window(app);
	mlx_hook(app->win, 17, 0, (int (*)(void *))close_window, app);
}
