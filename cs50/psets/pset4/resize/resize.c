/**
 * Copies a BMP piece by piece, just because.
 */
       
#include <stdio.h>
#include <stdlib.h>
#include <math.h>

#include "bmp.h"

int main(int argc, char *argv[])
{
    // ensure proper usage
    if (argc != 4)
    {
        fprintf(stderr, "Usage: ./resize n infile outfile\n");
        return 1;
    }

    float f = atof(argv[1]);
    if(f > 100.0 || f < 0.0)
    {
        fprintf(stderr, "n should be in 0.0-100.0.\n");
        return 2;
    }

    // remember filenames
    char *infile = argv[2];
    char *outfile = argv[3];

    // open input file 
    FILE *inptr = fopen(infile, "r");
    if (inptr == NULL)
    {
        fprintf(stderr, "Could not open %s.\n", infile);
        return 3;
    }

    // open output file
    FILE *outptr = fopen(outfile, "w");
    if (outptr == NULL)
    {
        fclose(inptr);
        fprintf(stderr, "Could not create %s.\n", outfile);
        return 4;
    }

    // read infile's BITMAPFILEHEADER
    BITMAPFILEHEADER bf, outBf;
    fread(&bf, sizeof(BITMAPFILEHEADER), 1, inptr);

    // read infile's BITMAPINFOHEADER
    BITMAPINFOHEADER bi, outBi;
    fread(&bi, sizeof(BITMAPINFOHEADER), 1, inptr);
    
    fseek(inptr, 0, SEEK_SET);
    fread(&outBf, sizeof(BITMAPFILEHEADER), 1, inptr);
    fread(&outBi, sizeof(BITMAPINFOHEADER), 1, inptr);

    // ensure infile is (likely) a 24-bit uncompressed BMP 4.0
    if (bf.bfType != 0x4d42 || bf.bfOffBits != 54 || bi.biSize != 40 || 
        bi.biBitCount != 24 || bi.biCompression != 0)
    {
        fclose(outptr);
        fclose(inptr);
        fprintf(stderr, "Unsupported file format.\n");
        return 5;
    }
        
    // update outfile's header and info
    outBi.biWidth = round(bi.biWidth * f);
    outBi.biHeight = round(bi.biHeight * f);
    
    // fprintf(stdout, "--> %i, %i, %i, %i, %i, %i, %i\n", 
    // bf.bfType, bf.bfSize, bf.bfOffBits, bi.biWidth, bi.biHeight, bi.biSize, bi.biBitCount);
    // return 1;

    // determine padding for scanlines
    int padding = (4 - (bi.biWidth * sizeof(RGBTRIPLE)) % 4) % 4;
    int outPadding = (4 - (outBi.biWidth * sizeof(RGBTRIPLE)) % 4) % 4;

    // update size
    outBi.biSizeImage = ((sizeof(RGBTRIPLE) * outBi.biWidth) + outPadding) * abs(outBi.biHeight);
    outBf.bfSize = outBi.biSizeImage + sizeof(BITMAPFILEHEADER) + sizeof(BITMAPINFOHEADER);

    // write outfile's BITMAPFILEHEADER
    fwrite(&outBf, sizeof(BITMAPFILEHEADER), 1, outptr);

    // write outfile's BITMAPINFOHEADER
    fwrite(&outBi, sizeof(BITMAPINFOHEADER), 1, outptr);
    
    float widthRatio = bi.biWidth/(float)outBi.biWidth, heightRatio = bi.biHeight/(float)outBi.biHeight;

    // int index = 0;
    // iterate over infile's scanlines
    for (int i = 0, biHeight = abs(outBi.biHeight); i < biHeight; i++)
    {
        // iterate over pixels in scanline
        for (int j = 0; j < outBi.biWidth; j++)
        {
            // temporary storage
            RGBTRIPLE triple;
            triple.rgbtBlue = 0x00;
            triple.rgbtGreen = 0x00;
            triple.rgbtRed = 0x00;

            RGBTRIPLE destTriple;
            
            // find all the pixels we need to calculate the i&j'th outptr's pixel
            // to find out which pixel of original photo should be used, I just average all the pixels' values,
            // first is to find out the limit of outptr's pixel occupied in the original photo
            // like a 3 by 3 photo resize to 4 times big, the first pixel's limit should be 0 - 1/4 of the first pixel in the original photo
            // if the limit is greater than 1, it means the factor is less than 1
            float widthStart = floor(j * widthRatio), widthEnd = (j+1) * widthRatio;
            float heightStart = floor(i * heightRatio), heightEnd = (i+1) * heightRatio;
            int mixPixelLength = ceil(widthEnd - widthStart) * ceil(heightEnd - heightStart);
            
            int singlePixel[3] = {0, 0, 0};

            for(int currentWidth = widthStart; currentWidth < widthEnd; currentWidth++)
            {
                for(int currentHeight = heightStart; currentHeight < heightEnd; currentHeight++)
                {
                    // if(index > 47) {
                    //     printf("test\n");
                    // }
                    int offset = 54 + currentHeight * (padding + bi.biWidth * 3) + currentWidth * 3;
                    // read RGB triple from infile
                    fseek(inptr, offset, SEEK_SET);
                    fread(&triple, sizeof(RGBTRIPLE), 1, inptr);
                    singlePixel[0] += triple.rgbtBlue;
                    singlePixel[1] += triple.rgbtGreen;
                    singlePixel[2] += triple.rgbtRed;
                }
            }
            
            // average the pixels
            destTriple.rgbtBlue = singlePixel[0] / mixPixelLength;
            destTriple.rgbtGreen = singlePixel[1] / mixPixelLength;
            destTriple.rgbtRed = singlePixel[2] / mixPixelLength;
            // fprintf(stdout, "%i: b: %i, g: %i, r: %i\n", 
            //     index++, destTriple.rgbtBlue, destTriple.rgbtGreen, destTriple.rgbtRed);
        
            // write RGB triple to outfile
            fwrite(&destTriple, sizeof(RGBTRIPLE), 1, outptr);
        }

        // then add it back (to demonstrate how)
        for (int k = 0; k < outPadding; k++)
        {
            fputc(0x00, outptr);
        }
    }

    // close infile
    fclose(inptr);

    // close outfile
    fclose(outptr);

    // success
    return 0;
}
