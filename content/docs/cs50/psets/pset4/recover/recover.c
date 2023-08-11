/**
 * Copies a BMP piece by piece, just because.
 */

#define BLOCK_SIZE 512

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>

int main(int argc, char *argv[])
{
    // ensure proper usage
    if (argc != 2)
    {
        fprintf(stderr, "Usage: ./recover image\n");
        return 1;
    }

    // remember filenames
    char *infile = argv[1];

    // open input file
    FILE *inptr = fopen(infile, "r");
    if (inptr == NULL)
    {
        fprintf(stderr, "Could not open %s.\n", infile);
        return 2;
    }

    uint8_t block[BLOCK_SIZE];

    int imageNo = 0;
    char *imageName = malloc(8);
    // sprintf(imageName, "%03i.jpg", imageNo++);
    // printf("image: %s\n", imageName);
    FILE *image;

    int flagToWrite = 0;

    while(fread(block, 1, BLOCK_SIZE, inptr))
    {
        // fread(block, 1, BLOCK_SIZE, inptr);

        if(block[0] == 0xff && block[1] == 0xd8 && block[2] == 0xff && ((block[3] & 0xf0) == 0xe0))
        {
            if (flagToWrite == 1)
            {
                fclose(image);
            }

            sprintf(imageName, "%03i.jpg", imageNo++);
            image = fopen(imageName, "w");
            flagToWrite = 1;
        }

        if (flagToWrite == 1)
        {
            fwrite(block, 1, BLOCK_SIZE, image);
        }
    }

    // close image again, just in case
    fclose(image);

    // free(block);
    free(imageName);

    // close infile
    fclose(inptr);

    // success
    return 0;
}
