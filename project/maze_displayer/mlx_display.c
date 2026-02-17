#include<stdio.h>
#include<stdlib.h>
#include<string.h>

// we need from config.txt: shape, wall_color, flag_color
// we will look for them and put them in variables when we find them,
// i will use a structure called config
struct t_config
{
    char    *shape;
    char    *wall_color;
    char    *flag_color;
    int     width;
    int     height;
} s_config;

struct t_point
{
    int x;
    int y;
} t_point;

// we need from maze.txt the 2D array -> maze
// entry, exit point and the path -> we need to read
// all the lines and put them in variables
struct t_maze
{
    char **grid; // 2D array containing hex values -> each cell
    int *entry
} s_maze;

void error(char *s)
{
    printf("%s\n", s);
    exit(1);
}

// i need a function that reads lines in a file to find the options and
// put them inside their corresponding variables

int main(int argc, char **argv)
{
    if (argc != 3)
    {
        printf("Error! Provide config file and output file.\n");
        exit(1);
    }
    FILE *config_file;
    FILE *output_file;
    char path[256];

    // Open config file in read mode
    sprintf(path, "configuration/%s", argv[1]);
    config_file = fopen(path, "r+");
    if (config_file == NULL)
        error("Error opening config file.\n");
    // Open output file in read mode
    output_file = fopen(argv[2], "r+");
    if (output_file == NULL)
        error("Error opening output file.\n");
    exit(0);
}
