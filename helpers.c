// Helper functions for music
#include <cs50.h>
#include <stdio.h>
#include <math.h>
#include <ctype.h>
#include <stdlib.h>
#include <string.h>
#include "helpers.h"
#include "wav.h"

// Converts a fraction formatted as X/Y to eighths
int duration(string fraction)
{
    int x = fraction [0] - '0';
    int y = fraction [2] - '0';
    //calculating duration
    return ((16 / y) * x / 2);
}

// Calculates frequency (in Hz) of a note
int frequency(string note)
{
    double octave = note[strlen(note) - 1] - '0';
    long double fre = 440.00;
    //switching octaves
    switch (note[0])
    {
        case 'A':
            break;

        case 'B':
            fre *= pow(2.0, (2.0 / 12.0));
            break;

        case 'C':
            fre /= pow(2, (9.0 / 12.0));
            break;

        case 'D':
            fre /= pow(2, (7.0 / 12.0));
            break;

        case 'E':
            fre /= pow(2, (5.0 / 12.0));
            break;

        case 'F':
            fre /= pow(2, (4.0 / 12.0));
            break;

        case 'G':
            fre /= pow(2, (2.0 / 12.0));
            break;
    }
    //checking if octave bigger or smaller than octave 4
    if (octave < 4)
    {
        fre /= pow(2.0, (4.0 - octave));
    }
    else if (octave > 4)
    {
        fre *= pow(2.0, (octave - 4.0));
    }
    //checking if the note has b or #
    if (note[1] == '#')
    {
        fre *= pow(2.0, 1.0 / 12.0);
    }
    else if (note[1] == 'b')
    {
        fre /= pow(2.0, 1.0 / 12.0);
    }
    return round(fre);
}

// Determines whether a string represents a rest
bool is_rest(string s)
{
    if (s[0] == '\0')
    {
        return true;
    }
    return false;
}
