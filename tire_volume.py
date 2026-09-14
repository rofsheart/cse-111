"""
Compute the approximate volume of a car tire and save to a file.
"""
#The basic structure to be used 
import math

def main():
    # Get tire specifications from the user
    width = input("Enter the width of the tire in mm: ")
    aspect = input("Enter the aspect ratio of the tire: ")
    diameter = input("Enter the diameter of the wheel in inches: ")

    # Calculate the volume using the compute_tire_volume function
    volume = compute_tire_volume(width, aspect, diameter)

def compute_tire_volume(width, aspect, diameter):
    """ Compute the approximate volume of a tire in liters.
    Parameters:
        width: Width of the tire in mm
        aspect: Aspect ratio of the tire
        diameter: Diameter of the wheel in inches
    Returns: Approximate volume of the tire in liters.
    """
    volume_of_tire = (math.pi * width**2 * aspect * (width * aspect + 2540 * diameter)) / 10000000000
    return volume_of_tire








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