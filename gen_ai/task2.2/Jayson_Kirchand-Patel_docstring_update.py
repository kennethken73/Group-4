from random import randint
import numpy as np

def format_array(arr, arr_size):
    """
    Formats an array of integers into a string representation that groups consecutive 
    numbers into ranges while keeping individual numbers separate.

    Args:
        arr (list[int]): The input array of integers.
        size (int): The size of the array.

    Returns:
        str: A formatted string representing individual numbers and consecutive integer ranges.

    Example:
        >>> format_consecutive_ranges([1, 2, 3, 5, 6, 8, 9, 10], 8)
        '1-3, 5, 6, 8-10'

        >>> format_consecutive_ranges([1, 3, 4, 5, 7], 5)
        '1, 3-5, 7'
    """
    consec_nums = [arr[0]]
    formatted_str = ""

    # Loop to check if consecutive elements of array are consecutive integers
    for i in range(arr_size):
        if i == arr_size-1:
            # Create formatted string
            formatted_str += create_string(consec_nums)
            break

        if arr[i] == arr[i+1]-1:
            consec_nums.append(arr[i+1])
        else:
            # Create formatted string
            formatted_str += create_string(consec_nums)
            consec_nums = [arr[i+1]]

    # Return formatted string
    return formatted_str.removesuffix(", ")

# Create part of formatted string
def create_string(consec_nums):
    if len(consec_nums) >= 3:
        return ('-'.join(str(consec_nums[i]) for i in range(0, -2, -1))) + ', '
    else:
        return (', '.join(str(element) for element in consec_nums)) + ', '

# Testing functionality
# Create array or random size and values
arr_size = randint(3, 30)
arr = np.empty(arr_size, np.int8)
for i in range(arr_size):
    arr = np.insert(arr, i, randint(-20, 20))

# Keep only unique values
arr = np.unique(arr)    # Returns sorted array
arr_size = arr.size

# Print array
print("Array before formatting:")
print(arr)

# Format array using function
str = format_array(arr, arr_size)

# Print formatted string
print("\nArray after formatting")
print(str)