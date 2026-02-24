/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   mlx_display_reload.c                               :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: aabi-mou <aabi-mou@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/02/24 04:25:00 by aabi-mou          #+#    #+#             */
/*   Updated: 2026/02/24 17:22:56 by aabi-mou         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <mlx_helper.h>

static void	free_maze(t_app *app)
{
	int	y;

	y = 0;
	while (app->maze.grid && y < app->maze.height)
		free(app->maze.grid[y++]);
	free(app->maze.grid);
	free(app->maze.solution);
	free(app->maze.gen_path);
	free(app->maze.logo_cells);
	app->maze.grid = NULL;
	app->maze.solution = NULL;
	app->maze.gen_path = NULL;
	app->maze.logo_cells = NULL;
}

static int	open_runtime_files(t_app *app, t_runtime_files *f)
{
	f->config = fopen(app->config_file, "r");
	f->path = fopen(app->path_file, "r");
	f->output = fopen(app->output_file, "r");
	f->logo = fopen(app->logo_file, "r");
	if (!f->config || !f->path || !f->output || !f->logo)
	{
		if (f->config)
			fclose(f->config);
		if (f->path)
			fclose(f->path);
		if (f->output)
			fclose(f->output);
		if (f->logo)
			fclose(f->logo);
		return (1);
	}
	return (0);
}

void	reload_from_files(t_app *app)
{
	t_runtime_files	f;
	t_parsed		p;

	if (open_runtime_files(app, &f) != 0)
		return ;
	p = parse_files(f.config, f.path, f.output, f.logo);
	fclose(f.config);
	fclose(f.path);
	fclose(f.output);
	fclose(f.logo);
	free(app->config.shape);
	free(app->config.wall_color);
	free(app->config.flag_color);
	free(app->config.path_color);
	free(app->config.generation_algorithm);
	free(app->config.solver_algorithm);
	free_maze(app);
	app->config = *p.cfg;
	app->maze = *p.maze;
	free(p.cfg);
	free(p.maze);
}

static const char	*cfg_basename(const char *path)
{
	const char	*base;

	base = strrchr(path, '/');
	if (!base)
		base = strrchr(path, '\\');
	if (!base)
		return (path);
	return (base + 1);
}

void	regenerate_maze(t_app *app)
{
	char	command[512];

	snprintf(command, sizeof(command),
		"AMAZE_NO_DISPLAY=1 DISPLAY= python3 a_maze_ing.py %s >/dev/null 2>&1",
		cfg_basename(app->config_file));
	if (system(command) != 0)
		return ;
	reload_from_files(app);
	app->phase = 0;
	app->anim_index = 0;
	app->frame = 0;
	animate_generation(app);
}
