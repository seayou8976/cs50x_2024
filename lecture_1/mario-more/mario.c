#include <cs50.h>
#include <stdio.h>

void print_pyramid(int h);

int main(void)
{
    int height;
    do
    {
        height = get_int("Height? ");
    }
    while ((height < 1) || (height > 8));

    print_pyramid(height);
}

void print_pyramid(h)
{
    for (int i = 1; i <= h; i++)
    {
        int num_space = h - i;
        int num_hash = i;

        for (int j = num_space; j > 0; j--)
        {
            printf(" ");
        }

        for (int k = num_hash; k > 0; k--)
        {
            printf("#");
        }

        printf("  ");

        for (int l = num_hash; l > 0; l--)
        {
            printf("#");
        }

        printf("\n");
    }
}
