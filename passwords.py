"""
PASSWORD STRENGTH CHECKER PROGRAM

A tool to help employees create stronger passwords by checking:
- Against dictionary words (70,000+ words)
- Against common passwords (top 1 million)
- Length requirements
- Character complexity (uppercase, lowercase, digits, special chars)

Author: Hearton Rofem Edu
Date: 09-11-2026

CREATIVE ADDITION (Rubric #11):
    In addition to Sven's required functions, main() displays an optional
    visual strength bar and an emoji indicator for each result. This is my
    own addition and is not part of the required specification. It has no
    effect on the required return values or required messages.
"""


# CONSTANTS - Character type definitions (provided by Sven)
LOWER = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m",
         "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]

UPPER = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M",
         "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]

DIGITS = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

SPECIAL = ["!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "-", "_", "=",
           "+", "[", "]", "{", "}", "|", ";", ":", "'", "\"", ",", ".", "<",
           ">", "?", "/", "\\", "`", "~"]


# FUNCTION 1: word_in_file
def word_in_file(word, filename, case_sensitive=False):
    """
    Check if a word exists in a file (one word per line).

    Parameters:
        word (str): The word to search for
        filename (str): Name of the file to search in
        case_sensitive (bool): True for case-sensitive match, False for
                               case-insensitive (default)

    Returns:
        bool: True if word is found, False otherwise
    """
    target = word if case_sensitive else word.casefold()

    try:
        with open(filename, "r", encoding="utf-8") as file:
            for line in file:
                file_word = line.strip()
                if not case_sensitive:
                    file_word = file_word.casefold()
                if file_word == target:
                    return True
        return False
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return False
    except Exception as e:
        print(f"Error reading file '{filename}': {e}")
        return False


# FUNCTION 2: word_has_character
def word_has_character(word, character_list):
    """
    Check if a word contains any character from a given list.

    Parameters:
        word (str): The word to check
        character_list (list): List of characters to look for

    Returns:
        bool: True if any character from the list is found, False otherwise
    """
    for char in word:
        if char in character_list:
            return True
    return False


# FUNCTION 3: word_complexity
def word_complexity(word):
    """
    Calculate a complexity score based on character types in the word.

    Parameters:
        word (str): The word to analyze

    Returns:
        int: Number of character types present (0-4)
    """
    complexity = 0

    if word_has_character(word, LOWER):
        complexity += 1
    if word_has_character(word, UPPER):
        complexity += 1
    if word_has_character(word, DIGITS):
        complexity += 1
    if word_has_character(word, SPECIAL):
        complexity += 1

    return complexity


# FUNCTION 4: password_strength
def password_strength(password, min_length=10, strong_length=16):
    """
    Calculate password strength based on length, dictionary, and complexity.

    Parameters:
        password (str): The password to check
        min_length (int): Minimum acceptable length (default: 10)
        strong_length (int): Length at which password is automatically strong
                             (default: 16, meaning "longer than 15 characters")

    Returns:
        int: Strength score from 0-5
    """
    # CHECK 1: Dictionary word (case-insensitive)
    if word_in_file(password, "wordlist.txt", case_sensitive=False):
        print("Password is a dictionary word and is not secure.")
        return 0

    # CHECK 2: Common password (case-sensitive)
    if word_in_file(password, "toppasswords.txt", case_sensitive=True):
        print("Password is a commonly used password and is not secure.")
        return 0

    # CHECK 3: Too short
    if len(password) < min_length:
        print("Password is too short and is not secure.")
        return 1

    # CHECK 4: Long enough to be automatically strong
    # (longer than 15 characters = at least strong_length)
    if len(password) >= strong_length:
        print("Password is long, length trumps complexity this is a good password.")
        return 5

    # CHECK 5: Strength = base 1 + complexity
    return 1 + word_complexity(password)


# FUNCTION 5: main
def main():
    """
    Main user interface loop. Repeatedly asks the user for a password,
    reports its strength, and quits when the user enters 'q' or 'Q'.
    """
    # CREATIVE ADDITION (documented above)
    # Optional visual bar / emoji feedback in the UI layer only.
    def _visual_bar(strength):
        filled = "\u2588" * strength
        empty = "\u2591" * (5 - strength)
        return f"[{filled}{empty}]"

    def _emoji(strength):
        return {0: "\U0001F534", 1: "\U0001F534", 2: "\U0001F7E1",
                3: "\U0001F7E1", 4: "\U0001F7E2", 5: "\U0001F7E2"}[strength]
    #

    print("Password Strength Checker")
    print("Type 'q' or 'Q' at any time to quit.")

    while True:
        password = input("\nEnter a password to test: ")

        if password.lower() == "q":
            print("Goodbye!")
            break

        strength = password_strength(password)
        print(f"Strength: {strength}/5 {_visual_bar(strength)} {_emoji(strength)}")


if __name__ == "__main__":
    main()
