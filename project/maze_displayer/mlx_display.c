#include<stdio.h>
#include<stdlib.h>

int main(int argc, char **argv)
{
    if (argc != 2)
    {
        printf("Error! Missing output text file.\n");
        exit(1);
    }
    FILE *file;
    
    // Open file in write mode
    file = fopen(argv[1], "r");
    if (file == NULL)
    {
        printf("Error opening file.\n");
        exit(1);
    }
    // read the hex values into a 2d array
    // read entry and exit points
    // 
    exit(0);
}