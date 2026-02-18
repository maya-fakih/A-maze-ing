/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   main.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: aabi-mou <aabi-mou@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/02/18 18:07:08 by aabi-mou          #+#    #+#             */
/*   Updated: 2026/02/18 18:43:40 by aabi-mou         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <mlx_helper.h>

t_app	*init_app(FILE *config_file, FILE *path_file, FILE *output_file)
{
	t_app	*app;
	t_cell	*gen_path;
	int		gen_path_count;

	app = (t_app *)malloc(sizeof(t_app));
	if (!app)
		return (NULL);
	app->config = *parse_settings(config_file);
	gen_path = parse_path(path_file, &gen_path_count);
	gen_path = parse_path(path_file, &gen_path_count);
	app->maze = *parse_output(output_file, gen_path, gen_path_count,
			app->config.width, app->config.height);
	app->phase = 0;
	app->anim_index = 0;
	app->frame = 0;
	return (app);
}

void	draw_maze(t_app *app)
{
	init_graphics(app);
	draw_static_maze(app);
	mlx_put_image_to_window(app->mlx, app->win, app->img.img, 0, 0);
	mlx_loop_hook(app->mlx, update, &app);
	mlx_hook(app->win, 17, 0, (int (*)(void *))close_window, &app);
	mlx_loop(app->mlx);
}

int	main(int argc, char **argv)
{
	FILE	*config_file;
	FILE	*output_file;
	FILE	*path_file;
	t_app	*app;
	char	path[256];

	if (argc != 4)
		error("Error! Provide config file, path file and output file.\n");
	sprintf(path, "configuration/%s", argv[1]);
	config_file = fopen(path, "r+");
	if (config_file == NULL)
		error("Error opening config file.\n");
	memset(&path, 0, sizeof(path));
	sprintf(path, "configuration/%s", argv[2]);
	path_file = fopen(path, "r+");
	if (path_file == NULL)
		error("Error opening generation path file.\n");
	output_file = fopen(argv[3], "r+");
	if (output_file == NULL)
		error("Error opening output file.\n");
	app = init_app(config_file, path_file, output_file);
	if (app == NULL)
		error("Error!");
	draw_maze(app);
	fclose(config_file);
	fclose(path_file);
	fclose(output_file);
	exit(0);
}
