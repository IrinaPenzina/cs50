// Implements a dictionary's functionality
#include <ctype.h>
#include <stdbool.h>
#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "dictionary.h"

typedef struct node
{
    bool is_word;
    struct node *children[27];
}
node;

node *root = NULL;

void release(node *);

unsigned int count = 0;

// Returns true if word is in dictionary else false
bool check(const char *word)
{
    int index = 0;
    node *cursor = root;
    //for each letter in input word
    int len = strlen(word);
    if (len >= LENGTH)
    {
        return true;
    }

    for(int n = 0; n < len; n++)
    {
        if (word[n] == '\n')
        {
            return cursor -> is_word;
        }

        if (word[n] == '\'')
        {
            index = 26;
        }
        else
        {
            index = (int)tolower(word[n]) - (int)'a';
        }

        if (cursor -> children[index] == NULL)
        {
            return false;
        }
        else if (cursor -> children[index] != NULL)
        {
            cursor = cursor -> children[index];
        }
    }
    return cursor -> is_word;
}

// Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionary)
{
    //open dictionary
    FILE *file = fopen(dictionary, "r");
    if (!file)
    {
        printf("Could not open %s.\n", dictionary);
        unload();
        return false;
    }
    //declaration party
    int index = 0;
    root = malloc(sizeof(node));
    memset(root -> children, '\0', sizeof(root -> children));
    root -> is_word = false;
    //struct node *children;
    node *cursor = root;

    //for every dictionary word
    char s[LENGTH];
    while(fgets(s, LENGTH, file) != NULL)
    {
        cursor = root;
        for(int n = 0; n < strlen(s); n++)
        {
            char c = s[n];
            if (c == '\n')
            {
                cursor -> is_word = true;
                count++;
                break;
            }

            if (c == '\'')
            {
                index = 26;
            }
            else
            {
                index = ((int)tolower(c) - (int)'a');
            }

            //if cursor is null
            if (cursor != NULL &&
                cursor -> children[index] == NULL)
            {
                cursor -> children[index] = malloc(sizeof(node));
                memset(cursor -> children[index] -> children, '\0', sizeof(cursor -> children[index] -> children));
                cursor -> children[index] -> is_word = false;
            }

            cursor = cursor -> children[index];
        }
    }
    fclose(file);
    return true;
}

// Returns number of words in dictionary if loaded else 0 if not yet loaded
unsigned int size(void)
{
    return count;
}

// Unloads dictionary from memory, returning true if successful else false
bool unload(void)
{
    release(root);
    return true;
}

void release (node * x)
{
    for (int i = 0; i < 27; i++)
    {
        if (x != NULL && x -> children[i] != NULL)
        {
            release (x -> children[i]);
        }
    }

    free(x);
}