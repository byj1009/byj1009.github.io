---
layout: post
title: "[Python] 다음 큰 숫자 / 카펫" #게시물 이름
tags: [pyhton, programmers, Algorithm] #태그 설정
categories: Algorithm #카테고리 설정
author: # 작성자
  - Byungineer
#toc : true #Table of Contents
---
## 다음 큰 숫자
<https://school.programmers.co.kr/learn/courses/30/lessons/12909>

### 문제 설명
_자연수 n이 주어졌을 때, n의 다음 큰 숫자는 다음과 같이 정의 합니다.

- 조건 1. n의 다음 큰 숫자는 n보다 큰 자연수 입니다.
- 조건 2. n의 다음 큰 숫자와 n은 2진수로 변환했을 때 1의 갯수가 같습니다.
- 조건 3. n의 다음 큰 숫자는 조건 1, 2를 만족하는 수 중 가장 작은 수 입니다.   
예를 들어서 78(1001110)의 다음 큰 숫자는 83(1010011)입니다.

자연수 n이 매개변수로 주어질 때, n의 다음 큰 숫자를 return 하는 solution 함수를 완성해주세요._

### 제한 사항
- n은 1,000,000 이하의 자연수 입니다.

### 입출력 예
n | return
--------------------- | ---------------------
78                    | 83
15                    | 23


**풀이**
```python
def solution(n):
    tmp=0
    answer=0
    check_num=str(format(n,'b')).count("1") # 2진법, 1의 갯수  >> 2진법은 str 타입 변환없이 바로 사용이 가능하다.
     
    while True:
        n += 1 
        tmp = str(format(n,'b')).count("1")
        print(tmp)
        if check_num == tmp:
            answer = n
            break

    return answer
```

**다른 풀이**
```python
def nextBigNumber(n):
    num1 = bin(n).count('1')
    while True:
        n = n + 1
        if num1 == bin(n).count('1'):
            break
    return n

```


<aside>
💡 2진법 변환은 bin, format()   
2진법은 count가 바로 사용이 됨.
</aside>


## 카펫
<https://school.programmers.co.kr/learn/courses/30/lessons/42842>

### 문제 설명
_Leo는 카펫을 사러 갔다가 아래 그림과 같이 중앙에는 노란색으로 칠해져 있고 테두리 1줄은 갈색으로 칠해져 있는 격자 모양 카펫을 봤습니다._
<img src="/image/programmers_carpet.png" alt="python_venv" style="height: 400px; width:600px;"/>   

Leo는 집으로 돌아와서 아까 본 카펫의 노란색과 갈색으로 색칠된 격자의 개수는 기억했지만, 전체 카펫의 크기는 기억하지 못했습니다.

Leo가 본 카펫에서 갈색 격자의 수 brown, 노란색 격자의 수 yellow가 매개변수로 주어질 때 카펫의 가로, 세로 크기를 순서대로 배열에 담아 return 하도록 solution 함수를 작성해주세요.

### 제한 조건
- 갈색 격자의 수 brown은 8 이상 5,000 이하인 자연수입니다.
- 노란색 격자의 수 yellow는 1 이상 2,000,000 이하인 자연수입니다.
- 카펫의 가로 길이는 세로 길이와 같거나, 세로 길이보다 깁니다.

### 입출력 예
brown                 | yellow                | return
--------------------- | --------------------- | ---------------------  
10                    | 2                     | [4, 3] 
8                     | 1                     | [3, 3]
24                    | 24                    | [8, 6]


**풀이**
```python
def solution(brown, yellow):
    answer = []
    # b = a(2x+2y) + 4    
    for y in range (1, yellow+1): # y : 세로
        val_y = yellow // y # val_y : 가로
        print(y)
        if yellow % y == 0: # y가 yellow 의 약수일 때

            if brown == val_y*2 + y*2 + 4:
                answer.append(val_y+2)
                answer.append(y+2)
                break
                
    return answer
```

**다른 풀이**
```python
#1. 가로 * 세로 = 격자 합, 둘레의 합(가로*2 + 세로*2 - 겹치는부분4) = 갈색 둘레
def solution(brown, red):
    for i in range(1, int(red**(1/2))+1):
        if red % i == 0:
            if 2*(i + red//i) == brown-4:
                return [red//i+2, i+2]


#2. 근의 공식 활용
import math
def solution(brown, yellow):
    w = ((brown+4)/2 + math.sqrt(((brown+4)/2)**2-4*(brown+yellow)))/2
    h = ((brown+4)/2 - math.sqrt(((brown+4)/2)**2-4*(brown+yellow)))/2
    return [w,h]
```
