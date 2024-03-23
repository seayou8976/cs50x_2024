#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <string.h>

int coleman_liau(string text);

int lws_array[3]; // [0] = letters, [1] = words, [2] = sentences

int main(void)
{
    // Prompt the user for some text
    string text = get_string("Text: ");

    // Compute the Coleman-Liau index
    int grade = coleman_liau(text);
    // Print the grade level
    if (grade < 1)
    {
        printf("Before Grade 1\n");
    }
    else if (grade > 16)
    {
        printf("Grade 16+\n");
    }
    else
    {
        printf("Grade %i\n", grade);
    }
}

int coleman_liau(string text)
{
    // Initialize index
    int index = 0;

    for (int i = 0; i < strlen(text); i++)
    {
        if (i == (strlen(text) - 1))
        {
            // The end of the text is always the end of a word, and is almost always punctuation
            // But I handle it separately, because it's just easier this way
            lws_array[1]++;
        }

        if (text[i] == '.' || text[i] == '!' || text[i] == '?')
        {
            // Increase sentence count on ., !, or ?
            lws_array[2]++;
        }
        else if (isspace(text[i]))
        {
            // Increase word count on space
            lws_array[1]++;
        }
        else if (text[i] == '"')
        {
            // DOUBLE QUOTES DON'T COUNT AS LETTERS. Enough said
            i++;
        }
        else
        {
            // Increase character count
            lws_array[0]++;
        }
    }
    //Calculate Coleman-Liau index
    int l = lws_array[0] / (lws_array[1] / 100.0);
    int s = lws_array[2] / (lws_array[1] / 100.0);
    index = 0.0588 * l - 0.296 * s - 15.8;

    return index;
}
