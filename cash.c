#include <cs50.h>
#include <math.h>
#include <stdio.h>

int main(void)
{
    // dollars
    float d = 0.00;
    int count = 0;
    int c;
    //prompt a user for a number-dollar
    do
    {
        d = get_float("Change owed: ");
    }
    while (d < 0);
    c = round(d * 100); //rounding dollars and getting cents out of it
    while (c >= 25)
    {
        count++;//counting how many times the loop was executed
        c = c - 25;
    }
    while (c >= 10)
    {
        count++;
        c = c - 10;
    }
    while (c >= 5)
    {
        count++;
        c = c - 5;
    }
    while (c >= 1)
    {
        count++;
        c = c - 1;
    }
    printf("You get %d coins.\n", count);// printing how many times all the loops were executed

}