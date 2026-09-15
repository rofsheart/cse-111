"""
Compute the approximate volume of a car tire and save to a file.
"""
#The basic structure to be used 
from datetime import datetime
import math

def main():
    # Get tire specifications from the user
    width = float(input("Enter the width of the tire in mm(ex 205): "))
    aspect = float(input("Enter the aspect ratio of the tire(ex 60): "))
    diameter = float(input("Enter the diameter of the wheel in inches(ex 15): "))

    # Calculate the volume using the compute_tire_volume function
    volume = compute_tire_volume(width, aspect, diameter)

    print(f"The approximate volume is {volume:.2f} liters")
    datetime.now(tz=None)

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








