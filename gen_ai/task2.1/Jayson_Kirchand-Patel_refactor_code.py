from random import randint
import numpy as np

# Function for formatting an array
def format_array(arr, arr_size):
    consec_nums = [arr[0]]
    formatted_str = ""

    # Loop to check if consecutive elements of array are consecutive integers
    for i in range(arr_size):
        if i == arr_size-1:
            # Create formatted string
            formatted_str += create_string(consec_nums)
            # Code duplication removed with help from ChatGPT
            # if len(consec_nums) >= 3:
            #     formatted_str += str(consec_nums[0]) + "-" + str(consec_nums[-1]) + ", "
            # else:
            #     for element in consec_nums:
            #         formatted_str += str(element) + ", "
            break

        if arr[i] == arr[i+1]-1:
            consec_nums.append(arr[i+1])
        else:
            # Create formatted string
            formatted_str += create_string(consec_nums)
            # Code duplication removed with help from ChatGPT
            # if len(consec_nums) >= 3:
            #     formatted_str += str(consec_nums[0]) + "-" + str(consec_nums[-1]) + ", "
            # else:
            #     for element in consec_nums:
            #         formatted_str += str(element) + ", "
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