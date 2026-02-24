/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   mlx_display_mouse_2.c                              :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: aabi-mou <aabi-mou@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/02/24 15:44:52 by aabi-mou          #+#    #+#             */
/*   Updated: 2026/02/24 15:57:01 by aabi-mou         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <mlx_helper.h>

static const char	*get_next_gen(t_app *app)
{
	const char	*gen_options[4] = {"dfs", "bfs", "prim", "huntkill"};

	return (next_option(app->config.generation_algorithm, gen_options, 4,
			NULL));
}

static void	apply_gen_change(t_app *app)
{
	const char	*next;

	next = get_next_gen(app);
	if (!next)
		return ;
	update_config_value(app->config_file, "GENERATION_ALGORITHM", next);
}

static const char	*get_next_solver(t_app *app)
{
	const char	*solver_options[4] = {"dfs", "bfs", "a*", "ucs"};

	return (next_option(app->config.solver_algorithm, solver_options, 4, NULL));
}

static void	apply_solver_change(t_app *app)
{
	const char	*next;

	next = get_next_solver(app);
	if (!next)
		return ;
	update_config_value(app->config_file, "SOLVER_ALGORITHM", next);
}

void	apply_click(t_app *app, int idx)
{
	if (idx == 0)
		regenerate_maze(app);
	if (idx == 1)
	{
		app->show_path = !app->show_path;
		redraw_base_scene(app);
	}
	if (idx == 2 || idx == 3 || idx == 4)
	{
		apply_color_update(app, idx);
		redraw_base_scene(app);
	}
	if (idx == 5)
		apply_shape_change(app);
	if (idx == 6)
		apply_gen_change(app);
	if (idx == 7)
		apply_solver_change(app);
	if (idx >= 5)
		regenerate_maze(app);
}
