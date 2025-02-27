from typing import List

class Solution:
    def trap(self, height: List[int]) -> int:
        n = len(height)
        res = 0

        l_max = [0] * n
        r_max = [0] * n

        l_max[0] = height[0]
        for i in range(1, n):
            l_max[i] = max(height[i], l_max[i-1])

        r_max[n-1] = height[n-1]
        for i in reversed(range(n-1)):
            r_max[i] = max(height[i], r_max[i+1])

        for i in range(n):
            res += min(l_max[i], r_max[i]) - height[i]

        return res

print(Solution().trap([0,1,0,2,1,0,1,3,2,1,2,1])) # 6
print(Solution().trap([4,2,0,3,2,5])) # 9
print(Solution().trap([4,2,3])) # 1