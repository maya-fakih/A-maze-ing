/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   mlx_display_config.c                               :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: aabi-mou <aabi-mou@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/02/24 04:25:00 by aabi-mou          #+#    #+#             */
/*   Updated: 2026/02/24 15:18:06 by aabi-mou         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <mlx_helper.h>

static int	line_key_matches(char *line, const char *key)
{
	char	key_buf[256];
	char	*eq;
	size_t	key_len;

	eq = strchr(line, '=');
	if (!eq || is_comment_line(line))
		return (0);
	memset(key_buf, 0, sizeof(key_buf));
	key_len = (size_t)(eq - line);
	if (key_len >= sizeof(key_buf))
		key_len = sizeof(key_buf) - 1;
	memcpy(key_buf, line, key_len);
	strcpy(key_buf, trim(key_buf));
	return (strcasecmp(key_buf, key) == 0);
}

static int	rewrite_config(FILE *in, FILE *out, const char *key,
		const char *value)
{
	char	line[512];
	int		found;

	found = 0;
	while (fgets(line, sizeof(line), in))
	{
		if (line_key_matches(line, key))
		{
			if (!found)
				fprintf(out, "%s=%s\n", key, value);
			found = 1;
		}
		else
			fputs(line, out);
	}
	if (!found)
		fprintf(out, "\n%s=%s", key, value);
	return (0);
}

int	update_config_value(const char *config_path, const char *key,
		const char *value)
{
	FILE	*in;
	FILE	*out;
	char	tmp_path[320];

	snprintf(tmp_path, sizeof(tmp_path), "%s.tmp", config_path);
	in = fopen(config_path, "r");
	out = fopen(tmp_path, "w");
	if (!in || !out)
	{
		if (in)
			fclose(in);
		if (out)
			fclose(out);
		return (1);
	}
	rewrite_config(in, out, key, value);
	fclose(in);
	fclose(out);
	remove(config_path);
	rename(tmp_path, config_path);
	return (0);
}
