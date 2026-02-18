#include <mlx_helper.h>

void put_pixel(t_img *img, int x, int y, int color)
{
    char *dst;

    if (x < 0 || y < 0)
        return;
    dst = img->addr + (y * img->line_len + x * (img->bpp / 8));
    *(unsigned int *)dst = color;
}

void draw_square(t_app *app, int gx, int gy, int color)
{
    int px = gx * app->config.cell_size;
    int py = gy * app->config.cell_size;
    int x;
    int y;

    y = 0;
    while (y < app->config.cell_size)
    {
        x = 0;
        while (x < app->config.cell_size)
        {
            put_pixel(&app->img, px + x, py + y, color);
            x++;
        }
        y++;
    }
}

void draw_static_maze(t_app *app)
{
    int x;
    int y;

    y = 0;
    while (y < app->maze.height)
    {
        x = 0;
        while (x < app->maze.width)
        {
            if (app->maze.grid[y][x] == '0' || app->maze.grid[y][x] == 'F')
                draw_square(app, x, y, 0xFFFFFF); // empty (white)
            else
                draw_square(app, x, y, 0x222222); // wall (dark)
            x++;
        }
        y++;
    }
}

void animate_generation(t_app *app)
{
    t_cell cell;

    if (app->anim_index >= app->maze.gen_total_steps)
    {
        app->phase = 1;
        app->anim_index = 0;
        return;
    }

    cell = app->maze.gen_path[app->anim_index];
    draw_square(app, cell.point.x, cell.point.y, 0x00AEEF); // blue
    app->anim_index++;
}

void animate_solution(t_app *app)
{
    int i;
    int x;
    int y;

    if (app->anim_index >= app->maze.solution_len)
    {
        app->phase = 2;
        return;
    }

    i = 0;
    x = app->maze.entry.x;
    y = app->maze.entry.y;
    
    while (i < app->anim_index && i < app->maze.solution_len)
    {
        if (app->maze.solution[i] == 'N')
            y--;
        else if (app->maze.solution[i] == 'S')
            y++;
        else if (app->maze.solution[i] == 'E')
            x++;
        else if (app->maze.solution[i] == 'W')
            x--;
        i++;
    }
    draw_square(app, x, y, 0x00FF00); // green
    app->anim_index++;
}

int update(void *param)
{
    t_app *app = (t_app *)param;

    app->frame++;

    if (app->frame % app->config.animation_speed != 0)
        return (0);

    if (app->phase == 0)
        animate_generation(app);
    else if (app->phase == 1)
        animate_solution(app);

    mlx_put_image_to_window(app->mlx, app->win, app->img.img, 0, 0);
    return (0);
}

int close_window(t_app *app)
{
    mlx_destroy_window(app->mlx, app->win);
    exit(0);
}

void init_graphics(t_app *app)
{
    int win_w;
    int win_h;

    win_w = app->maze.width * app->config.cell_size;
    win_h = app->maze.height * app->config.cell_size;

    app->mlx = mlx_init();
    app->win = mlx_new_window(app->mlx, win_w, win_h, "A-MAZE-ING");

    app->img.img = mlx_new_image(app->mlx, win_w, win_h);
    app->img.addr = mlx_get_data_addr(app->img.img,
                                      &app->img.bpp,
                                      &app->img.line_len,
                                      &app->img.endian);
}
