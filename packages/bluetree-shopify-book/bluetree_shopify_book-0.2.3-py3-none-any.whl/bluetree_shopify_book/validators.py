from __future__ import annotations

from urllib.parse import urlparse


def is_valid_url(url: str) -> bool:
    """
    Checks if a given string is a valid URL.

    Parameters:
    url (str): The string to check.

    Returns:
    bool: True if the string is a valid URL, False otherwise.
    """
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False


def is_valid_isbn(isbn: str) -> bool:
    """
    Validates an ISBN code in either 10-digit or 13-digit format.

    Parameters:
    isbn (str): The ISBN code to validate.

    Returns:
    bool: True if the ISBN code is valid, False otherwise.

    This function validates an ISBN code in either 10-digit or 13-digit format. The validation algorithm is based on the
    check digit, which is the last digit of the ISBN code. The check digit is calculated using a specific formula
    depending on the number of digits in the ISBN code. If the calculated check digit matches the actual check digit
    in the ISBN code, then the code is considered valid.
    """
    # Remove any non-numeric characters and leading/trailing white space
    isbn = "".join(c for c in isbn if c.isdigit())

    # Check if the ISBN is 10 or 13 digits long
    if len(isbn) == 10:
        # Validate 10-digit ISBN
        check_digit = 0
        for i in range(9):
            check_digit += (i + 1) * int(isbn[i])
        check_digit %= 11
        if check_digit == int(isbn[9]) or (check_digit == 10 and isbn[9] == "X"):
            return True
    elif len(isbn) == 13:
        # Validate 13-digit ISBN
        check_digit = 0
        for i in range(12):
            if i % 2 == 0:
                check_digit += int(isbn[i])
            else:
                check_digit += 3 * int(isbn[i])
        check_digit %= 10
        check_digit = (10 - check_digit) % 10
        if check_digit == int(isbn[12]):
            return True

    # If the ISBN is not 10 or 13 digits or the check digit is invalid, return False
    return False


def sanitize_isbn(isbn: str) -> str:
    """
    Sanitizes an ISBN code by removing any non-numeric characters and leading/trailing white space.

    Parameters:
    isbn (str): The ISBN code to sanitize.

    Returns:
    str: The sanitized ISBN code.

    This function removes any non-numeric characters and leading/trailing white space from the provided ISBN code.
    The resulting string contains only numeric characters.
    """
    return "".join(c for c in isbn if c.isdigit())
