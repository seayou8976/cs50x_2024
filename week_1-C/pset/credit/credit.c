#include <cs50.h>
#include <stdio.h>

int get_doubled_digits(long card);
int get_single_digits(long card);
int get_int_length(long num);
string get_issuer(long card);

int main(void)
{

    long card_num = get_long("Card number: ");

    string issuer = get_issuer(card_num);

    if ((get_doubled_digits(card_num) + get_single_digits(card_num)) % 10 != 0)
    {
        issuer = "INVALID";
    }

    printf("%s\n", issuer);
}

int get_doubled_digits(long card)
{
    int total = 0;
    while (card > 0)
    {
        long discard = card / 10;
        long double_digit = (discard % 10) * 2;
        if (double_digit >= 10)
        {
            total += (double_digit / 10) + (double_digit % 10);
        }
        else
        {
            total += double_digit;
        }
        card = card / 100;
    }
    return total;
}

int get_single_digits(long card)
{
    int total = 0;
    while (card > 0)
    {
        long single_digit = (card % 10);
        total += single_digit;
        card = card / 100;
    }
    return total;
}

int get_int_length(long num)
{
    int length = 1;
    while (num > 9)
    {
        length++;
        num = num / 10;
    }
    return length;
}

string get_issuer(long card)
{
    int card_length = get_int_length(card);
    if (card_length == 13 || card_length == 15 || card_length == 16)
    {
        int first_two = 0;
        if (card_length == 13)
        {
            first_two = card / 100000000000;
            if (first_two >= 40 && first_two <= 49)
            {
                return "VISA";
            }
            else
            {
                return "INVALID";
            }
        }
        else if (card_length == 15)
        {
            first_two = card / 10000000000000;
            if (first_two == 34 || first_two == 37)
            {
                return "AMEX";
            }
            else
            {
                return "INVALID";
            }
        }
        else
        {
            first_two = card / 100000000000000;
            if (first_two >= 40 && first_two <= 49)
            {
                return "VISA";
            }
            else if (first_two >= 51 && first_two <= 55)
            {
                return "MASTERCARD";
            }
            else
            {
                return "INVALID";
            }
        }
    }
    else
    {
        return "INVALID";
    }
}
