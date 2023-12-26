---
layout: post
title: "[Python] Two Sum / palindrome-number " #게시물 이름
tags: [pyhton, Leetcode, Algorithm] #태그 설정
categories: python #카테고리 설정
author: # 작성자
  - Byungineer
#toc : true #Table of Contents
---

## Two Sum
<https://leetcode.com/problems/two-sum/submissions/1090599733/>

### 문제 설명
Int로 구성된 Array의 숫자 2개를 조합해, 합이 target이 되는 Array의 Index Return

### 입출력 예
- nums = [2,7,11,15]
- target = 9   

- nums = [3,2,4]
- target = 6 

- nums = [3,3]
- target =6


**풀이**
```python
class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        for i in range (0,len(nums)):
            for j in range (i+1,len(nums)):
                if target == nums[i] + nums[j]:
                    return [i,j]
```

**다른 풀이**
```python
class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        num_to_index = {}
        for index, num in enumerate(nums):
            complement = target - num
            if complement in num_to_index:
                return [num_to_index[complement], index]
            num_to_index[num] = index
        return []
```

- 💡enumerate(iterable, startIndex)
    - Iterable : 반복할 개체
    - StartIndex : (Optional) startIndex에 제공된 값으로 시작하고 루프의 끝에 도달할 때까지 다음 항목에 대해 증가합니다.





## palindrome-number
<https://leetcode.com/problems/palindrome-number/>

### 문제 설명


### 입출력 예
- x = 121
- x = -121
- x = 10


**풀이**
```python
class Solution:
    def isPalindrome(self, x: int) -> bool:
        x = str(x)
        if x == x[::-1]:
            return True
        else:
            False
```

**다른 풀이**
```python

```

- 💡enumerate(iterable, startIndex)
    - Iterable : 반복할 개체
    - StartIndex : (Optional) startIndex에 제공된 값으로 시작하고 루프의 끝에 도달할 때까지 다음 항목에 대해 증가합니다.









https://leetcode.com/problems/remove-duplicates-from-sorted-array/

Change the array nums such that the first k elements of nums contain the unique elements in the order they were present in nums initially. The remaining elements of nums are not important as well as the size of nums.
Return k.
Custom Judge:

The judge will test your solution with the following code:

int[] nums = [...]; // Input array
int[] expectedNums = [...]; // The expected answer with correct length

int k = removeDuplicates(nums); // Calls your implementation

assert k == expectedNums.length;
for (int i = 0; i < k; i++) {
    assert nums[i] == expectedNums[i];
}
If all assertions pass, then your solution will be accepted.

 

Example 1:

Input: nums = [1,1,2]
Output: 2, nums = [1,2,_]
Explanation: Your function should return k = 2, with the first two elements of nums being 1 and 2 respectively.
It does not matter what you leave beyond the returned k (hence they are underscores).
Example 2:

Input: nums = [0,0,1,1,1,2,2,3,3,4]
Output: 5, nums = [0,1,2,3,4,_,_,_,_,_]
Explanation: Your function should return k = 5, with the first five elements of nums being 0, 1, 2, 3, and 4 respectively.
It does not matter what you leave beyond the returned k (hence they are underscores).
 

Constraints:

1 <= nums.length <= 3 * 104
-100 <= nums[i] <= 100
nums is sorted in non-decreasing order.


class Solution:
    """
    nums array를 중복을 제거한 상태로 갱신하고, k 를 return

    """
    def removeDuplicates(self, nums: List[int]) -> int:
        nums_tmp = list(set(nums))
        nums_tmp.sort()

        for i in range(len(nums_tmp)):
            nums[i] = nums_tmp[i]

        return len(nums_tmp)


https://leetcode.com/problems/remove-element/


class Solution:
    def removeElement(self, nums: List[int], val: int) -> int:
        """
        Given an integer array nums and an integer val, remove all occurrences of val in nums in-place. The order of the elements may be changed. Then return the number of elements in nums which are not equal to val.

Consider the number of elements in nums which are not equal to val be k, to get accepted, you need to do the following things:

Change the array nums such that the first k elements of nums contain the elements which are not equal to val. The remaining elements of nums are not important as well as the size of nums.
Return k.
        """
        for i in range (len(nums)-1,-1,-1):
            if nums[i] == val:
                nums.pop(i)
        nums.sort()
        

