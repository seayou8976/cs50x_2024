#include <cs50.h>
#include <stdio.h>

int main(void)
{
    // TODO: Prompt for start size
    int start_size;
    do
    {
        start_size = get_int("Start size: ");
    }
    while (start_size < 9);
    // TODO: Prompt for end size
    int end_size;
    do
    {
        end_size = get_int("End size: ");
    }
    while (end_size < start_size);
    // TODO: Calculate number of years until we reach threshold
    int num_of_years = 0;
    while (start_size < end_size)
    {
        int pop_growth = start_size / 3;
        int reduce_growth = start_size / 4;
        start_size = start_size + pop_growth - reduce_growth;

        num_of_years += 1;
    }
    // TODO: Print number of years
    printf("Years: %i\n", num_of_years);
}
