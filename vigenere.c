#include <cs50.h>
#include <ctype.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, char **argv)
{
    //making sure that the user type in something on the command line
    if (argc != 2)
    {
        printf("Usage: ./vigenere k\n");
        return 1;
    }
    //making the user type in letters not numbers
    string k = argv[1];
    int l = strlen(k);
    int j = 0;
    for (j = 0; j < l; j++)
    {
        //yell at them if they don't
        if (!isalpha(k[j]))
        {
            printf("Usage: ./vigenere k\n");
            return 1;
        }
    }
    string p = get_string("plaintext: ");
    printf("ciphertext: ");
    for (int i = 0, y = 0, n = strlen(p); y < l && i < n; i++)
    {
        //check if the character isalpha not a digit or space
        if (isalpha(p[i]))
        {
            //index to count the letters in the key word
            y = (j + i) % l;
            //this loop is going to work if letter is capitel from the plaintext
            if (isupper(p[i]))
            {
                printf("%c", (p[i] - 65 + toupper(k[y]) - 65) % 26 + 65);
            }
            //this loop is going to work if letter is small from the plaintext
            else if (islower(p[i]))
            {
                printf("%c", (p[i] - 97 + toupper(k[y]) - 65) % 26 + 97);
            }
        }
        //printing if it something else as it is
        else
        {
            printf("%c", p[i]);
            j--;
        }
    }
    printf("\n");
    return 0;
}