#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int n;
    int i;
    int j;
    do
        //Ask for positive
    {
        n = get_int("Positive number: ");
    }
    //The height of the pyramid
    while (n > 23 || n < 0);
    for (i = 0; i <= n - 1; i++)
    {
        //Print so many spaces
        for (j = 0; j <= n - i - 2; j++)
        {
            printf(" ");
        }
        //Print so many #
        for (j = 0; j <= i + 1; j++)
        {
            printf("#");
        }
        printf("\n");
    }
}




