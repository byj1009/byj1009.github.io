---
layout: post
title: "[Python] H-Index / [1차] 캐시" #게시물 이름
tags: [pyhton, programmers, Algorithm] #태그 설정
categories: Algorithm #카테고리 설정
author: # 작성자
  - Byungineer
#toc : true #Table of Contents
---

## H-Index
<https://school.programmers.co.kr/learn/courses/30/lessons/42747>

### 문제 설명
_H-Index는 과학자의 생산성과 영향력을 나타내는 지표입니다. 어느 과학자의 H-Index를 나타내는 값인 h를 구하려고 합니다. 위키백과1에 따르면, H-Index는 다음과 같이 구합니다.

어떤 과학자가 발표한 논문 n편 중, h번 이상 인용된 논문이 h편 이상이고 나머지 논문이 h번 이하 인용되었다면 h의 최댓값이 이 과학자의 H-Index입니다.

어떤 과학자가 발표한 논문의 인용 횟수를 담은 배열 citations가 매개변수로 주어질 때, 이 과학자의 H-Index를 return 하도록 solution 함수를 작성해주세요._

### 제한 조건
- 과학자가 발표한 논문의 수는 1편 이상 1,000편 이하입니다.
- 논문별 인용 횟수는 0회 이상 10,000회 이하입니다.

### 입출력 예

s                     | return
--------------------- | ---------------------
[3, 0, 6, 1, 5]       | 3

### 입출력 예 설명
이 과학자가 발표한 논문의 수는 5편이고, 그중 3편의 논문은 3회 이상 인용되었습니다. 그리고 나머지 2편의 논문은 3회 이하 인용되었기 때문에 이 과학자의 H-Index는 3입니다.

**풀이**
```python
def solution(citations):
    citations.sort(reverse=True)
    for c in range(len(citations)):
        if citations[c] <= c:
            answer = c
            break
        else:
            answer=len(citations)
    return answer
```

**다른 풀이**
```python
def solution(citations):
    citations.sort(reverse=True)
    answer = max(map(min, enumerate(citations, start=1)))
    return answer

def solution(citations):
    citations = sorted(citations)
    l = len(citations)
    for i in range(l):
        if citations[i] >= l-i:
            return l-i
    return 0
```

## [1차] 캐시
<https://school.programmers.co.kr/learn/courses/30/lessons/42747>

### 문제 설명
_지도개발팀에서 근무하는 제이지는 지도에서 도시 이름을 검색하면 해당 도시와 관련된 맛집 게시물들을 데이터베이스에서 읽어 보여주는 서비스를 개발하고 있다.
이 프로그램의 테스팅 업무를 담당하고 있는 어피치는 서비스를 오픈하기 전 각 로직에 대한 성능 측정을 수행하였는데, 제이지가 작성한 부분 중 데이터베이스에서 게시물을 가져오는 부분의 실행시간이 너무 오래 걸린다는 것을 알게 되었다.
어피치는 제이지에게 해당 로직을 개선하라고 닦달하기 시작하였고, 제이지는 DB 캐시를 적용하여 성능 개선을 시도하고 있지만 캐시 크기를 얼마로 해야 효율적인지 몰라 난감한 상황이다.

어피치에게 시달리는 제이지를 도와, DB 캐시를 적용할 때 캐시 크기에 따른 실행시간 측정 프로그램을 작성하시오._

### 입력 형식
- 캐시 크기(cacheSize)와 도시이름 배열(cities)을 입력받는다.
- cacheSize는 정수이며, 범위는 0 ≦ cacheSize ≦ 30 이다.
- cities는 도시 이름으로 이뤄진 문자열 배열로, 최대 도시 수는 100,000개이다.
- 각 도시 이름은 공백, 숫자, 특수문자 등이 없는 영문자로 구성되며, 대소문자 구분을 하지 않는다. 도시 이름은 최대 20자로 이루어져 있다.

### 출력 형식
- 입력된 도시이름 배열을 순서대로 처리할 때, "총 실행시간"을 출력한다.

### 조건
- 캐시 교체 알고리즘은 LRU(Least Recently Used)를 사용한다.
- cache hit일 경우 실행시간은 1이다.
- cache miss일 경우 실행시간은 5이다.

### 입출력 예

캐시크기(cacheSize)   | 도시이름(cities)       | 실행시간
--------------------- | --------------------- | ---------------------
3                     |["Jeju", "Pangyo", "Seoul", "NewYork", "LA", "Jeju", "Pangyo", "Seoul", "NewYork", "LA"] | 50
3                     |["Jeju", "Pangyo", "Seoul", "Jeju", "Pangyo", "Seoul", "Jeju", "Pangyo", "Seoul"] | 21
2                     |["Jeju", "Pangyo", "Seoul", "NewYork", "LA", "SanFrancisco", "Seoul", "Rome", "Paris", "Jeju", "NewYork", "Rome"] | 60
5                     |["Jeju", "Pangyo", "Seoul", "NewYork", "LA", "SanFrancisco", "Seoul", "Rome", "Paris", "Jeju", "NewYork", "Rome"] | 52
2                     |["Jeju", "Pangyo", "NewYork", "newyork"] | 16
0                     |["Jeju", "Pangyo", "Seoul", "NewYork", "LA"] | 25


**풀이**
```python
def solution(cacheSize, cities):
    answer = 0
    cache=[]
    if cacheSize == 0:
        return 5 * len(cities)
        
    for c in cities:
        c=c.lower()
        
        if len(cache) == 0:
            cache.append(c)
            answer += 5
            
        elif len(cache) == cacheSize:
            if c in cache:
                cache.remove(c)
                cache.append(c)
                answer += 1         
            else:
                cache.pop(0)
                cache.append(c)
                answer += 5   
                
        else:
            if c in cache:
                cache.remove(c)
                cache.append(c)
                answer += 1
            else:
                cache.append(c)
                answer += 5
    return answer
```

**다른 풀이**
```python
def solution(cacheSize, cities):
    import collections
    cache = collections.deque(maxlen=cacheSize)
    time = 0
    for i in cities:
        s = i.lower()
        if s in cache:
            cache.remove(s)
            cache.append(s)
            time += 1
        else:
            cache.append(s)
            time += 5
    return time
```
