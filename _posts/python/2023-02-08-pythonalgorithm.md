---
layout: post
title: "[Python] 괄호 회전하기 / 행렬의 곱셈" #게시물 이름
tags: [pyhton, programmers, Algorithm] #태그 설정
categories: Algorithm3 #카테고리 설정
author: # 작성자
  - Byungineer
#toc : true #Table of Contents
published: true
---

## 괄호 회전하기
<https://school.programmers.co.kr/learn/courses/30/lessons/76502>

### 문제 설명
_다음 규칙을 지키는 문자열을 올바른 괄호 문자열이라고 정의합니다.

- (), [], {} 는 모두 올바른 괄호 문자열입니다.
- 만약 A가 올바른 괄호 문자열이라면, (A), [A], {A} 도 올바른 괄호 문자열입니다. 예를 들어, [] 가 올바른 괄호 문자열이므로, ([]) 도 올바른 괄호 문자열입니다.
- 만약 A, B가 올바른 괄호 문자열이라면, AB 도 올바른 괄호 문자열입니다. 예를 들어, {} 와 ([]) 가 올바른 괄호 문자열이므로, {}([]) 도 올바른 괄호 문자열입니다.   

대괄호, 중괄호, 그리고 소괄호로 이루어진 문자열 s가 매개변수로 주어집니다. 이 s를 왼쪽으로 x (0 ≤ x < (s의 길이)) 칸만큼 회전시켰을 때 s가 올바른 괄호 문자열이 되게 하는 x의 개수를 return 하도록 solution 함수를 완성해주세요._

### 제한 조건
- s의 길이는 1 이상 1,000 이하입니다.

### 입출력 예

s                     | return
--------------------- | ---------------------
"[](){}"              | 3
"}]()[{"              | 2
"[)(]"                | 0
"}}}"                 | 0

### 입출력 예 설명
입출력 예 #1   
다음 표는 "[](){}" 를 회전시킨 모습을 나타낸 것입니다.

x                  | s를 왼쪽으로 x칸만큼 회전 | 올바른 괄호 문자열?
------------------ | --------------------- | ---------------------
0                  | "[](){}"              | O
1                  | "](){}["              | X
2                  | "(){}[]"              | O
3                  | "){}[]("              | X
4                  | "{}[]()"              | O
5                  | "}[](){"              | X

올바른 괄호 문자열이 되는 x가 3개이므로, 3을 return 해야 합니다.   

입출력 예 #2   
다음 표는 "}]()[{" 를 회전시킨 모습을 나타낸 것입니다.

x               | s를 왼쪽으로 x칸만큼 회전 | 올바른 괄호 문자열?
--------------- | --------------------- | ---------------------
0               | "}]()[{"              | X
1               | "]()[{}"              | X
2               | "()[{}]"              | O
3               | ")[{}]("              | X
4               | "[{}]()"              | O
5               | "{}]()["              | X

올바른 괄호 문자열이 되는 x가 2개이므로, 2를 return 해야 합니다.

입출력 예 #3   
s를 어떻게 회전하더라도 올바른 괄호 문자열을 만들 수 없으므로, 0을 return 해야 합니다.

입출력 예 #4   
s를 어떻게 회전하더라도 올바른 괄호 문자열을 만들 수 없으므로, 0을 return 해야 합니다.


**풀이**
```python
def solution(s):
    answer = 0
    s_list = list(map(str,s))
    for i in range(len(s)):
        tmp=s_list.pop(0)
        s_list.append(tmp)
        stack = []
        for e in s_list:
            if e == '(' or e == '[' or e == '{':
                stack.append(e)
            try:
                if e == ')' and stack[-1] == '(':
                    stack.pop()
                elif e == ']' and stack[-1] == '[':
                    stack.pop()
                elif e == '}' and stack[-1] == '{':
                    stack.pop()
            except:
                stack = ["break"]
                print("break")
                break
        if stack == []:
            answer += 1
    return answer
```

반례가 존재하는 풀이 `[{]}`
```python
# 반례 !!!! [{]}
def solution(s):
    answer = 0
    s_list = list(map(str,s))

    for i in range(len(s)):
        tmp=s_list.pop(0)
        s_list.append(tmp)
        check_1 = 0
        check_2 = 0
        check_3 = 0
        for s_bracket in s_list:
            if s_bracket == "(":
                check_1 += 1
            elif s_bracket == ")":
                check_1 -= 1
            elif s_bracket == "[":
                check_2 += 1
            elif s_bracket == "]":
                check_2 -= 1
            elif s_bracket == "{":
                check_3 += 1
            else:
                check_3 -= 1
            if check_1 < 0 or check_2 < 0 or check_3 < 0:
                break
        if check_1 == 0 and check_2 == 0 and check_3 == 0:
            answer+=1
    return answer
```




**다른 풀이**
```python
def solution(s):
    answer = 0
    for i in range(len(s)):
        rotate_s=s[i:]+s[:i]
        if check(rotate_s):
            answer+=1
    return answer

def check(str):
    stack=[]

    for s in str:
        if s in ('(','[','{'):
            stack.append(s)
        else:
            if not stack:
                return False
            item=stack.pop()
            if s == ')' and item != '(':
                return False
            elif s == ']' and item != '[':
                return False
            elif s == '}' and item != '{':
                return False

    # 문자열 체크 후 스택이 비어있으면 올바른 문자열, 아니면 올바른 문자열이 아님!
    if len(stack)==0:
        return True
    return False
```

## 행렬의 곱셈
<https://school.programmers.co.kr/learn/courses/30/lessons/42586>

### 문제 설명
_2차원 행렬 arr1과 arr2를 입력받아, arr1에 arr2를 곱한 결과를 반환하는 함수, solution을 완성해주세요._

### 제한 조건
- 행렬 arr1, arr2의 행과 열의 길이는 2 이상 100 이하입니다.
- 행렬 arr1, arr2의 원소는 -10 이상 20 이하인 자연수입니다.
- 곱할 수 있는 배열만 주어집니다.

### 입출력 예

arr1                     | arr2                  | return                    
------------------------ | --------------------- | ---------------------
[[1, 4], [3, 2], [4, 1]] | [[3, 3], [3, 3]]   | [[15, 15], [15, 15], [15, 15]]
[[2, 3, 2], [4, 2, 4], [3, 1, 4]] | [[5, 4, 3], [2, 4, 1], [3, 1, 1]] | [[22, 22, 11], [36, 28, 18], [29, 20, 14]]


**풀이**
```python
def solution(arr1, arr2):
    answer = [[0 for w in range(len(arr2[0]))] for h in range(len(arr1))]
    for x in range(len(arr1)): 
        for y in range(len(arr1[0])):
            for z in range(len(arr2[0])):
                answer[x][z]+=arr1[x][y]*arr2[y][z]
    return answer
```

**다른 풀이**
```python
def productMatrix(A, B):
    return [[sum(a*b for a, b in zip(A_row,B_col)) for B_col in zip(*B)] for A_row in A]
```

💡 zip() 내장함수

<https://docs.python.org/ko/3/library/functions.html?highlight=zip#zip>