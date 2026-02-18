#include <mlx_helper.h>

int main(int argc, char **argv)
{
    FILE            *config_file;
    FILE            *output_file;
    FILE            *path_file;
    t_app           app;
    t_cell          *gen_path;
    char            path[256];
    int             gen_path_count;

    printf("A-MAZE-ING Visualizer\n");
    if (argc != 4)
        error("Error! Provide config file, path file and output file.\n");
    
    sprintf(path, "configuration/%s", argv[1]);
    config_file = fopen(path, "r");
    if (config_file == NULL)
        error("Error opening config file.\n");
    
    memset(&path, 0, sizeof(path));
    sprintf(path, "configuration/%s", argv[2]);
    path_file = fopen(path, "r");
    if (path_file == NULL)
        error("Error opening generation path file.\n");
    
    output_file = fopen(argv[3], "r");
    if (output_file == NULL)
        error("Error opening output file.\n");
    
    app.config = *parse_settings(config_file);
    printf("✓ Config loaded: %dx%d\n", app.config.width, app.config.height);
    
    gen_path = parse_path(path_file, &gen_path_count);
    printf("✓ Generation path loaded: %d steps\n", gen_path_count);
    
    app.maze = *parse_output(output_file, gen_path, gen_path_count, 
                             app.config.width, app.config.height);
    printf("✓ Maze loaded\n");
    printf("Entry: (%d, %d), Exit: (%d, %d)\n", 
           app.maze.entry.x, app.maze.entry.y,
           app.maze.exit.x, app.maze.exit.y);
    
    app.phase = 0;
    app.anim_index = 0;
    app.frame = 0;
    
    init_graphics(&app);
    draw_static_maze(&app);
    mlx_put_image_to_window(app.mlx, app.win, app.img.img, 0, 0);
    
    mlx_loop_hook(app.mlx, update, &app);
    mlx_hook(app.win, 17, 0, (int (*) (void *))close_window, &app);
    mlx_loop(app.mlx);
    
    fclose(config_file);
    fclose(path_file);
    fclose(output_file);
    return (0);
}
