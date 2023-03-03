---
layout: post
title: "[Python] JadenCase 문자열 만들기 / 최솟값 만들기" #게시물 이름
tags: [pyhton, programmers, Algorithm] #태그 설정
categories: Algorithm #카테고리 설정
author: # 작성자
  - Byungineer
#toc : true #Table of Contents
---
## JadenCase 문자열 만들기
<https://school.programmers.co.kr/learn/courses/30/lessons/12951>

### 문제 설명
_JadenCase란 모든 단어의 첫 문자가 대문자이고, 그 외의 알파벳은 소문자인 문자열입니다.   
단, 첫 문자가 알파벳이 아닐 때에는 이어지는 알파벳은 소문자로 쓰면 됩니다. (첫 번째 입출력 예 참고)   
문자열 s가 주어졌을 때, s를 JadenCase로 바꾼 문자열을 리턴하는 함수, solution을 완성해주세요._

### 제한 조건
- s는 길이 1 이상 200 이하인 문자열입니다.
- s는 알파벳과 숫자, 공백문자(" ")로 이루어져 있습니다.
  - 숫자는 단어의 첫 문자로만 나옵니다.
  - 숫자로만 이루어진 단어는 없습니다.
  - 공백문자가 연속해서 나올 수 있습니다.

### 입출력 예
s                     | return
--------------------- | ---------------------
3people unFollowed me |	3people Unfollowed Me
for the last week	  |	For The Last Week


**풀이**
```python
def solution(s):
    answer = ''

    # 전체 소문자 변환
    s = s.lower()
    words = list(s)
    for n in range (len(s)):
        
        if n == 0 and words[n].isalpha()==True:
            words[n]=words[n].upper()
        elif n != 0 and words[n-1]==" " and words[n].isalpha()==True:
            words[n]=words[n].upper()
        else:
            emp_num=1
        answer += words[n]  
            
    return answer
```

**다른 풀이**
```python
# 1.
def Jaden_Case(s):
    answer =[]
    for i in range(len(s.split())):
        answer.append(s.split()[i][0].upper() + s.split()[i].lower()[1:]) 
    return " ".join(answer)
# 2.
def solution(s):
    answer =''
    for i in s.split(' '):
        i = i.lower()
        i = i.capitalize()
        answer += i +' '
    return answer[:-1]
```


<aside>
💡 입력받는 s의 조건 중, 공백이 들어갈 수 있다는 것 때문에 쉽지만 헤맨 문제. 
</aside>


## 최솟값 만들기
<https://school.programmers.co.kr/learn/courses/30/lessons/12941>

### 문제 설명
_길이가 같은 배열 A, B 두개가 있습니다. 각 배열은 자연수로 이루어져 있습니다.   
배열 A, B에서 각각 한 개의 숫자를 뽑아 두 수를 곱합니다. 이러한 과정을 배열의 길이만큼 반복하며, 두 수를 곱한 값을 누적하여 더합니다.   
이때 최종적으로 누적된 값이 최소가 되도록 만드는 것이 목표입니다.   
(단, 각 배열에서 k번째 숫자를 뽑았다면 다음에 k번째 숫자는 다시 뽑을 수 없습니다.)   

예를 들어 A = [1, 4, 2] , B = [5, 4, 4] 라면   
- A에서 첫번째 숫자인 1, B에서 첫번째 숫자인 5를 뽑아 곱하여 더합니다. (누적된 값 : 0 + 5(1x5) = 5)
- A에서 두번째 숫자인 4, B에서 세번째 숫자인 4를 뽑아 곱하여 더합니다. (누적된 값 : 5 + 16(4x4) = 21)
- A에서 세번째 숫자인 2, B에서 두번째 숫자인 4를 뽑아 곱하여 더합니다. (누적된 값 : 21 + 8(2x4) = 29)   
즉, 이 경우가 최소가 되므로 29를 return 합니다.

배열 A, B가 주어질 때 최종적으로 누적된 최솟값을 return 하는 solution 함수를 완성해 주세요._

### 제한 조건
- 배열 A, B의 크기 : 1,000 이하의 자연수
- 배열 A, B의 원소의 크기 : 1,000 이하의 자연수

### 입출력 예
A                     | B                     | answer
--------------------- | --------------------- | ---------------------
[1, 4, 2]             | [5, 4, 4]             | 29
[1, 2]                | [3, 4]                | 10

### 입출력 예 설명
입출력 예 #2
A에서 첫번째 숫자인 1, B에서 두번째 숫자인 4를 뽑아 곱하여 더합니다. (누적된 값 : 4) 다음, A에서 두번째 숫자인 2, B에서 첫번째 숫자인 3을 뽑아 곱하여 더합니다. (누적된 값 : 4 + 6 = 10)
이 경우가 최소이므로 10을 return 합니다.

**풀이**
```python
def solution(A,B):
    answer = 0
		# 곱의 값이 작은수로 더해야 하기 때문에, B를 역순으로 정렬하여 곱
    sorted_a=sorted(A)
    sorted_b=sorted(B, reverse=True)
    # print(sorted_a,sorted_b)
    for n in range (len(A)):
        answer+= sorted_a[n]*sorted_b[n]

    return answer
```

**다른 풀이**
```python
def getMinSum(A,B):
    return sum(a*b for a, b in zip(sorted(A), sorted(B, reverse = True)))
```
