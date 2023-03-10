---
layout: post
title: "[Python] 숫자의 표현 / 피보나치 수" #게시물 이름
tags: [pyhton, programmers, Algorithm] #태그 설정
categories: Algorithm #카테고리 설정
author: # 작성자
  - Byungineer
#toc : true #Table of Contents
---
## 숫자의 표현
<https://school.programmers.co.kr/learn/courses/30/lessons/12909>

### 문제 설명
_Finn은 요즘 수학공부에 빠져 있습니다. 수학 공부를 하던 Finn은 자연수 n을 연속한 자연수들로 표현 하는 방법이 여러개라는 사실을 알게 되었습니다. 예를들어 15는 다음과 같이 4가지로 표현 할 수 있습니다.

- 1 + 2 + 3 + 4 + 5 = 15
- 4 + 5 + 6 = 15
- 7 + 8 = 15
- 15 = 15   
자연수 n이 매개변수로 주어질 때, 연속된 자연수들로 n을 표현하는 방법의 수를 return하는 solution를 완성해주세요._

### 제한 조건
- n은 10,000 이하의 자연수 입니다.

### 입출력 예
n                     | return
--------------------- | ---------------------
15	                  | 4


**풀이**
```python
def solution(n):
    cnt=1 # n 그자체로 1회
    for i in range(1,n+1):
        num=i
        for j in range(i+1,n+1):
            num+=j
            if num<n:
                continue
            elif num==n:
                cnt+=1
            else:
                break     
    return cnt
```

**다른 풀이**
```python
# 1.
def expressions(num):
    return len([i  for i in range(1,num+1,2) if num % i is 0]) 

```


<aside>
💡 Programmers의 다른 풀이를 보다보면 한줄로 된 풀이가 심심치않게 보인다. 심플한 문장을 한줄로 압축하여 표현하는 것이 가독성에 도움이 되는 경우도 있지만, 남용은 피해야할 것 같다. 

~~이게 무슨 소리인지 알아보기가 너무 힘들다.~~
</aside>


## 피보나치 수
<https://school.programmers.co.kr/learn/courses/30/lessons/70129>

### 문제 설명
_피보나치 수는 F(0) = 0, F(1) = 1일 때, 1 이상의 n에 대하여 F(n) = F(n-1) + F(n-2) 가 적용되는 수 입니다.

예를들어   
- F(2) = F(0) + F(1) = 0 + 1 = 1
- F(3) = F(1) + F(2) = 1 + 1 = 2
- F(4) = F(2) + F(3) = 1 + 2 = 3
- F(5) = F(3) + F(4) = 2 + 3 = 5   
와 같이 이어집니다.

2 이상의 n이 입력되었을 때, n번째 피보나치 수를 1234567으로 나눈 나머지를 리턴하는 함수, solution을 완성해 주세요._

### 제한 조건
- n은 2 이상 100,000 이하인 자연수입니다.

### 입출력 예
n                     | return
--------------------- | ---------------------
3                     | 2 
5                     | 5

### 입출력 예 설명
피보나치수는 0번째부터 0, 1, 1, 2, 3, 5, ... 와 같이 이어집니다.

**풀이**
```python
def solution(n):
    fibo_list=[0,1] # F(0), F(1)
    
    for i in range(2,n+1):
        append_num=fibo_list[i-1]+fibo_list[i-2]
        fibo_list.append(append_num)
        
    return fibo_list[n]%1234567
```

**다른 풀이**
```python
def fibonacci(num):
    a,b = 0,1
    for i in range(num):
        a,b = b,a+b
    return a
```
