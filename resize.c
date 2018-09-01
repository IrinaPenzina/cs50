// Copies a BMP file
#include <stdio.h>
#include <stdlib.h>

#include "bmp.h"

int main(int argc, char *argv[])
{
    // ensure proper usage
    if (argc != 4)
    {
        fprintf(stderr, "Usage: three command-line arguments (argc)\n");
        return 1;
    }
    //number from a user using what th picture is going to be resized
    int n = atoi(argv[1]);
    if (n >= 100 || n < 0)
    {
        fprintf(stderr, "Input a valid number.\n");
        return 1;
    }
    char *infile = argv[2];
    char *outfile = argv[3];
    // open input file
    FILE *inptr = fopen(infile, "r");
    if (inptr == NULL)
    {
        fprintf(stderr, "Could not open %s.\n", infile);
        return 2;
    }

    // open output file
    FILE *outptr = fopen(outfile, "w");
    if (outptr == NULL)
    {
        fclose(inptr);
        fprintf(stderr, "Could not open %s.\n", outfile);
        return 3;
    }
    // read infile's BITMAPFILEHEADER
    BITMAPFILEHEADER bf;
    fread(&bf, sizeof(BITMAPFILEHEADER), 1, inptr);

    // read infile's BITMAPINFOHEADER
    BITMAPINFOHEADER bi;
    fread(&bi, sizeof(BITMAPINFOHEADER), 1, inptr);

    // ensure infile is (likely) a 24-bit uncompressed BMP 4.0
    if (bf.bfType != 0x4d42 || bf.bfOffBits != 54 || bi.biSize != 40 ||
        bi.biBitCount != 24 || bi.biCompression != 0)
    {
        fclose(outptr);
        fclose(inptr);
        fprintf(stderr, "Unsupported file format.\n");
        return 4;
    }

    int old_biWidth = bi.biWidth;
    int old_biHeight = bi.biHeight;
    int padding = (4 - (old_biWidth * sizeof(RGBTRIPLE)) % 4) % 4;

    bi.biWidth *= n;
    bi.biHeight *= n;
    // determine padding for scanlines
    int newpadding = (4 - (bi.biWidth * sizeof(RGBTRIPLE)) % 4) % 4;
    bi.biSizeImage = ((sizeof(RGBTRIPLE) * bi.biWidth) + newpadding) * abs(bi.biHeight);
    bf.bfSize = bi.biSizeImage + sizeof(BITMAPFILEHEADER) + sizeof(BITMAPINFOHEADER);

    // write outfile's BITMAPFILEHEADER
    fwrite(&bf, sizeof(BITMAPFILEHEADER), 1, outptr);

    // write outfile's BITMAPINFOHEADER
    fwrite(&bi, sizeof(BITMAPINFOHEADER), 1, outptr);

    // iterate over outfile's scanlines vertically
    for (int i = 0, biHeight = abs(old_biHeight); i < biHeight; i++)
    {
        //recopy
        for (int l = 0; l < (n - 1); l++)
        {
            // iterate over pixels in scanline
            for (int j = 0; j < old_biWidth; j++)
            {
                // temporary storage
                RGBTRIPLE triple;

                // read RGB triple from infile
                fread(&triple, sizeof(RGBTRIPLE), 1, inptr);

                // write RGB triple to outfile
                for (int k = 0; k < n; k++)
                {
                    // write RGB triple to outfile
                    fwrite(&triple, sizeof(RGBTRIPLE), 1, outptr);
                }
            }

            // then add it back (to demonstrate how)
            for (int p = 0; p < newpadding; p++)
            {
                fputc(0x00, outptr);
            }
            //bring back cursor for a new line
            fseek(inptr, - 1 * (old_biWidth * sizeof(RGBTRIPLE)), SEEK_CUR);
        }

        //resizing horizontally
        for (int m = 0; m < old_biWidth; m++)
        {
            // temporary storage
            RGBTRIPLE triple;

            //read RGB triple from infile
            fread(&triple, sizeof(RGBTRIPLE), 1, inptr);

            // write RGB triple to outfile
            for (int k = 0; k < n; k++)
            {
                // write RGB triple to outfile
                fwrite(&triple, sizeof(RGBTRIPLE), 1, outptr);
            }
        }
        // skip over padding, if any
        fseek(inptr, padding, SEEK_CUR);
        for (int p = 0; p < newpadding; p++)
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

