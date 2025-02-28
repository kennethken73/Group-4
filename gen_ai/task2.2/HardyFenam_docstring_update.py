from typing import List

class Solution:
    def trap(self, height: List[int]) -> int:
        """
        Calculates the amount of water that can be trapped between bars after rainfall.

        Uses a two-pointer approach to efficiently compute the trapped water.

        Args:
            height (List[int]): A list of non-negative integers representing the heights of the bars.

        Returns:
            int: The total amount of trapped rainwater.
        """

        # If the height list is empty, no water can be trapped.
        if not height:
            return 0

        # Initialize two pointers, one starting from the left and one from the right.
        left, right = 0, len(height) - 1
        
        # Track the maximum height encountered from the left and right sides.
        left_max, right_max = height[left], height[right]

        # Variable to store the total trapped water.
        res = 0

        # Process the height array until the two pointers meet.
        while left < right:
            if height[left] < height[right]:
                # Update left_max to the highest wall encountered from the left.
                left_max = max(left_max, height[left])
                
                # Water trapped at current left index is the difference between left_max and the current height.
                res += left_max - height[left]
                
                # Move the left pointer one step to the right.
                left += 1
            else:
                # Update right_max to the highest wall encountered from the right.
                right_max = max(right_max, height[right])
                
                # Water trapped at current right index is the difference between right_max and the current height.
                res += right_max - height[right]
                
                # Move the right pointer one step to the left.
                right -= 1

        # Return the total trapped water.
        return res

# Example test cases
print(Solution().trap([0,1,0,2,1,0,1,3,2,1,2,1]))  # Output: 6
print(Solution().trap([4,2,0,3,2,5]))  # Output: 9
print(Solution().trap([4,2,3]))  # Output: 1
