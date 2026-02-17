#include<stdio.h>
#include<stdlib.h>
#include<string.h>

void error(char *s)
{
    printf("%s\n", s);
    exit(1);
}

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
    config_file = fopen(path, "r");
    if (config_file == NULL)
        error("Error opening config file.\n");
    // Open output file in read mode
    output_file = fopen(argv[2], "r");
    if (output_file == NULL)
        error("Error opening output file.\n");
    exit(0);
}
