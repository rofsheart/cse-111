"""
PASSWORD STRENGTH CHECKER PROGRAM

A tool to help employees create stronger passwords by checking:
- Against dictionary words (70,000+ words)
- Against common passwords (top 1 million)
- Length requirements
- Character complexity (uppercase, lowercase, digits, special chars)

Author: Hearton Rofem Edu
Date: 09-09-2026
"""

import os

# CONSTANTS - Character type definitions

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
    Check if a word exists in a file.
    
    Parameters:
        word (str): The word to search for
        filename (str): Name of the file to search in
        case_sensitive (bool): If True, case-sensitive match; if False, case-insensitive
    
    Returns:
        bool: True if word is found, False otherwise
    """
    try:
        # Open the file with UTF-8 encoding
        with open(filename, "r", encoding="utf-8") as file:
            # Read each line in the file
            for line in file:
                # Remove newline character and any extra whitespace
                file_word = line.strip()
                
                # Compare based on case sensitivity
                if case_sensitive:
                    # Exact match required
                    if word == file_word:
                        return True
                else:
                    # Case-insensitive match (convert both to lowercase)
                    if word.lower() == file_word.lower():
                        return True
        
        # Word not found in file
        return False
        
    except FileNotFoundError:
        # Handle missing file
        print(f"Error: File '{filename}' not found.")
        return False
    except Exception as e:
        # Handle other errors
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
    # Loop through each character in the word
    for char in word:
        # Check if this character is in the character list
        if char in character_list:
            return True
    
    # No matching characters found
    return False


# FUNCTION 3: word_complexity

def word_complexity(word):
    """
    Calculate the complexity score of a word based on character types.
    
    Parameters:
        word (str): The word to analyze
    
    Returns:
        int: Number of different character types found (0-4)
    """
    complexity = 0
    
    # Check for lowercase letters
    if word_has_character(word, LOWER):
        complexity += 1
    
    # Check for uppercase letters
    if word_has_character(word, UPPER):
        complexity += 1
    
    # Check for digits
    if word_has_character(word, DIGITS):
        complexity += 1
    
    # Check for special characters
    if word_has_character(word, SPECIAL):
        complexity += 1
    
    return complexity


# FUNCTION 4: get_character_type_breakdown

def get_character_type_breakdown(word):
    """
    Get a breakdown of which character types are in the word.
    
    Parameters:
        word (str): The word to analyze
    
    Returns:
        list: List of character types present
    """
    types = []
    
    if word_has_character(word, LOWER):
        types.append("lowercase")
    if word_has_character(word, UPPER):
        types.append("UPPERCASE")
    if word_has_character(word, DIGITS):
        types.append("digits")
    if word_has_character(word, SPECIAL):
        types.append("special")
    
    return types


# FUNCTION 5: draw_strength_bar

def draw_strength_bar(strength):
    """
    Draw a visual progress bar for password strength.
    
    Parameters:
        strength (int): Strength score from 0-5
    
    Returns:
        str: Visual bar representation
    """
    # Define labels based on strength
    if strength == 0:
        label = "VERY WEAK"
    elif strength == 1:
        label = "WEAK"
    elif strength == 2:
        label = "FAIR"
    elif strength == 3:
        label = "MODERATE"
    elif strength == 4:
        label = "STRONG"
    else:  # strength == 5
        label = "VERY STRONG"
    
    # Create bar (5 filled blocks = full strength)
    filled = strength
    bar = ""
    for i in range(5):
        if i < filled:
            bar += "█"
        else:
            bar += "░"
    
    return f"[{bar}] {label}"


# FUNCTION 6: password_strength

def password_strength(password, min_length=10, strong_length=16):
    """
    Calculate password strength based on multiple factors.
    
    Parameters:
        password (str): The password to check
        min_length (int): Minimum acceptable length (default: 10)
        strong_length (int): Length that automatically gets full strength (default: 16)
    
    Returns:
        int: Strength score from 0-5
    
    Messages printed:
        - 0: Dictionary word or common password
        - 1: Too short
        - 2-4: Based on complexity
        - 5: Very long password
    """
    
    # CHECK 1: Is it a dictionary word? (case insensitive)
    if word_in_file(password, "wordlist.txt", case_sensitive=False):
        print(f"\n❌ Password is a dictionary word and is not secure.")
        print(f"   Dictionary words are easy to guess or crack.")
        return 0
    
    # CHECK 2: Is it a commonly used password? (case sensitive)
    if word_in_file(password, "toppasswords.txt", case_sensitive=True):
        print(f"\n❌ Password is a commonly used password and is not secure.")
        print(f"   This password appears in the top 1 million most common passwords.")
        return 0
    
    # CHECK 3: Is it too short?
    if len(password) < min_length:
        print(f"\n❌ Password is too short and is not secure.")
        print(f"   Minimum length is {min_length} characters (yours has {len(password)})")
        return 1
    
    # CHECK 4: Is it long enough to be automatically strong?
    if len(password) > strong_length:
        print(f"\n✅ Password is long, length trumps complexity this is a good password.")
        print(f"   Your password has {len(password)} characters, which is excellent!")
        return 5
    
    # CHECK 5: Calculate strength based on complexity
    complexity = word_complexity(password)
    strength = 1 + complexity  # Base score of 1 plus complexity
    
    # Show character type breakdown
    types_present = get_character_type_breakdown(password)
    if types_present:
        print(f"\n📊 Character types used: {', '.join(types_present)}")
    else:
        print(f"\n⚠️  No standard character types found.")
    
    print(f"📏 Password length: {len(password)} characters")
    
    # Provide feedback based on strength
    if strength <= 2:
        print(f"\n⚠️  Password is weak, consider adding more character types.")
    elif strength == 3:
        print(f"\n⚠️  Password is moderate, could be improved with more variety.")
    elif strength == 4:
        print(f"\n✅ Password has good complexity, this is a strong password.")
    else:  # strength == 5
        print(f"\n✅ Password has excellent complexity, this is a very strong password.")
    
    return strength


# FUNCTION 7: main

def main():
    """
    Main program loop - provides user interface for password testing.
    """
    # Welcome banner
    print(f"\n{'='*60}")
    print(f"🔐  PASSWORD STRENGTH CHECKER  🔐")
    print(f"{'='*60}")
    print("Welcome to the Password Strength Checker tool!")
    print(f"\nThis tool helps you create stronger passwords by:")
    print("  • Checking against 70,000+ dictionary words")
    print("  • Checking against 1 million common passwords")
    print("  • Evaluating length and character variety")
    print("  • Providing detailed feedback")
    print("\n" + "="*60)
    
    # Show instructions
    print(f"\nINSTRUCTIONS:")
    print("  • Enter a password to check its strength")
    print(f"  • Type 'q' or 'Q' to quit")
    print("="*60)
    
    # Check if required files exist
    required_files = ["wordlist.txt", "toppasswords.txt"]
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print(f"\n⚠️  WARNING: The following files are missing:")
        for file in missing_files:
            print(f"  • {file}")
        print(f"Some password checks may not work correctly.\n")
    
    # Initialize counter for tested passwords
    password_count = 0
    
    # Main loop
    while True:
        # Get user input
        print(f"\n{'─'*60}")
        password = input(f"Enter a password to test (or 'q' to quit): ")
        print(f"{'─'*60}")
        
        # Check for quit command
        if password.lower() == 'q':
            print(f"\nGoodbye! Stay secure! 🔒")
            print(f"You tested {password_count} password(s) in this session.\n")
            break
        
        # Skip empty passwords
        if len(password.strip()) == 0:
            print(f"⚠️  Please enter a valid password.")
            continue
        
        # Increment password counter
        password_count += 1
        
        # Print the password being tested (with masking for security in real-world)
        print(f"\nTesting password: {'*' * len(password)}")
        
        # Calculate password strength
        strength = password_strength(password)
        
        # Show visual strength bar
        bar = draw_strength_bar(strength)
        print(f"\nStrength Score: {strength}/5 {bar}")
        
        # Show additional strength info
        if strength == 0:
            print(f"🔴 This password is NOT secure. Do NOT use it!")
        elif strength == 1:
            print(f"🔴 This password is weak. Choose a stronger one!")
        elif strength == 2:
            print(f"🟡 This password is fair, but could be improved.")
        elif strength == 3:
            print(f"🟡 This password is moderate. Consider adding more variety.")
        elif strength == 4:
            print(f"🟢 This password is strong! Good job!")
        else:  # strength == 5
            print(f"🟢 Excellent! This is a very strong password!")
        
        # Show complexity score
        complexity = word_complexity(password)
        print(f"Complexity Score: {complexity}/4")


# PROGRAM ENTRY POINT

if __name__ == "__main__":
    main()