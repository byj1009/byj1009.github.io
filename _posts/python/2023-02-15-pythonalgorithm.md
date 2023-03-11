---
layout: post
title: "[Python] 위장 / 튜플" #게시물 이름
tags: [pyhton, programmers, Algorithm] #태그 설정
categories: Algorithm #카테고리 설정
author: # 작성자
  - Byungineer
#toc : true #Table of Contents
---
{%raw%}
## 위장
<https://school.programmers.co.kr/learn/courses/30/lessons/42578>

### 문제 설명
_스파이들은 매일 다른 옷을 조합하여 입어 자신을 위장합니다.

예를 들어 스파이가 가진 옷이 아래와 같고 오늘 스파이가 동그란 안경, 긴 코트, 파란색 티셔츠를 입었다면 다음날은 청바지를 추가로 입거나 동그란 안경 대신 검정 선글라스를 착용하거나 해야 합니다.

종류   | 이름
----- | -----
얼굴  | 동그란 안경, 검정 선글라스
상의  | 파란색 티셔츠
하의  | 청바지
겉옷  | 긴 코트

스파이가 가진 의상들이 담긴 2차원 배열 clothes가 주어질 때 서로 다른 옷의 조합의 수를 return 하도록 solution 함수를 작성해주세요._

### 제한 조건
- clothes의 각 행은 [의상의 이름, 의상의 종류]로 이루어져 있습니다.
- 스파이가 가진 의상의 수는 1개 이상 30개 이하입니다.
- 같은 이름을 가진 의상은 존재하지 않습니다.
- clothes의 모든 원소는 문자열로 이루어져 있습니다.
- 모든 문자열의 길이는 1 이상 20 이하인 자연수이고 알파벳 소문자 또는 '_' 로만 이루어져 있습니다.
- 스파이는 하루에 최소 한 개의 의상은 입습니다.

### 입출력 예

clothes	              | return
--------------------- | ---------------------
[["yellow_hat", "headgear"], ["blue_sunglasses", "eyewear"], ["green_turban", "headgear"]] | 5
[["crow_mask", "face"], ["blue_sunglasses", "face"], ["smoky_makeup", "face"]] | 3

### 입출력 예 설명
예제 #1   
headgear에 해당하는 의상이 yellow_hat, green_turban이고 eyewear에 해당하는 의상이 blue_sunglasses이므로 아래와 같이 5개의 조합이 가능합니다.
1. yellow_hat
2. blue_sunglasses
3. green_turban
4. yellow_hat + blue_sunglasses
5. green_turban + blue_sunglasses

예제 #2   
face에 해당하는 의상이 crow_mask, blue_sunglasses, smoky_makeup이므로 아래와 같이 3개의 조합이 가능합니다.
1. crow_mask
2. blue_sunglasses
3. smoky_makeup

**풀이**
```python
def solution(clothes):
    answer = {}
    ans = 1
    
    for c in clothes:
        if c[1] in answer:
            answer[c[1]] += 1 #dictionary Item add
        else:
            answer[c[1]] = 1
            
    for v in answer.values():
        ans *= (v+1)
    return ans - 1
```

**다른 풀이**
```python
# 1.
def solution(clothes):
    from collections import Counter
    from functools import reduce
    cnt = Counter([kind for name, kind in clothes])
    answer = reduce(lambda x, y: x*(y+1), cnt.values(), 1) - 1
    return answer
# 2.
import collections
from functools import reduce

def solution(c):
    return reduce(lambda x,y:x*y,[a+1 for a in collections.Counter([x[1] for x in c]).values()])-1
```


💡 파이썬을 알고리즘을 풀다보면, collection, itertools, functools, etc... 코딩에 유용한 모듈을 활용하는 경우가 있다. 문제 풀이를 통해 내장 파이썬 모듈을 활용해보고, 외워두는 것도... 좋을 것 같다.

## 튜플
<https://school.programmers.co.kr/learn/courses/30/lessons/64065>

### 문제 설명
_셀수있는 수량의 순서있는 열거 또는 어떤 순서를 따르는 요소들의 모음을 튜플(tuple)이라고 합니다. n개의 요소를 가진 튜플을 n-튜플(n-tuple)이라고 하며, 다음과 같이 표현할 수 있습니다.

- (a1, a2, a3, ..., an)   
튜플은 다음과 같은 성질을 가지고 있습니다.

1. 중복된 원소가 있을 수 있습니다. ex : (2, 3, 1, 2)
2. 원소에 정해진 순서가 있으며, 원소의 순서가 다르면 서로 다른 튜플입니다. ex : (1, 2, 3) ≠ (1, 3, 2)
3. 튜플의 원소 개수는 유한합니다.

원소의 개수가 n개이고, 중복되는 원소가 없는 튜플 (a1, a2, a3, ..., an)이 주어질 때(단, a1, a2, ..., an은 자연수), 이는 다음과 같이 집합 기호 '{', '}'를 이용해 표현할 수 있습니다.
- {%raw%}{{a1}, {a1, a2}, {a1, a2, a3}, {a1, a2, a3, a4}, ... {a1, a2, a3, a4, ..., an}}

