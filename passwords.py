"""
PASSWORD STRENGTH CHECKER

A tool to help employees create stronger passwords by checking:
- Against dictionary words (70,000+ words)
- Against common passwords (top 1 million)
- Length requirements
- Character complexity (uppercase, lowercase, digits, special chars)

ENHANCEMENT:
Added colored console output for better visual feedback:
- Red for weak/error messages
- Yellow for warnings
- Green for success/strong passwords
- Blue for informational messages
- Purple for strength indicators
- Bold for emphasis

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

# Color codes for terminal output
RED = '\033[91m'
YELLOW = '\033[93m'
GREEN = '\033[92m'
BLUE = '\033[94m'
PURPLE = '\033[95m'
CYAN = '\033[96m'
BOLD = '\033[1m'
END = '\033[0m'

"""
PASSWORD STRENGTH CHECKER - PROGRAM OUTLINE
------------------------------------------
A tool to help employees create stronger passwords by checking:
- Against dictionary words (70,000+ words)
- Against common passwords (top 1 million)
- Length requirements
- Character complexity (uppercase, lowercase, digits, special chars)

ENHANCEMENT:
Added colored console output for better visual feedback

Author: Student
Date: 2024
"""

# CONSTANTS - Character type definitions
LOWER = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", 
         "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]

UPPER = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", 
         "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]

DIGITS = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

SPECIAL = ["!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "-", "_", "=", 
           "+", "[", "]", "{", "}", "|", ";", ":", "'", "\"", ",", ".", "<", 
           ">", "?", "/", "\\", "`", "~"]

# Color codes for terminal output
RED = '\033[91m'
YELLOW = '\033[93m'
GREEN = '\033[92m'
BLUE = '\033[94m'
PURPLE = '\033[95m'
CYAN = '\033[96m'
BOLD = '\033[1m'
END = '\033[0m'



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
    # TODO: Implement this function
    # Steps:
    # 1. Open the file with UTF-8 encoding
    # 2. Read each line
    # 3. Strip newline characters
    # 4. Compare based on case sensitivity
    # 5. Return True if found, False otherwise
    pass



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
    # TODO: Implement this function
    # Steps:
    # 1. Loop through each character in the word
    # 2. Check if character is in the character_list
    # 3. Return True if found, False otherwise
    pass



# FUNCTION 3: word_complexity

def word_complexity(word):
    """
    Calculate the complexity score of a word based on character types.
    
    Parameters:
        word (str): The word to analyze
    
    Returns:
        int: Number of different character types found (0-4)
    """
    # TODO: Implement this function
    # Steps:
    # 1. Initialize complexity to 0
    # 2. Call word_has_character for LOWER, UPPER, DIGITS, SPECIAL
    # 3. Add 1 to complexity for each type found
    # 4. Return complexity
    pass


# FUNCTION 4: password_strength

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
    # TODO: Implement this function
    # Steps:
    # 1. Check if password is in dictionary (case insensitive) → return 0
    # 2. Check if password is in common passwords (case sensitive) → return 0
    # 3. Check if password length < min_length → return 1
    # 4. Check if password length > strong_length → return 5
    # 5. Calculate complexity using word_complexity
    # 6. Strength = 1 + complexity
    # 7. Print appropriate message
    # 8. Return strength
    pass



# FUNCTION 5: draw_strength_bar (ENHANCEMENT)

def draw_strength_bar(strength):
    """
    Draw a visual progress bar for password strength.
    ENHANCEMENT: Provides visual representation of strength.
    
    Parameters:
        strength (int): Strength score from 0-5
    
    Returns:
        str: Visual bar representation with color
    """
    # TODO: Implement this function
    # Steps:
    # 1. Define colors and labels for each strength level
    # 2. Create bar with filled and empty blocks
    # 3. Return formatted string with colors
    pass



# FUNCTION 6: main

def main():
    """
    Main program loop - provides user interface for password testing.
    """
    # TODO: Implement this function
    # Steps:
    # 1. Display welcome message with colors
    # 2. Show instructions
    # 3. Check if required files exist
    # 4. Create main loop:
    #    a. Ask user for password
    #    b. Check if user wants to quit (q or Q)
    #    c. Call password_strength function
    #    d. Call draw_strength_bar for visual feedback
    #    e. Show results with colors
    pass



# PROGRAM ENTRY POINT

if __name__ == "__main__":
    main()

"""The above code provides a structured outline for a password strength checker tool. Each function has been defined with its purpose, parameters, and expected return values. The main function serves as the entry point for the program, guiding the user through the password testing process. The code includes enhancements for colored console output to improve user experience and feedback."""



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
        print(f"{RED}Error: File '{filename}' not found.{END}")
        return False
    except Exception as e:
        # Handle other errors
        print(f"{RED}Error reading file '{filename}': {e}{END}")
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
    # Define bar colors based on strength
    if strength == 0:
        color = RED
        label = "VERY WEAK"
    elif strength == 1:
        color = RED
        label = "WEAK"
    elif strength == 2:
        color = YELLOW
        label = "FAIR"
    elif strength == 3:
        color = YELLOW
        label = "MODERATE"
    elif strength == 4:
        color = GREEN
        label = "STRONG"
    else:  # strength == 5
        color = GREEN
        label = "VERY STRONG"
    
    # Create bar (5 filled blocks = full strength)
    filled = strength
    bar = ""
    for i in range(5):
        if i < filled:
            bar += f"{color}█{END}"
        else:
            bar += "░"
    
    return f"[{bar}] {color}{label}{END}"


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
        print(f"\n{RED}❌ Password is a dictionary word and is not secure.{END}")
        print(f"{RED}   Dictionary words are easy to guess or crack.{END}")
        return 0
    
    # CHECK 2: Is it a commonly used password? (case sensitive)
    if word_in_file(password, "toppasswords.txt", case_sensitive=True):
        print(f"\n{RED}❌ Password is a commonly used password and is not secure.{END}")
        print(f"{RED}   This password appears in the top 1 million most common passwords.{END}")
        return 0
    
    # CHECK 3: Is it too short?
    if len(password) < min_length:
        print(f"\n{RED}❌ Password is too short and is not secure.{END}")
        print(f"{YELLOW}   Minimum length is {min_length} characters (yours has {len(password)}){END}")
        return 1
    
    # CHECK 4: Is it long enough to be automatically strong?
    if len(password) > strong_length:
        print(f"\n{GREEN}✅ Password is long, length trumps complexity this is a good password.{END}")
        print(f"{GREEN}   Your password has {len(password)} characters, which is excellent!{END}")
        return 5
    
    # CHECK 5: Calculate strength based on complexity
    complexity = word_complexity(password)
    strength = 1 + complexity  # Base score of 1 plus complexity
    
    # Show character type breakdown
    types_present = get_character_type_breakdown(password)
    if types_present:
        print(f"\n{CYAN}📊 Character types used: {', '.join(types_present)}{END}")
    else:
        print(f"\n{YELLOW}⚠️  No standard character types found.{END}")
    
    print(f"{CYAN}📏 Password length: {len(password)} characters{END}")
    
    # Provide feedback based on strength
    if strength <= 2:
        print(f"\n{YELLOW}⚠️  Password is weak, consider adding more character types.{END}")
    elif strength == 3:
        print(f"\n{YELLOW}⚠️  Password is moderate, could be improved with more variety.{END}")
    elif strength == 4:
        print(f"\n{GREEN}✅ Password has good complexity, this is a strong password.{END}")
    else:  # strength == 5
        print(f"\n{GREEN}✅ Password has excellent complexity, this is a very strong password.{END}")
    
    return strength


# FUNCTION 7: main

def main():
    """
    Main program loop - provides user interface for password testing.
    """
    # Welcome banner
    print(f"\n{BOLD}{'='*60}{END}")
    print(f"{BOLD}{PURPLE}🔐  PASSWORD STRENGTH CHECKER  🔐{END}")
    print(f"{BOLD}{'='*60}{END}")
    print("Welcome to the Password Strength Checker tool!")
    print(f"\n{CYAN}This tool helps you create stronger passwords by:{END}")
    print("  • Checking against 70,000+ dictionary words")
    print("  • Checking against 1 million common passwords")
    print("  • Evaluating length and character variety")
    print("  • Providing detailed feedback")
    print("\n" + "="*60)
    
    # Show instructions
    print(f"\n{BOLD}INSTRUCTIONS:{END}")
    print("  • Enter a password to check its strength")
    print(f"  • Type {BOLD}'q'{END} or {BOLD}'Q'{END} to quit")
    print("="*60)
    
    # Check if required files exist
    required_files = ["wordlist.txt", "toppasswords.txt"]
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print(f"\n{YELLOW}⚠️  WARNING: The following files are missing:{END}")
        for file in missing_files:
            print(f"  • {file}")
        print(f"{YELLOW}Some password checks may not work correctly.{END}\n")
    
    # Initialize counter for tested passwords
    password_count = 0
    
    # Main loop
    while True:
        # Get user input
        print(f"\n{BOLD}{'─'*60}{END}")
        password = input(f"{BOLD}Enter a password to test (or 'q' to quit): {END}")
        print(f"{'─'*60}")
        
        # Check for quit command
        if password.lower() == 'q':
            print(f"\n{GREEN}Goodbye! Stay secure! 🔒{END}")
            print(f"{CYAN}You tested {password_count} password(s) in this session.{END}\n")
            break
        
        # Skip empty passwords
        if len(password.strip()) == 0:
            print(f"{YELLOW}⚠️  Please enter a valid password.{END}")
            continue
        
        # Increment password counter
        password_count += 1
        
        # Print the password being tested (with masking for security in real-world)
        print(f"\n{BOLD}Testing password: {BLUE}{'*' * len(password)}{END}")
        
        # Calculate password strength
        strength = password_strength(password)
        
        # Show visual strength bar
        bar = draw_strength_bar(strength)
        print(f"\n{BOLD}Strength Score: {strength}/5 {bar}{END}")
        
        # Show additional strength info
        if strength == 0:
            print(f"{RED}🔴 This password is NOT secure. Do NOT use it!{END}")
        elif strength == 1:
            print(f"{RED}🔴 This password is weak. Choose a stronger one!{END}")
        elif strength == 2:
            print(f"{YELLOW}🟡 This password is fair, but could be improved.{END}")
        elif strength == 3:
            print(f"{YELLOW}🟡 This password is moderate. Consider adding more variety.{END}")
        elif strength == 4:
            print(f"{GREEN}🟢 This password is strong! Good job!{END}")
        else:  # strength == 5
            print(f"{GREEN}🟢 Excellent! This is a very strong password!{END}")
        
        # Show complexity score
        complexity = word_complexity(password)
        print(f"{CYAN}Complexity Score: {complexity}/4{END}")


# PROGRAM ENTRY POINT

if __name__ == "__main__":
    # This code only runs if this file is executed directly
    # (not imported as a module)
    main()