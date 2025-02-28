import numpy as np
from math import gcd

# Vectorized GCD function for efficient computation across arrays
gcd_vectorized = np.vectorize(gcd)

def degrees_to_radians(degrees):
    """
    Converts an array of degree values to their equivalent fractional representation in radians.
    
    Args:
        degrees (array-like): An array of degree values to be converted.
        
    Returns:
        tuple: Two arrays representing the numerators and denominators of the reduced fractions.
    """
    numerators = np.array(degrees)
    denominators = np.full_like(numerators, 180)  # Create an array of 180s
    
    # Compute GCD for each pair to simplify the fraction
    gcds = gcd_vectorized(numerators, denominators)
    
    # Reduce fractions by dividing by their GCD
    numerators = numerators // gcds
    denominators = denominators // gcds
    
    return numerators, denominators

# Generate an array of angles from 0 to 360 degrees
degree_angles = np.arange(0, 361)

# Compute the reduced fractional representation of each angle in radians
numerators, denominators = degrees_to_radians(degree_angles)

# Iterate through the computed fractions and print them in a readable format
for angle, num, denom in zip(degree_angles, numerators, denominators):
    """
    This loop iterates over each angle and its corresponding reduced fraction representation in radians.
    
    - If the numerator is 0, the result is simply "0 Radians".
    - If the denominator is 1, the result is formatted as "Xπ Radians".
    - Otherwise, the result is presented as a fraction in the form "Xπ/Y Radians".
    
    This ensures that the output is both human-readable and mathematically correct.
    """
    if num == 0:
        print(f"{angle} Degrees = 0 Radians")
    elif denom == 1:
        print(f"{angle} Degrees = {num}π Radians")
    else:
        print(f"{angle} Degrees = {num}π/{denom} Radians")