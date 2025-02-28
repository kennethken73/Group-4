#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

class Solution {
public:
    int maxArea(vector<int>& height) 
    {
        int left = 0, right = height.size() - 1;  // Two pointers, one at the start and one at the end
        int maxWater = 0;  // Stores the maximum water container capacity found so far

        while (left < right) 
        {
            // Calculate the current container's area using the shorter height
            int minHeight = min(height[left], height[right]);
            int width = right - left;
            int currentArea = minHeight * width;

            // Update maxWater if the current area is larger
            if (currentArea > maxWater) 
            {
                maxWater = currentArea;
            }

            // Move the pointer that points to the shorter height inward
            if (height[left] < height[right]) 
            {
                left++;  // Move left pointer rightward to find a potentially taller boundary
            } 
            else 
            {
                right--; // Move right pointer leftward to find a potentially taller boundary
            }
        }
        return maxWater;
    }
};

int main()
{
    vector<int> height = {1, 8, 6, 2, 5, 4, 8, 3, 7};
    Solution obj;
    cout << obj.maxArea(height) << endl;
    return 0;
}
