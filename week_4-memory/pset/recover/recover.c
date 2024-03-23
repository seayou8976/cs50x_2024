#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef uint8_t BYTE;

const int BLOCK_SIZE = 512;

int main(int argc, char *argv[])
{
    // Accept a single command-line argument
    if (argc != 2)
    {
        printf("Usage: ./recover FILE\n");
        return 1;
    }

    // Open the memory card
    FILE *card = fopen(argv[1], "r");
    if (card == NULL)
    {
        printf("Cannot open %s\n", argv[1]);
        return 1;
    }

    // Create a buffer for a block of data
    BYTE buffer[BLOCK_SIZE];

    // Initialize some variables for the recovery process
    int img_count = 0;
    FILE *recovered_jpg = NULL;

    // While there's still data left to read from the memory card...
    while (fread(buffer, sizeof(buffer), 1, card) == 1)
    {
        // Create JPEGs from the data
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {
            // filename will be: three digit number, + ".jpg" + terminating NUL
            char filename[8];

            // If this is not the first image, close the previous
            if (img_count != 0)
            {
                fclose(recovered_jpg);
            }

            // Create the filename
            sprintf(filename, "%03i.jpg", img_count);
            // Open the new file
            recovered_jpg = fopen(filename, "w");
            // Increase the count of discovered images
            img_count++;
        }

        // If this block is not a header, but the image count is > 1, keep writing
        if (img_count != 0)
        {
            fwrite(buffer, sizeof(buffer), 1, recovered_jpg);
        }
    }

    fclose(card);
    fclose(recovered_jpg);
}
