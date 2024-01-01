#include <cs50.h>
#include <stdio.h>

int get_size(void);
void print_grid(int size);

int main(void)
{
    // Get size of grid
    int n = get_size();

    // Print square grid of bricks
    print_grid(n);
}

int get_size(void)
{
    int i;
    do
    {
        i = get_int("Size: ");
    }
    while (i < 1);
    return i;
}

void print_grid(int size)
{
    for (int i = 0; i < size; i++)
    {
        for (int j = 0; j < size; j++)
        {
            printf("#");
        }
        printf("\n");
    }
}
