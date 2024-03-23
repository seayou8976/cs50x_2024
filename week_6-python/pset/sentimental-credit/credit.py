import cs50
import re


def main():
    card = cs50.get_string("Card number: ")
    print(luhn_algo(card))


def luhn_algo(card_num):

    # By default, start with issuer being "INVALID"
    issuer = "INVALID"

    # Legitimate card numbers are only 16, 15, or 13 digits
    if re.fullmatch("\d{16}|\d{15}|\d{13}", card_num):
        # Convert to digits
        digits = [int(d) for d in card_num]

        # Iterate through every second digit in reverse and mutliply
        # Start at -2, stop at -1, step by -2
        for i in range(len(digits) - 2, -1, -2):
            digits[i] *= 2
            if digits[i] > 9:
                digits[i] -= 9

        # Calculate the sum
        total = sum(digits)

        # If total % 10 = 0, the number is valid. Get the issuer
        if total % 10 == 0:
            # Additional error checking included for number length, just to make sure
            # Mastercard is 16 digits and starts with 51, 52, 53, 54, or 55
            if re.fullmatch("\d{16}", card_num) and re.match(
                "51|52|53|54|55", card_num
            ):
                issuer = "MASTERCARD"
            # Visa is 13 or 16 digits and starts with 4
            elif re.fullmatch("\d{16}|\d{13}", card_num) and re.match("4", card_num):
                issuer = "VISA"
            # Amex is 15 digits and starts with 34 or 37
            elif re.fullmatch("\d{15}", card_num) and re.match("34|37", card_num):
                issuer = "AMEX"

    return issuer


main()
