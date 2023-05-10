---
layout: post
title: "[Python] 구명보트 / N개의 최소공배수" #게시물 이름
tags: [pyhton, programmers, Algorithm] #태그 설정
categories: python #카테고리 설정
author: # 작성자
  - Byungineer
#toc : true #Table of Contents
---

## 구명보트
<https://school.programmers.co.kr/learn/courses/30/lessons/42885>

### 문제 설명
_무인도에 갇힌 사람들을 구명보트를 이용하여 구출하려고 합니다. 구명보트는 작아서 한 번에 최대 2명씩 밖에 탈 수 없고, 무게 제한도 있습니다.

예를 들어, 사람들의 몸무게가 [70kg, 50kg, 80kg, 50kg]이고 구명보트의 무게 제한이 100kg이라면 2번째 사람과 4번째 사람은 같이 탈 수 있지만 1번째 사람과 3번째 사람의 무게의 합은 150kg이므로 구명보트의 무게 제한을 초과하여 같이 탈 수 없습니다.

구명보트를 최대한 적게 사용하여 모든 사람을 구출하려고 합니다.

사람들의 몸무게를 담은 배열 people과 구명보트의 무게 제한 limit가 매개변수로 주어질 때, 모든 사람을 구출하기 위해 필요한 구명보트 개수의 최솟값을 return 하도록 solution 함수를 작성해주세요._

### 제한 조건
- 무인도에 갇힌 사람은 1명 이상 50,000명 이하입니다.
- 각 사람의 몸무게는 40kg 이상 240kg 이하입니다.
- 구명보트의 무게 제한은 40kg 이상 240kg 이하입니다.
- 구명보트의 무게 제한은 항상 사람들의 몸무게 중 최댓값보다 크게 주어지므로 사람들을 구출할 수 없는 경우는 없습니다.

### 입출력 예

people                | limit                 | return
--------------------- | --------------------- | ---------------------
[70, 50, 80, 50]      | 100                   | 3
[70, 80, 50]          | 100                   | 3


**풀이**
```python
def solution(people,limit):
    answer=0
    people.sort()
    
    light = 0
    heavy = len(people) - 1

    while light <= heavy: ## 몸무게 많이 나가는 사람을 기준으로 적게 나가는 사람과의 합이 limit을 넘는지 체크.
        if people[light] + people[heavy] <= limit:
            light += 1
        heavy -= 1
        answer+=1
    return answer



### 효율성 테스트 1개 실패  >>>>>>>>>>>>>> deque 라이브러리를 이용하면 패스
def solution(people,limit):
    answer=0
    people.sort()
  
    while people:
        if len(people) >= 2: # people에 1명남으면 pop 할 때 에러
            if people[-1] + people[0] <= limit:
                people.pop()
                people.pop(0)
                answer+=1
            else:
                people.pop()
                answer+=1
        else:
            people.pop()
            answer+=1           
    return answer
```

**다른 풀이**
```python
from collections import deque

def solution(people, limit):
    result = 0
    deque_people = deque(sorted(people))

    while deque_people:
        left = deque_people.popleft()
        if not deque_people:
            return result + 1
        right = deque_people.pop()
        if left + right > limit:
            deque_people.appendleft(left)
        result += 1
    return result
```


<aside>
💡 - 이번 문제에서 알아두면 좋을 함수
    - pop(0) 의 경우 데이터를 지우고 한칸씩 앞으로 당기기 때문에 O(1)이 아니라 O(n)이 됩니다. 그래서 people을 collections.deque()로 만들어 popleft()를 사용하면 시간초과가 나지 않고 해결됩니다.
    - 그리디 알고리즘 사용시 투포인터(데이터 정렬 후 우측과 좌측 끝 인자) 추출로 사용하면 도움이 될 듯합니다.
</aside>



## N개의 최소공배수
<https://school.programmers.co.kr/learn/courses/30/lessons/12953>

### 문제 설명
_두 수의 최소공배수(Least Common Multiple)란 입력된 두 수의 배수 중 공통이 되는 가장 작은 숫자를 의미합니다. 예를 들어 2와 7의 최소공배수는 14가 됩니다. 정의를 확장해서, n개의 수의 최소공배수는 n 개의 수들의 배수 중 공통이 되는 가장 작은 숫자가 됩니다. n개의 숫자를 담은 배열 arr이 입력되었을 때 이 수들의 최소공배수를 반환하는 함수, solution을 완성해 주세요._

### 제한 조건
- arr은 길이 1이상, 15이하인 배열입니다.
- arr의 원소는 100 이하인 자연수입니다.

### 입출력 예

arr                   | return
--------------------- | ---------------------
[2,6,8,14]            | 168
[1,2,3]               | 6


**풀이**
```python
def solution(arr):
    answer = arr[0]
    LCM_list=[]
        
    # 최대공약수를 구하고, 두 수의 값을 최대공약수로 나누면 최대공배수
    # ab/(a와b의 최대공약수)
    for a in range(1,len(arr)):
        for i in range(min(answer,arr[a]),0,-1):
            if answer % i == 0 and arr[a] % i == 0:
                answer = int(answer*arr[a]/i)
                break
    return answer
```

**다른 풀이**
```python
from fractions import gcd

def nlcm(num):      
    answer = num[0]
    for n in num:
        answer = n * answer / gcd(n, answer)

    return answ

### gcd를 구현 한 것.
def gcd(x, y):
   # y가 0이 될 때까지 반복
   while y:
       # y를 x에 대입
       # x를 y로 나눈 나머지를 y에 대입
       x, y = y, x % y
   return x

## python 3.9 이상 math.lcm 라이브러리 사용도 가능.
```
