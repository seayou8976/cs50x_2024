#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <string.h>

bool validate_key(string key);
string substitute_text(string text, string key);

int main(int argc, string argv[])
{
    string substitution_key = argv[1];

    if (argc != 2)
    {
        printf("Usage: ./substitution KEY\n");
        return 1;
    }
    else if (validate_key(substitution_key) == false)
    {
        printf("Please provide a 26 character key using each letter only once\n");
        return 1;
    }
    else
    {
        // prepare_cipher(substitution_key);
        string plain = get_string("plaintext: ");
        printf("ciphertext: %s\n", substitute_text(plain, substitution_key));
    }
}

bool validate_key(string key)
{
    int used_letters[26] = {0};

    if (strlen(key) != 26)
    {
        return false;
    }

    for (int i = 0; i < strlen(key); i++)
    {
        if (isspace(key[i]) || ispunct(key[i]) || isdigit(key[i]))
        {
            return false;
        }
        else
        {
            int current_letter = toupper(key[i]) - 'A';
            used_letters[current_letter]++;
        }
    }
    // Verify each letter was seen exactly once
    for (int j = 0; j < 26; j++)
    {
        if (used_letters[j] != 1)
        {
            return false;
        }
    }
    return true;
}

string substitute_text(string text, string key)
{
    string output = text;
    for (int i = 0; i < strlen(text); i++)
    {
        if (isalpha(text[i]))
        {
            if (isupper(text[i]))
            {
                output[i] = toupper(key[text[i] - 'A']);
            }
            else
            {
                output[i] = tolower(key[text[i] - 'a']);
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