https://leetcode.com/problems/find-the-index-of-the-first-occurrence-in-a-string/

Example 1:

Input: haystack = "sadbutsad", needle = "sad"
Output: 0
Explanation: "sad" occurs at index 0 and 6.
The first occurrence is at index 0, so we return 0.
Example 2:

Input: haystack = "leetcode", needle = "leeto"
Output: -1
Explanation: "leeto" did not occur in "leetcode", so we return -1.


class Solution:
    def strStr(self, haystack: str, needle: str) -> int:
        """
        Given two strings needle and haystack, return the index of the first occurrence of needle in haystack, or -1 if needle is not part of haystack.
        """
        n = len(needle)
        for h in range (len(haystack)):
            print(h)
            if haystack[h] == needle[0]:    
                if haystack[h:h+len(needle)] == needle:
                    return h
                    break
                else:
                    continue
            else:
                continue
        print("ret2")
        return -1




https://leetcode.com/problems/search-insert-position/
Example 1:

Input: nums = [1,3,5,6], target = 5
Output: 2
Example 2:

Input: nums = [1,3,5,6], target = 2
Output: 1
Example 3:

Input: nums = [1,3,5,6], target = 7
Output: 4
 


class Solution:
    def searchInsert(self, nums: List[int], target: int) -> int:
        """
        Given a sorted array of distinct integers and a target value, return the index if the target is found. 
        If not, return the index where it would be if it were inserted in order.
        You must write an algorithm with O(log n) runtime complexity.
        """
        # O(log n) >> 2진 탐색
        # 정렬된 array nums
        left, right = 0, len(nums) - 1

        if target in nums:
            return nums.index(target)

        while left <= right:
            mid = left + (right - left) // 2

            if nums[mid] == target:
                return mid  # `target`을 찾았을 때의 인덱스
            elif nums[mid] < target:
                left = mid + 1
            else:
                right = mid - 1

        return left  # `target`이 삽입될 인덱스


https://leetcode.com/problems/length-of-last-word/

Example 1:

Input: s = "Hello World"
Output: 5
Explanation: The last word is "World" with length 5.
Example 2:

Input: s = "   fly me   to   the moon  "
Output: 4
Explanation: The last word is "moon" with length 4.
Example 3:

Input: s = "luffy is still joyboy"
Output: 6
Explanation: The last word is "joyboy" with length 6.


class Solution:
    def lengthOfLastWord(self, s: str) -> int:
        """
        Given a string s consisting of words and spaces, return the length of the last word in the string.

        A word is a maximal 
        substring
        consisting of non-space characters only.
         """
        tmp = s.split()
        return len(tmp[-1])


https://leetcode.com/problems/plus-one/

class Solution:
    def plusOne(self, digits: List[int]) -> List[int]:
        """
        You are given a large integer represented as an integer array digits, where each digits[i] is the ith digit of the integer. 
        The digits are ordered from most significant to least significant in left-to-right order. The large integer does not contain any leading 0's.

        Increment the large integer by one and return the resulting array of digits.
        """
        
        digits.reverse()
        dig = 0
        ans = []
        for i in range (len(digits)):
            dig += digits[i] * (10**i)
        dig += 1
        for d in str(dig):
            ans.append(int(d))
        
        return ans


https://leetcode.com/problems/add-binary/


class Solution:
    def addBinary(self, a: str, b: str) -> str:
        """
        Given two binary strings a and b, return their sum as a binary string.
        """
        num = int(a, 2) + int(b, 2)
        return str(format(num, 'b'))



https://leetcode.com/problems/sqrtx/

class Solution:
    def mySqrt(self, x: int) -> int:
        """
        Given a non-negative integer x, return the square root of x rounded down to the nearest integer. 
        The returned integer should be non-negative as well.

        You must not use any built-in exponent function or operator.

        For example, do not use pow(x, 0.5) in c++ or x ** 0.5 in python.
        """
        return int(sqrt(x))


        