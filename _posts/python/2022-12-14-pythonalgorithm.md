---
layout: post
title: "[Python] Lv2 최댓값과 최솟값" #게시물 이름
tags: [pyhton, programmers, Algorithm] #태그 설정
categories: Algorithm #카테고리 설정
author: # 작성자
  - Byungineer
toc : true #Table of Contents
comments : true
---

<https://school.programmers.co.kr/learn/courses/30/lessons/12939>

### 문제 설명
_문자열 s에는 공백으로 구분된 숫자들이 저장되어 있습니다. str에 나타나는 숫자 중 최소값과 최대값을 찾아 이를 "(최소값) (최대값)"형태의 문자열을 반환하는 함수, solution을 완성하세요.
예를들어 s가 "1 2 3 4"라면 "1 4"를 리턴하고, "-1 -2 -3 -4"라면 "-4 -1"을 리턴하면 됩니다._

### 제한 조건
- s에는 둘 이상의 정수가 공백으로 구분되어 있습니다.

### 입출력 예
s | return
--------------------- | ---------------------
"1 2 3 4" |	"1 4"
"-1 -2 -3 -4" |	"-4 -1"
"-1 -1" |	"-1 -1"



**풀이**
```python
def solution(s):
    answer = ''
    ans_list=[]
    temp_list=[]

    ans_list=s.split(" ")

    for num in ans_list:
        temp_list.append(int(num))     

    answer = (str(min(temp_list)) + " " + str(max(temp_list))) 
    return answer
```

**다른 풀이**
```python
def solution(s):
    ans = list(map(int, s.split()))
    return f'{min(ans)} {max(ans)}' # 포맷팅 이용
```


<aside>
💡 f-string을 사용하면 쉽게 출력 문자열을 포맷팅할 수 있다. Python3.6 버전부터 사용이 가능하며 %, format 함수를 쓰는 것 보다 익혀두면 편리하기 때문에 공부해두자.
</aside>