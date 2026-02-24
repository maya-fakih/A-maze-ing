/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   mlx_helper_3.c                                     :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: aabi-mou <aabi-mou@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/02/24 01:33:53 by aabi-mou          #+#    #+#             */
/*   Updated: 2026/02/24 13:50:12 by aabi-mou         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <mlx_helper.h>

void	copy_runtime_paths(t_app *app, char **argv)
{
	snprintf(app->config_file, sizeof(app->config_file), "%s", argv[1]);
	snprintf(app->path_file, sizeof(app->path_file), "%s", argv[2]);
	snprintf(app->output_file, sizeof(app->output_file), "%s", argv[3]);
	snprintf(app->logo_file, sizeof(app->logo_file), "%s", argv[4]);
}

void	parse_line(t_cell *path, char *line)
{
	char	is_sol_str[10];
	int		x;
	int		y;
	int		maze_val;

	if (sscanf(line, "%d %d %d %s", &x, &y, &maze_val, is_sol_str) == 4)
	{
		path->point.x = x;
		path->point.y = y;
		path->value = maze_val;
		path->is_sol = (strcmp(is_sol_str, "True") == 0);
	}
}

static t_parsed	parse_files_stage1(FILE *config_file, FILE *path_file,
		FILE *logo_file)
{
	t_parsed	p;

	p = (t_parsed){0};
	p.cfg = parse_settings(config_file);
	if (!p.cfg)
		error("Error parsing config file.\n");
	p.gen_path = parse_path(path_file, &p.gen_path_count);
	if (!p.gen_path)
	{
		free(p.cfg);
		error("Error parsing generation path.\n");
	}
	p.logo_cells = parse_logo_cells(logo_file, &p.logo_count);
	if (!p.logo_cells)
	{
		free(p.cfg);
		free(p.gen_path);
		error("Error parsing logo file.\n");
	}
	return (p);
}

static void	parse_files_stage2(t_parsed *p, FILE *output_file)
{
	t_parse_opts	opts;

	opts.path = p->gen_path;
	opts.steps = p->gen_path_count;
	opts.width = p->cfg->width;
	opts.height = p->cfg->height;
	p->maze = parse_output(output_file, &opts);
	if (!p->maze)
	{
		free(p->cfg);
		free(p->gen_path);
		free(p->logo_cells);
		error("Error while parsing display files.\n");
	}
	p->maze->logo_cells = p->logo_cells;
	p->maze->logo_count = p->logo_count;
}

t_parsed	parse_files(FILE *config_file, FILE *path_file, FILE *output_file,
		FILE *logo_file)
{
	t_parsed	p;

	p = parse_files_stage1(config_file, path_file, logo_file);
	parse_files_stage2(&p, output_file);
	return (p);
}
