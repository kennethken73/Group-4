import numpy as np
from math import gcd

# Vectorized GCD function
gcd_vectorized = np.vectorize(gcd)

def degrees_to_radians(degrees):
    numerators = np.array(degrees)
    denominators = np.full_like(numerators, 180)  # Create an array of 180s
    
    # Compute GCD for each pair
    gcds = gcd_vectorized(numerators, denominators)
    
    # Reduce fractions
    numerators = numerators // gcds
    denominators = denominators // gcds
    
    return numerators, denominators

# Generate angles as a NumPy array
degree_angles = np.arange(0, 361)

# Compute reduced fractions
numerators, denominators = degrees_to_radians(degree_angles)

# Format and print results
for angle, num, denom in zip(degree_angles, numerators, denominators):
    if num == 0:
        print(f"{angle} Degrees = 0 Radians")
    elif denom == 1:
        print(f"{angle} Degrees = {num}π Radians")
    else:
        print(f"{angle} Degrees = {num}π/{denom} Radians")