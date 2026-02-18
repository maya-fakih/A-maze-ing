# include <mlx_helper.h>

int main(int argc, char **argv)
{
    FILE        *config_file;
    FILE        *output_file;
    FILE        *path_file;
    t_config    *config;
    t_maze      *maze;
    t_cell      *gen_path;
    char        path[256];
    int         gen_path_count;

    printf("Hello Minilibx!\n");
    if (argc != 4)
        error("Error! Provide config file, path file and output file.\n");
    // Open config file in read/write mode
    sprintf(path, "configuration/%s", argv[1]);
    config_file = fopen(path, "r+");
    if (config_file == NULL)
        error("Error opening config file.\n");
    // open gen_path file in read/write mode
    memset(&path, 0, sizeof(path));
    sprintf(path, "configuration/%s", argv[2]);
    path_file = fopen(path, "r+");
    if (path_file == NULL)
        error("Error opening generation path file.\n");
    // Open output file in read/write mode
    output_file = fopen(argv[3], "r+");
    if (output_file == NULL)
        error("Error opening output file.\n");
    // a function that handles parsing from config_file into t_config
    config = parse_settings(config_file);
    if (config == NULL)
        error("Error while parsing config.txt!\n");
    print_config(config);
    // TODO: parse gen_path_file into t_maze inside gen_path
    gen_path = parse_path(path_file, &gen_path_count);
    printf("Loaded %d generation steps\n", gen_path_count);
    print_path(gen_path, gen_path_count);
    // TODO: parse output_file into t_maze
    maze = parse_output(output_file, gen_path, gen_path_count, config->width, config->height);
	if (maze == NULL)
		error("Error!");
	print_maze(maze);
    // parsing done, display now
    
	free(config);
    free(gen_path);
    fclose(config_file);
    fclose(path_file);
    fclose(output_file);
    exit(0);
}
