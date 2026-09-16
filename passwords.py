"""
PASSWORD STRENGTH CHECKER PROGRAM

A tool to help employees create stronger passwords by checking:
- Against dictionary words (70,000+ words)
- Against common passwords (top 1 million)
- Length requirements
- Character complexity (uppercase, lowercase, digits, special chars)
"""

# import the Character types  

LOWER = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m",
         "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]

UPPER = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M",
         "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]

DIGITS = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

SPECIAL = ["!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "-", "_", "=",
           "+", "[", "]", "{", "}", "|", ";", ":", "'", "\"", ",", ".", "<",
           ">", "?", "/", "\\", "`", "~"]


# function 1: word in file
def word_in_file(word, filename, case_sensitive=False):
    """
    Check if a word exists in a file.

    Parameters:
        word (str): The word to search for.
        filename (str): Name of the file to search in.
        case_sensitive (bool): If True, match exactly. If False (default),
                               ignore upper/lower case.

    Returns:
        bool: True if the word is found, False otherwise.
    """
    try:
        # Sven's Tip #2: Open the file using UTF-8 encoding
        with open(filename, "r", encoding="utf-8") as file:
            # Read each line in the file
            for line in file:
                # Sven's Tip #3: use strip() to remove the newline
                file_word = line.strip()

                # Compare based on case sensitivity
                if case_sensitive:
                    if word == file_word:
                        return True
                else:
                    if word.lower() == file_word.lower():
                        return True

        # Not found
        return False

    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return False
    except Exception as e:
        print(f"Error reading file '{filename}': {e}")
        return False

# FUNCTION 2: Check whether the password contains a character from the list

def word_has_character(word, character_list):
    """
    Check if a word contains any character from a given list.

    Parameters:
        word (str): The word to check.
        character_list (list): List of characters to look for.

    Returns:
        bool: True if any character from the list is in the word,
              False otherwise.
    """
    for char in word:
        if char in character_list:
            return True
    return False

# FUNCTION 3: word_complexity
def word_complexity(word):
    """
    Checks how many different types of characters
    are present in the password.

    Parameters:
        word (str): The word to analyze.

    Returns:
        int: Complexity score from 0 to 4.
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
    Calculate password strength based on multiple factors.

    Checks length requirements, checks the dictionary and known-password
    files, calls word_complexity() to calculate complexity, then
    determines strength based on the user requirements.

    Parameters:
        password (str): The password to check.
        min_length (int): Minimum acceptable length (default 10).
        strong_length (int): Length that automatically gets full strength (default 16).

    Returns:
        int: Strength score from 0 to 5.
    """
    # Check dictionary (case insensitive)
    if word_in_file(password, "wordlist.txt", case_sensitive=False):
        print("Password is a dictionary word and is not secure.")
        return 0

    # Check common passwords (case sensitive)
    if word_in_file(password, "toppasswords.txt", case_sensitive=True):
        print("Password is a commonly used password and is not secure.")
        return 0

    # Check if too short
    if len(password) < min_length:
        print("Password is too short and is not secure.")
        return 1

    # Check if very long
    if len(password) > strong_length:
        print("Password is long enough to receive the maximum strength score.")
        return 5
    
    # Otherwise, use complexity
    complexity = word_complexity(password)
    strength = 1 + complexity
    return strength

# FUNCTION 5: main
def main():
    """
    Main program loop.

    Asks the user for a password to test. If the password is anything
    other than "q" or "Q", calls password_strength() and reports the
    results. If the user enters "q" or "Q", the program quits.
    """
    while True:
        # Ask for a password
        password = input("Enter a password to test (or 'q' to quit): ")

        # Quit if the user typed q or Q
        if password.lower() == "q":
            print("Thanks for using the password strength checker!")
            break

        # Otherwise, test the password
        strength = password_strength(password)
        print(f"Strength: {strength}/5")
        print()

# PROGRAM ENTRY POINT
if __name__ == "__main__":
     main()

