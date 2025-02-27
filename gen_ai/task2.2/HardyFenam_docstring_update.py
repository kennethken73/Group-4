from typing import List

class Solution:
    def trap(self, height: List[int]) -> int:
        if not height:
            return 0

        left, right = 0, len(height) - 1
        left_max, right_max = height[left], height[right]
        res = 0

        while left < right:
            if height[left] < height[right]:
                left_max = max(left_max, height[left])
                res += left_max - height[left]
                left += 1
            else:
                right_max = max(right_max, height[right])
                res += right_max - height[right]
                right -= 1

        return res

# Test cases
print(Solution().trap([0,1,0,2,1,0,1,3,2,1,2,1]))  # Output: 6
print(Solution().trap([4,2,0,3,2,5]))  # Output: 9
print(Solution().trap([4,2,3]))  # Output: 1
