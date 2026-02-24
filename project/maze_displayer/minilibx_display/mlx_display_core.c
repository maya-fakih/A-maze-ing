/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   mlx_display_core.c                                 :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: aabi-mou <aabi-mou@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/02/24 04:25:00 by aabi-mou          #+#    #+#             */
/*   Updated: 2026/02/24 03:04:55 by aabi-mou         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <mlx_helper.h>

int	color_from_name(const char *name, int fallback)
{
	if (!name)
		return (fallback);
	if (strcasecmp(name, "black") == 0)
		return (0x1E1E1E);
	if (strcasecmp(name, "white") == 0 || strcasecmp(name, "bright_white") == 0)
		return (0xFFFFFF);
	if (strcasecmp(name, "red") == 0 || strcasecmp(name, "light_red") == 0)
		return (0xE53935);
	if (strcasecmp(name, "green") == 0 || strcasecmp(name, "light_green") == 0)
		return (0x43A047);
	if (strcasecmp(name, "yellow") == 0 || strcasecmp(name,
			"light_yellow") == 0)
		return (0xFDD835);
	if (strcasecmp(name, "blue") == 0 || strcasecmp(name, "light_blue") == 0)
		return (0x1E88E5);
	if (strcasecmp(name, "magenta") == 0 || strcasecmp(name,
			"light_magenta") == 0)
		return (0xD81B60);
	if (strcasecmp(name, "cyan") == 0 || strcasecmp(name, "light_cyan") == 0)
		return (0x00ACC1);
	if (strcasecmp(name, "orange") == 0)
		return (0xFB8C00);
	if (strcasecmp(name, "grey") == 0 || strcasecmp(name, "gray") == 0)
		return (0x6D6D6D);
	return (fallback);
}

void	put_pixel(t_img *img, int x, int y, int color)
{
	char	*dst;

	if (x < 0 || y < 0)
		return ;
	dst = img->addr + (y * img->line_len + x * (img->bpp / 8));
	*(unsigned int *)dst = color;
}

void	fill_rect(t_app *app, t_rect *r)
{
	int	px;
	int	py;

	if (!r)
		return ;
	py = r->y;
	while (py < r->y + r->h)
	{
		px = r->x;
		while (px < r->x + r->w)
		{
			put_pixel(&app->img, px, py, r->color);
			px++;
		}
		py++;
	}
}

void	draw_square(t_app *app, int gx, int gy, int color)
{
	int	px;
	int	py;
	int	x;
	int	y;

	px = gx * app->config.cell_size;
	py = gy * app->config.cell_size;
	y = 0;
	while (y < app->config.cell_size)
	{
		x = 0;
		while (x < app->config.cell_size)
		{
			put_pixel(&app->img, px + x, py + y, color);
			x++;
		}
		y++;
	}
}

void	draw_star_marker(t_app *app, int gx, int gy, int color)
{
	int	cx;
	int	cy;
	int	size;
	int	i;

	size = app->config.cell_size;
	cx = gx * size + size / 2;
	cy = gy * size + size / 2;
	put_pixel(&app->img, cx, cy, color);
	i = 1;
	while (i <= (size / 6 + 1))
	{
		put_pixel(&app->img, cx + i, cy, color);
		put_pixel(&app->img, cx - i, cy, color);
		put_pixel(&app->img, cx, cy + i, color);
		put_pixel(&app->img, cx, cy - i, color);
		i++;
	}
}
