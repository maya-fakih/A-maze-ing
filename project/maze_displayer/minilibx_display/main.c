/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   main.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: aabi-mou <aabi-mou@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/02/18 18:07:08 by aabi-mou          #+#    #+#             */
/*   Updated: 2026/02/20 23:49:00 by codex             ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <mlx_helper.h>

static void	copy_runtime_paths(t_app *app, char **argv)
{
	snprintf(app->config_file, sizeof(app->config_file),
		"configuration/%s", argv[1]);
	snprintf(app->path_file, sizeof(app->path_file),
		"configuration/%s", argv[2]);
	snprintf(app->output_file, sizeof(app->output_file), "%s", argv[3]);
	snprintf(app->logo_file, sizeof(app->logo_file),
		"configuration/%s", argv[4]);
}

t_app	*init_app(FILE *config_file, FILE *path_file, FILE *output_file,
	FILE *logo_file,
	char **argv)
{
	t_app		*app;
	t_cell		*gen_path;
	t_point		*logo_cells;
	int			gen_path_count;
	int			logo_count;
	t_config	*cfg;
	t_maze		*maze;

	app = (t_app *)malloc(sizeof(t_app));
	if (!app)
		return (NULL);
	memset(app, 0, sizeof(t_app));
	cfg = parse_settings(config_file);
	if (!cfg)
		error("Error parsing config file.");
	gen_path = parse_path(path_file, &gen_path_count);
	if (!gen_path)
		error("Error parsing generation path.");
	logo_cells = parse_logo_cells(logo_file, &logo_count);
	if (!logo_cells)
		error("Error parsing logo file.");
	maze = parse_output(output_file, gen_path, gen_path_count,
			cfg->width, cfg->height);
	if (!maze)
		error("Error while parsing display files.");
	maze->logo_cells = logo_cells;
	maze->logo_count = logo_count;
	app->config = *cfg;
	free(cfg);
	app->maze = *maze;
	free(maze);
	copy_runtime_paths(app, argv);
	app->phase = 2;
	app->anim_index = 0;
	app->frame = 0;
	app->show_path = true;
	return (app);
}

void	draw_maze(t_app *app)
{
	init_graphics(app);
	redraw_base_scene(app);
	mlx_put_image_to_window(app->mlx, app->win, app->img.img, 0, 0);
	draw_button_panel(app);
	mlx_loop_hook(app->mlx, update, app);
	mlx_mouse_hook(app->win, mouse_hook, app);
	mlx_hook(app->win, 17, 0, (int (*)(void *))close_window, app);
	mlx_loop(app->mlx);
}

int	main(int argc, char **argv)
{
	FILE	*config_file;
	FILE	*output_file;
	FILE	*path_file;
	FILE	*logo_file;
	t_app	*app;
	char	path[256];

	if (argc != 5)
		error("Error! Provide config, path, output and logo files.\n");
	snprintf(path, sizeof(path), "configuration/%s", argv[1]);
	config_file = fopen(path, "r");
	if (config_file == NULL)
		error("Error opening config file.\n");
	snprintf(path, sizeof(path), "configuration/%s", argv[2]);
	path_file = fopen(path, "r");
	if (path_file == NULL)
		error("Error opening generation path file.\n");
	output_file = fopen(argv[3], "r");
	if (output_file == NULL)
		error("Error opening output file.\n");
	snprintf(path, sizeof(path), "configuration/%s", argv[4]);
	logo_file = fopen(path, "r");
	if (logo_file == NULL)
		error("Error opening logo file.\n");
	app = init_app(config_file, path_file, output_file, logo_file, argv);
	if (app == NULL)
		error("Error!");
	draw_maze(app);
	fclose(config_file);
	fclose(path_file);
	fclose(output_file);
	fclose(logo_file);
	return (0);
}
