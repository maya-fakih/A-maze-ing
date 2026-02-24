/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   main.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: aabi-mou <aabi-mou@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/02/21 13:45:59 by aabi-mou          #+#    #+#             */
/*   Updated: 2026/02/24 03:01:29 by aabi-mou         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <mlx_helper.h>

t_app	*init_app_options(t_config *cfg, t_cell *gen_path, t_point *logo_cells,
		t_maze *maze)
{
	t_app	*app;

	(void)gen_path;
	(void)logo_cells;
	app = (t_app *)malloc(sizeof(t_app));
	memset(app, 0, sizeof(t_app));
	if (!app)
		error("Error creating app!\n");
	app->config = *cfg;
	app->maze = *maze;
	free(cfg);
	free(maze);
	app->phase = 0;
	app->anim_index = 0;
	app->frame = 0;
	app->show_path = true;
	return (app);
}

t_app	*init_app(FILE *config_file, FILE *path_file, FILE *output_file,
		FILE *logo_file)
{
	t_parsed	p;

	p = parse_files(config_file, path_file, output_file, logo_file);
	return (init_app_options(p.cfg, p.gen_path, p.logo_cells, p.maze));
}

void	draw_maze(t_app *app)
{
	init_graphics(app);
	animate_generation(app);
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

	if (argc != 5)
		error("Error! Provide config, path, output and logo files.\n");
	if (!open_file(&config_file, argv[1]) || !open_file(&output_file, argv[2])
		|| !open_file(&path_file, argv[3]) || !open_file(&logo_file, argv[4]))
		error("Error opening file!\n");
	app = init_app(config_file, path_file, output_file, logo_file);
	copy_runtime_paths(app, argv);
	draw_maze(app);
	fclose(config_file);
	fclose(path_file);
	fclose(output_file);
	fclose(logo_file);
	return (0);
}