예를 들어 튜플이 (2, 1, 3, 4)인 경우 이는
- {{2}, {2, 1}, {2, 1, 3}, {2, 1, 3, 4}}   

와 같이 표현할 수 있습니다. 이때, 집합은 원소의 순서가 바뀌어도 상관없으므로

- {{2}, {2, 1}, {2, 1, 3}, {2, 1, 3, 4}}
- {{2, 1, 3, 4}, {2}, {2, 1, 3}, {2, 1}}
- {{1, 2, 3}, {2, 1}, {1, 2, 4, 3}, {2}}   
는 모두 같은 튜플 (2, 1, 3, 4)를 나타냅니다.

특정 튜플을 표현하는 집합이 담긴 문자열 s가 매개변수로 주어질 때, s가 표현하는 튜플을 배열에 담아 return 하도록 solution 함수를 완성해주세요._

### 제한 조건
- s의 길이는 5 이상 1,000,000 이하입니다.
- s는 숫자와 '{', '}', ',' 로만 이루어져 있습니다.
- 숫자가 0으로 시작하는 경우는 없습니다.
- s는 항상 중복되는 원소가 없는 튜플을 올바르게 표현하고 있습니다.
- s가 표현하는 튜플의 원소는 1 이상 100,000 이하인 자연수입니다.
- return 하는 배열의 길이가 1 이상 500 이하인 경우만 입력으로 주어집니다.

### 입출력 예

s | return
--------------------- | ---------------------
"{{2},{2,1},{2,1,3},{2,1,3,4}}" | [2, 1, 3, 4]
"{{1,2,3},{2,1},{1,2,4,3},{2}}" | [2, 1, 3, 4]
"{{20,111},{111}}" | [111, 20]
"{{123}}" | [123]
"{{4,2,3},{3},{2,3,4,1},{2,3}}" | [3, 2, 4, 1]

**풀이**
```python
def solution(s):
    answer = []
    ans_list=[]
    tmp_list=[]
    
    ans_word = s[1:len(s)-1]
    tmp_str=''
    for w in ans_word:
        if w.isdecimal():
            tmp_str = tmp_str + w
        else:
            if tmp_str == '' and tmp_list==[]:
                continue
                
            if w == ',' and tmp_list==[]:
                tmp_list.append(int(tmp_str))
                tmp_str = ''
                continue
            if w == ',' and tmp_list!=[]:        
                tmp_list.append(int(tmp_str))
                tmp_str = ''
            if w =='}':
                tmp_list.append(int(tmp_str))
                ans_list.append(tmp_list)
                tmp_list=[]
                tmp_str=''
    for i in tmp_str:
        ans_list.append(i.split(','))
    ans_list.sort(key = len)
    
    for a in ans_list:
        for ans_num in a:
            if ans_num not in answer:
                answer.append(ans_num)
    return answer
```

```python
# 이전 풀이
def solution(s): ###################### 이전 풀이
    answer = []
    #1.앞뒤 {, } 제거하기
    ans_word = s[1:len(s)-1]
    #2.{} 단위로 잘라서 리스트에 넣기. 10이상은 숫자 붙이기.
    tmp_list=[]
    ans_list=[]

    tmp_str=''
    for w in ans_word:
        if w.isdecimal():
            tmp_str = tmp_str + w
        else:
            if tmp_str == '' and tmp_list==[]:
                continue
                
            if w == ',' and tmp_list==[]:
                tmp_list.append(int(tmp_str))
                tmp_str = ''
                continue
            if w == ',' and tmp_list!=[]:        
                tmp_list.append(int(tmp_str))
                tmp_str = ''
            if w =='}':
                tmp_list.append(int(tmp_str))
                ans_list.append(tmp_list)
                tmp_list=[]
                tmp_str=''
    # 3. 원소 갯수로 오름차순 정렬
    ans_list_sorted=[]
    for num in range(len(ans_list)+1):
        for ans in ans_list:
            if len(ans)==num:
                ans_list_sorted.append(ans)
    # 4. ans_list_sorted에서 순서대로 뽑아서 중복안되는 숫자를 answer에 추가
    for ans in ans_list_sorted:
        for ans_num in ans:
            if ans_num not in answer:
                answer.append(ans_num)
    return answer
```

**다른 풀이**
```python
# 1.
import re
from collections import Counter

def solution(s):

    s = Counter(re.findall('\d+', s))
    return list(map(int, [k for k, v in sorted(s.items(), key=lambda x: x[1], reverse=True)]))

# 2. 
def solution(s):
    answer = []

    s1 = s.lstrip('{').rstrip('}').split('},{')

    new_s = []
    for i in s1:
        new_s.append(i.split(','))

    new_s.sort(key = len)

    for i in new_s:
        for j in range(len(i)):
            if int(i[j]) not in answer:
                answer.append(int(i[j]))

    return answer
```

