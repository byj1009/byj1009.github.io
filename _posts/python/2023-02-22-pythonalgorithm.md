---
layout: post
title: "[Python] 귤 고르기 / n^2 배열 자르기" #게시물 이름
tags: [pyhton, programmers, Algorithm] #태그 설정
categories: python #카테고리 설정
author: # 작성자
  - Byungineer
#toc : true #Table of Contents
---

## 귤 고르기
<https://school.programmers.co.kr/learn/courses/30/lessons/138476>

### 문제 설명
_경화는 과수원에서 귤을 수확했습니다. 경화는 수확한 귤 중 'k'개를 골라 상자 하나에 담아 판매하려고 합니다. 그런데 수확한 귤의 크기가 일정하지 않아 보기에 좋지 않다고 생각한 경화는 귤을 크기별로 분류했을 때 서로 다른 종류의 수를 최소화하고 싶습니다.

예를 들어, 경화가 수확한 귤 8개의 크기가 [1, 3, 2, 5, 4, 5, 2, 3] 이라고 합시다. 경화가 귤 6개를 판매하고 싶다면, 크기가 1, 4인 귤을 제외한 여섯 개의 귤을 상자에 담으면, 귤의 크기의 종류가 2, 3, 5로 총 3가지가 되며 이때가 서로 다른 종류가 최소일 때입니다.

경화가 한 상자에 담으려는 귤의 개수 k와 귤의 크기를 담은 배열 tangerine이 매개변수로 주어집니다. 경화가 귤 k개를 고를 때 크기가 서로 다른 종류의 수의 최솟값을 return 하도록 solution 함수를 작성해주세요._

### 제한 조건
- 1 ≤ k ≤ tangerine의 길이 ≤ 100,000
- 1 ≤ tangerine의 원소 ≤ 10,000,000

### 입출력 예

k | tangerine | result
--------------------- | ---------------------  | ---------------------
6 | [1, 3, 2, 5, 4, 5, 2, 3] | 3
4 | [1, 3, 2, 5, 4, 5, 2, 3] | 2
2 | [1, 1, 1, 1, 2, 2, 2, 3] | 1


**풀이**
```python
def solution(k, tangerine):
    answer = 0
    count=0
    
    tan_dict={}
    for t in tangerine:
        if t in tan_dict:
            tan_dict[t]+=1
        else:
            tan_dict[t]=1
    tan_dict = dict(sorted(tan_dict.items(), key=lambda x: x[1], reverse=True))
    # value : 종류별 갯수
    for value in tan_dict.values():
        answer += 1
        count+=value
        if count >= k:
            break
    return answer
```

Time out이 발생했던 다른 풀이

```python
def solution(k, tangerine):
    answer = 0
    count=0
    # tangerine list to dict type
    t_dict = {t:tangerine.count(t) for t in tangerine}
    t_dict = dict(sorted(t_dict.items(), key=lambda item: item[1], reverse=True))
    # value : 종류별 갯수
    for value in t_dict.values():
        answer += 1
        count+=value
        if count >= k:
            break
    return answer
```


**다른 풀이**
```python
from collections import Counter

def solution(k, tangerine):
    counter = Counter(tangerine)
    tangerine.sort(key = lambda t: (-counter[t], t))
    return len(set(tangerine[:k]))

```

💡 count 말고, counter를 활용하면 좀 더 효율적인 계산이 가능한가봄.
- 💡이번 문제에서 알아두면 좋을 내용
    - count 라는 함수를 사용하면, 리스트에 있는 요소의 갯수를 활용할 수 있다. 하지만, 작업이 무거워지는 만큼 효율성에서 떨어질 수 있기 때문에… 잘 확인하고 쓰자.
    - dictionary = [”key”: value]
        - items() : key, value 출력
        - keys() : key
        - values() : value

## n^2 배열 자르기
<https://school.programmers.co.kr/learn/courses/30/lessons/87390>

### 문제 설명
_정수 n, left, right가 주어집니다. 다음 과정을 거쳐서 1차원 배열을 만들고자 합니다.

1. n행 n열 크기의 비어있는 2차원 배열을 만듭니다.
2. i = 1, 2, 3, ..., n에 대해서, 다음 과정을 반복합니다.
  - 1행 1열부터 i행 i열까지의 영역 내의 모든 빈 칸을 숫자 i로 채웁니다.
3. 1행, 2행, ..., n행을 잘라내어 모두 이어붙인 새로운 1차원 배열을 만듭니다.
4. 새로운 1차원 배열을 arr이라 할 때, arr[left], arr[left+1], ..., arr[right]만 남기고 나머지는 지웁니다.

정수 n, left, right가 매개변수로 주어집니다. 주어진 과정대로 만들어진 1차원 배열을 return 하도록 solution 함수를 완성해주세요._

### 제한 조건
- 1 ≤ n ≤ 107
- 0 ≤ left ≤ right < n2
- right - left < 105

### 입출력 예

n | left | right | result
------ | ------ | ------ | ------
3 | 2 | 5 | [3,2,2,3]
4 | 7 | 14 | [4,3,3,3,4,4,4,4]

### 입출력 예 설명

입출력 예 #1   
다음 애니메이션은 주어진 과정대로 1차원 배열을 만드는 과정을 나타낸 것입니다.   
<img src="/image/FlattenedFills_ex1.gif" alt="test" style="height: 100px; width:100px;"/>

입출력 예 #2   
다음 애니메이션은 주어진 과정대로 1차원 배열을 만드는 과정을 나타낸 것입니다.   
<img src="/image/FlattenedFills_ex2.gif" alt="test" style="height: 100px; width:100px;"/>


**풀이**
```python
def solution(n, left, right):
    answer = []
    for i in range(left,right+1):
        x = i//n 
        y = i%n
        if x > y: 
            answer.append(x+1)
        else:
            answer.append(y+1)
    return answer
```

💡 파이썬 알고리즘 문제에서 마주치는 어려움 중 하나 인 것 같다. 기능 구현보다는, 문제의 규칙성을 찾아 코드로 변환하는 것. 코딩테스트를 준비한다면 다양한 케이스를 접하고, 조금의 암기는 필요할 것 같다.