"""
The size of a car tire in the United States is represented with three numbers like this: 205/60R15. 
The first number is the width of the tire in millimeters. The second number is the aspect ratio. The third 
number is the diameter in inches of the wheel that the tire fits.

Compute the approximate volume of a car tire and save to a file.
"""

import math
from datetime import datetime

def main():
    # Get tire specifications from the user
    width = float(input("Enter the width of the tire in mm (ex 205): "))
    aspect = float(input("Enter the aspect ratio of the tire (ex 60): "))
    diameter = float(input("Enter the diameter of the wheel in inches (ex 15): "))
    
    # Calculate the volume using the formula:
    # v = (π × w² × a × (w × a + 2,540 × d)) / 10,000,000,000
    volume = (math.pi * width**2 * aspect * (width * aspect + 2540 * diameter)) / 10000000000
    
    # Get current date from operating system
    current_date = datetime.now()
    formatted_date = current_date.strftime("%Y-%m-%d")
    
    # Print the result with 2 decimal places
    print(f"The approximate volume is {volume:.2f} liters")
    
    # Open the volumes.txt file for appending
    with open("volumes.txt", "a") as file:
        # Print all required values to the file
        file.write(f"{formatted_date}, {width:.0f}, {aspect:.0f}, {diameter:.0f}, {volume:.2f}\n")

    # Extra creativity: Tell the user where the data was saved
    print(f"Tire information saved to volumes.txt")

# Call the main function
main()