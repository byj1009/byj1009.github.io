---
layout: post
title: "[Python] 올바른 괄호 / 이진변환 반복하기" #게시물 이름
tags: [pyhton, programmers, Algorithm] #태그 설정
categories: Algorithm #카테고리 설정
author: # 작성자
  - Byungineer
#toc : true #Table of Contents
---
## 올바른 괄호
<https://school.programmers.co.kr/learn/courses/30/lessons/12909>

### 문제 설명
_괄호가 바르게 짝지어졌다는 것은 '(' 문자로 열렸으면 반드시 짝지어서 ')' 문자로 닫혀야 한다는 뜻입니다. 예를 들어   
"()()" 또는 "(())()" 는 올바른 괄호입니다.   
")()(" 또는 "(()(" 는 올바르지 않은 괄호입니다.   
'(' 또는 ')' 로만 이루어진 문자열 s가 주어졌을 때, 문자열 s가 올바른 괄호이면 true를 return 하고,   
올바르지 않은 괄호이면 false를 return 하는 solution 함수를 완성해 주세요._

### 제한 조건
- 문자열 s의 길이 : 100,000 이하의 자연수
- 문자열 s는 '(' 또는 ')' 로만 이루어져 있습니다.

### 입출력 예

s                     | return
--------------------- | ---------------------
"()()"	              | true
"(())()"              |	true
")()("	              | false
"(()("	              | false


**풀이**
```python
def solution(s):
    answer = True
    temp=0
    input_list=list(map(str,s))
        
    for ip in input_list:
        if ip == "(":    
            temp += 1
        else:
            temp -= 1
            
        if temp < 0:
            answer = False
            break
    if temp != 0:
        answer = False
        
    return answer
```

**다른 풀이**
```python
# 1.
def is_pair(s):
    x = 0
    for w in s:
        if x < 0:
            break
        x = x+1 if w=="(" else x-1 if w==")" else x
    return x==0

# 2. del, remove 대체 가능
def is_pair(s):
    st = list()
    for c in s:
        if c == '(':
            st.append(c)

        if c == ')':
            try:
                st.pop()
            except IndexError:
                return False

    return len(st) == 0
```


## 이진변환 반복하기
<https://school.programmers.co.kr/learn/courses/30/lessons/70129>

### 문제 설명
_0과 1로 이루어진 어떤 문자열 x에 대한 이진 변환을 다음과 같이 정의합니다.

1. x의 모든 0을 제거합니다.   
2. x의 길이를 c라고 하면, x를 "c를 2진법으로 표현한 문자열"로 바꿉니다.   

예를 들어, x = "0111010"이라면, x에 이진 변환을 가하면 x = "0111010" -> "1111" -> "100" 이 됩니다.   
0과 1로 이루어진 문자열 s가 매개변수로 주어집니다. s가 "1"이 될 때까지 계속해서 s에 이진 변환을 가했을 때,    
이진 변환의 횟수와 변환 과정에서 제거된 모든 0의 개수를 각각 배열에 담아 return 하도록 solution 함수를 완성해주세요._

### 제한 조건
- s의 길이는 1 이상 150,000 이하입니다.
- s에는 '1'이 최소 하나 이상 포함되어 있습니다.

### 입출력 예
A                     | B                    
--------------------- | ---------------------
"110010101001"	      | [3,8]
"01110"           	  | [3,3]
"1111111"	          | [4,1]

### 입출력 예 설명
입출력 예 #1   
- "110010101001"이 "1"이 될 때까지 이진 변환을 가하는 과정은 다음과 같습니다.

회차	              | 이진 변환 이전	      | 제거할 0의 개수	      | 0 제거 후 길이	     | 이진 변환 결과
--------------------- | ---------------------| ---------------------| ---------------------| ---------------------
1	                  | "110010101001"	     | 6	                | 6                    | "110"
2                     | "110"                | 1                    | 2                    | "10"
3                     |	"10"                 | 1                    | 1                    | "1"

입출력 예 #2   
- "01110"이 "1"이 될 때까지 이진 변환을 가하는 과정은 다음과 같습니다.
회차	              | 이진 변환 이전	      | 제거할 0의 개수	      | 0 제거 후 길이	     | 이진 변환 결과
--------------------- | ---------------------| ---------------------| ---------------------| ---------------------
1	                  |	"01110"	             | 2	                | 3	                   | "11"
2	                  |	"11"	             | 0	                | 2	                   | "10"
3	                  |	"10"	             | 1	                | 1	                   | "1"

- 3번의 이진 변환을 하는 동안 3개의 0을 제거했으므로, [3,3]을 return 해야 합니다.   

입출력 예 #3   

"1111111"이 "1"이 될 때까지 이진 변환을 가하는 과정은 다음과 같습니다.
회차	              | 이진 변환 이전	      | 제거할 0의 개수	      | 0 제거 후 길이	     | 이진 변환 결과
--------------------- | ---------------------| ---------------------| ---------------------| ---------------------
1	                  |	"1111111"	         | 0		            | 7	                   | "111"
2	                  |	"111"	             | 0	                | 3	                   | "11"
3	                  |	"11"	             | 0	                | 2	                   | "10"
4	                  |	"10"	             | 1	                | 1	                   | "1"

- 4번의 이진 변환을 하는 동안 1개의 0을 제거했으므로, [4,1]을 return 해야 합니다.


**풀이**
```python
def solution(s):
    temp_list=list(s)
    num,zero_sum,cnt=0,0,0
    answer = []

    for t in temp_list:
        if t=="1":
            num+=1
        else:
            zero_sum+=1
    
    cnt+=1
    print(cnt,zero_sum)
    while num > 1:
        temp=format(num,'b')
        num=0
        for n in temp:    
            if n=="1":
                num+=1
            else:
                zero_sum+=1
        cnt+=1
        print(cnt,zero_sum, num)
    answer.append(cnt)
    answer.append(zero_sum)
    return answer
```

**다른 풀이**
```python
def solution(s):
    a, b = 0, 0
    while s != '1':
        a += 1
        num = s.count('1')
        b += len(s) - num
        s = bin(num)[2:]
    return [a, b]
```
