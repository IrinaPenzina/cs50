#include <cs50.h>
#include <ctype.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, string argv[])
{
    int k = 0;
    // checks if argc equals 2
    if (argc == 2)
    {
        k = atoi(argv[1]);
        //prompting user for a positive int
        if (k < 0)
        {
            printf("Give me a positive integer!\n");
            return 1;
        }
        string p = get_string("plaintext: ");
        //printing enciphered text from the code below thank you printf
        printf("ciphertext: ");
        //getting and checking each character separetly
        for (int i = 0, n = strlen(p); i < n; i++)
        {
            //checkin if it's a letter
            if (isalpha(p[i]))
            {
                //if the letter is capital
                if (isupper(p[i]))
                {
                    printf("%c", (((p[i] - 65) + k) % 26) + 65);
                }
                //if it's low
                else if (islower(p[i]))
                {
                    printf("%c", (((p[i] - 97) + k) % 26) + 97);
                }
            }
            //if it's a punctuation
            else if (ispunct(p[i]))
            {
                printf("%c", (p[i]));
            }
            //space
            else if (isspace(p[i]))
            {
                printf("%c", (p[i]));
            }
        }
        printf("\n");
        return 0;
    }
    return 1;
}