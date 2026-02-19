#include <mlx_helper.h>

void error(const char *s)
{
    printf("%s\n", s);
    exit(1);
}

// Testing
void print_config(t_config *config)
{
    if (!config)
    {
        printf("Config is NULL\n");
        return;
    }
    printf("=== Config ===\n");
    printf("Width           : %d\n", config->width);
    printf("Height          : %d\n", config->height);
    printf("Shape           : %s\n", config->shape ? config->shape : "(null)");
    printf("Wall color      : %s\n", config->wall_color ? config->wall_color : "(null)");
    printf("Flag color      : %s\n", config->flag_color ? config->flag_color : "(null)");
    printf("Cell size       : %d\n", config->cell_size);
    printf("Animation speed : %d\n", config->animation_speed);
    printf("================\n");
}

void print_cell(t_cell *cell)
{
    if (!cell)
    {
        printf("Cell is NULL\n");
        return;
    }
    printf("Cell: x=%d, y=%d, value=%d, is_solution=%d\n",
           cell->point.x, cell->point.y, cell->value, cell->is_sol);
}

void print_path(t_cell *path, int count)
{
    int i;

    if (!path)
    {
        printf("Path is NULL\n");
        return;
    }
    printf("=== Generation Path (%d steps) ===\n", count);
    for (i = 0; i < count; i++)
    {
        printf("[%d] x=%d, y=%d, value=%d, is_solution=%d\n",
               i, path[i].point.x, path[i].point.y,
               path[i].value, path[i].is_sol);
    }
    printf("==================================\n");
}

void print_maze(t_maze *maze)
{
    int i;

    if (!maze)
    {
        printf("Maze is NULL\n");
        return;
    }
    printf("=== Maze Structure ===\n");
    
    printf("Dimensions      : %dx%d\n", maze->width, maze->height);
    printf("Entry Point     : (%d, %d)\n", maze->entry.x, maze->entry.y);
    printf("Exit Point      : (%d, %d)\n", maze->exit.x, maze->exit.y);
    printf("Solution Length : %d\n", maze->solution_len);
    printf("Solution String : %s\n", maze->solution ? maze->solution : "(null)");
    printf("Gen Total Steps : %d\n", maze->gen_total_steps);
    
    printf("Grid            : %s\n", maze->grid ? "allocated" : "(null)");
    if (maze->grid)
    {
        printf("Grid content (all %d rows):\n", maze->height);
        for (i = 0; i < maze->height && maze->grid[i]; i++)
            printf("  [%d] %s\n", i, maze->grid[i]);
    }
    
    printf("Gen Path        : %s\n", maze->gen_path ? "allocated" : "(null)");
    if (maze->gen_path && maze->gen_total_steps > 0)
    {
        printf("First gen step  : x=%d, y=%d, value=%d, is_sol=%d\n",
               maze->gen_path[0].point.x, maze->gen_path[0].point.y,
               maze->gen_path[0].value, maze->gen_path[0].is_sol);
    }
    printf("=======================\n");
}


// trim leading and trailing whitespaces
char *trim(char *str)
{
    char *end;

    while(isspace((unsigned char)*str))
        str++;

    if (*str == 0)
        return str;

    end = str + strlen(str) - 1;
    while (end > str && isspace((unsigned char)*end))
        end--;

    *(end + 1) = '\0';
    return str;
}