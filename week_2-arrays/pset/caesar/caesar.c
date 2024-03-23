#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

bool validate_offset(string key);
string rotate_letters(string text, int offset);

int main(int argc, string argv[])
{

    if (argc != 2 || validate_offset(argv[1]) == false)
    {
        printf("Usage: ./caesar OFFSET\n");
        return 1;
    }
    else
    {
        int offset = atoi(argv[1]);

        string plain = get_string("plaintext: ");
        printf("ciphertext: %s\n", rotate_letters(plain, offset));
    }
}

bool validate_offset(string key)
{
    for (int i = 0; i < strlen(key); i++)
    {
        if (isdigit(key[i]) == false)
        {
            return false;
        }
    }
    return true;
}

string rotate_letters(string text, int offset)
{
    string output = text;
    for (int i = 0; i < strlen(text); i++)
    {
        if (isalpha(text[i]))
        {
            if (isupper(text[i]))
            {
                output[i] = toupper((text[i] - 'A' + offset) % 26 + 'A');
            }
            else
            {
                output[i] = tolower((text[i] - 'a' + offset) % 26 + 'a');
            }
        }
        else
        {
            // non-alphabetic characters should not change
            output[i] = text[i];
        }
    }
    return output;
}
