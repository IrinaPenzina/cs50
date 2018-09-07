#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>


int main(int argc, char *argv[])
{
    // ensure proper usage
    if (argc != 2)
    {
        fprintf(stderr, "Usage: one command-line argument (argc)\n");
        return 1;
    }
    //user inputs the name of the file
    char *infile = argv[1];
    //blocks of the memory
    uint8_t buffer[512] = {0};
    //track new images
    int nimage = 0;
    //open card
    FILE *inptr = fopen(infile, "r");
    if (inptr == NULL)
    {
        fprintf(stderr, "Could not open %s.\n", infile);
        return 1;
    }
    //char* outfile;
    FILE *outfile = NULL;
    char image[8];
    //reading bytes
    while (fread(buffer, sizeof(buffer), 1, inptr) == 1)
    {
        //loking for the first three bytes of the beggining of jpg
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {
            //read file shoud be inside of c
            if (outfile != NULL)
            {
                fclose(outfile);
            }
            sprintf(image, "%.3d.jpg", nimage);

            outfile = fopen(image, "w");
            if (outfile == NULL)
            {
                fclose(inptr);
                return 2;
            }
            nimage++;
            fwrite(buffer, sizeof(buffer), 1, outfile);
        }
        else if (nimage > 0)
        {
            fwrite(buffer, sizeof(buffer), 1, outfile);
        }
    }
    // close infile
    fclose(inptr);

    // close outfile
    //fclose(outfile);

    // success
    return 0;
}