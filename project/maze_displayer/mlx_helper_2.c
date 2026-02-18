#include <mlx_helper.h>

// check if the current line is a comment
bool is_comment_line(const char *line)
{
    if (!line)
        return false;
    // Skip leading whitespace
    while (*line && isspace((unsigned char)*line))
        line++;
    // Check if the first non-space character is '#'
    return (*line == '#');
}

// find the value of a setting (what is after the =)
char *find_value(char *line)
{
    int     i;
    int     start;
    int     size;
    char    *val;
    char    *trimmed_val;

    if (line == NULL)
        return (NULL);
    i = 0;
    while (line[i] && line[i] != '=')
        i++;
    if (line[i] != '=')
        return (NULL); // no '=' in line
    i++; // move past '='
    start = i;
    // compute size of value
    size = 0;
    while (line[i])
    {
        i++;
        size++;
    }
    // allocate string
    val = (char *)malloc(sizeof(char) * (size + 1));
    if (!val)
        return (NULL);
    // copy characters
    i = 0;
    while (line[start])
        val[i++] = line[start++];
    val[i] = '\0';
    // trim leading/trailing whitespace
    trimmed_val = strdup(trim(val));
    return (trimmed_val);
}


void parse_line(t_cell *path, char *line)
{
    int     x;
    int     y;
    int     maze_val;
    char    is_sol_str[10];

    // Parse: "12 4 11 False"
    if (sscanf(line, "%d %d %d %s", &x, &y, &maze_val, is_sol_str) == 4)
    {
        path->point.x = x;
        path->point.y = y;
        path->value = maze_val;
        path->is_sol = (strcmp(is_sol_str, "True") == 0);
    }
}

char **fill_grid(FILE *f, int w, int h)
{
	int		i;
	int		j;
    char	**grid;
	char	line[256];

	grid = (char **)malloc(sizeof(char *) * h);
    if (!grid)
        return (NULL);
    i = 0;
    while(i < h)
    {
        grid[i] = (char *)malloc(sizeof(char) * (w + 1));
        if (!grid[i])
        {
            j = 0;
            while(j < i)
            {
                free(grid[j]);
                j++;
            }
            free(grid);
            return (NULL);
		}
		if (fgets(line, sizeof(line), f) == NULL)
		{
			j = 0;
			while(j <= i)
			{
				free(grid[j]);
				j++;
			}
			free(grid);
			return (NULL);
		}
		// Skip empty lines
		if (line[0] == '\n' || line[0] == '\0')
		{
			free(grid[i]);
			continue;
		}
		// Copy line to grid[i], removing newline
		j = 0;
		while(j < w && line[j] && line[j] != '\n')
		{
			grid[i][j] = line[j];
			j++;
		}
		grid[i][j] = '\0';  // Null terminate string
		i++;
	}
	return (grid);
}

t_point parse_coordinates(const char *line)
{
    t_point point;
    
    point.x = 0;
    point.y = 0;
    if (sscanf(line, "%d,%d", &point.x, &point.y) != 2)
    {
        printf("Error parsing coordinates: %s\n", line);
    }
    return (point);
}

