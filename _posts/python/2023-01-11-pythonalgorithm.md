---
layout: post
title: "[Python] 짝지어 제거하기 / 영어 끝말잇기" #게시물 이름
tags: [pyhton, programmers, Algorithm] #태그 설정
categories: Algorithm #카테고리 설정
author: # 작성자
  - Byungineer
#toc : true #Table of Contents
---

## 짝지어 제거하기
<https://school.programmers.co.kr/learn/courses/30/lessons/12973>

### 문제 설명
_짝지어 제거하기는, 알파벳 소문자로 이루어진 문자열을 가지고 시작합니다. 먼저 문자열에서 같은 알파벳이 2개 붙어 있는 짝을 찾습니다. 그다음, 그 둘을 제거한 뒤, 앞뒤로 문자열을 이어 붙입니다. 이 과정을 반복해서 문자열을 모두 제거한다면 짝지어 제거하기가 종료됩니다. 문자열 S가 주어졌을 때, 짝지어 제거하기를 성공적으로 수행할 수 있는지 반환하는 함수를 완성해 주세요. 성공적으로 수행할 수 있으면 1을, 아닐 경우 0을 리턴해주면 됩니다.

예를 들어, 문자열 S = baabaa 라면   
`b aa baa → bb aa → aa →`   
의 순서로 문자열을 모두 제거할 수 있으므로 1을 반환합니다._

### 제한 조건
- 문자열의 길이 : 1,000,000이하의 자연수
- 문자열은 모두 소문자로 이루어져 있습니다.

### 입출력 예

s                     | return
--------------------- | ---------------------
baabaa                | 1
cdcd                  | 0

### 입출력 예 설명

입출력 예 #2   
문자열이 남아있지만 짝지어 제거할 수 있는 문자열이 더 이상 존재하지 않기 때문에 0을 반환합니다.

**풀이**
```python
def solution(s):
    temp_list=[]
    for i in s:
        if temp_list==[]:
            temp_list.append(i)
        elif temp_list[-1]==i:
            temp_list.pop()#remove last element
        else:
            temp_list.append(i)
    
    if temp_list==[]:
        return 1
    else:
        return 0


### 예전에 풀어둔 풀이 1
def solution(s):
    num=0
    while num < len(s) -1 :
        if s[num]==s[num+1]:
            s = s[0:num] + s[num+2:]
            num=max(0,num-1)
        else:
            num+=1
    if len(s) == 0:
        return 1
    else:
        return 0
### 예전에 풀어둔 풀이 2            
def solution(s):
    stack = []
    for i in s:
        if len(stack) ==0:
            stack.append(i)
        elif stack[-1] == i:
            stack.pop()
        else:
            stack.append(i)
    if len(stack) ==0:
        return 1
    else:
        return 0
```

**다른 풀이**
```python
def solution(s):
    
    s1=[]
    s1.append(s[0]) # 미리 0번째 문자열을 넣어둔다
    
    for i in range(1, len(s)):   
        if len(s1) > 0 and s1[-1]==s[i]: # len(s1)을 해주지 않으면 error남/ 왜냐 요소 하나라도 들어있어야 비교가 되니까
            s1.pop(-1)
              
        else:
            s1.append(s[i])
    
    if len(s1) == 0: # 최종적으로 리스트가 비었다면 1
        return 1
    else:
        return 0
```


💡 알아두면 좋은 것
- list.remove(”특정 element”)
- list.pop(”리스트의 index” or “공백시 마지막 요소제거”)
- list.del(”리스트 index”) or del list >> 리스트 삭제



## 영어 끝말잇기
<https://school.programmers.co.kr/learn/courses/30/lessons/12981>

### 문제 설명
_1부터 n까지 번호가 붙어있는 n명의 사람이 영어 끝말잇기를 하고 있습니다. 영어 끝말잇기는 다음과 같은 규칙으로 진행됩니다.

1. 1번부터 번호 순서대로 한 사람씩 차례대로 단어를 말합니다.
2. 마지막 사람이 단어를 말한 다음에는 다시 1번부터 시작합니다.
3. 앞사람이 말한 단어의 마지막 문자로 시작하는 단어를 말해야 합니다.
4. 이전에 등장했던 단어는 사용할 수 없습니다.
5. 한 글자인 단어는 인정되지 않습니다.   
다음은 3명이 끝말잇기를 하는 상황을 나타냅니다.

`tank → kick → know → wheel → land → dream → mother → robot → tank`   

위 끝말잇기는 다음과 같이 진행됩니다.

- 1번 사람이 자신의 첫 번째 차례에 tank를 말합니다.
- 2번 사람이 자신의 첫 번째 차례에 kick을 말합니다.
- 3번 사람이 자신의 첫 번째 차례에 know를 말합니다.
- 1번 사람이 자신의 두 번째 차례에 wheel을 말합니다.
- (계속 진행)

끝말잇기를 계속 진행해 나가다 보면, 3번 사람이 자신의 세 번째 차례에 말한 tank 라는 단어는 이전에 등장했던 단어이므로 탈락하게 됩니다.

사람의 수 n과 사람들이 순서대로 말한 단어 words 가 매개변수로 주어질 때, 가장 먼저 탈락하는 사람의 번호와 그 사람이 자신의 몇 번째 차례에 탈락하는지를 구해서 return 하도록 solution 함수를 완성해주세요._

### 제한 조건
- 끝말잇기에 참여하는 사람의 수 n은 2 이상 10 이하의 자연수입니다.
- words는 끝말잇기에 사용한 단어들이 순서대로 들어있는 배열이며, 길이는 n 이상 100 이하입니다.
- 단어의 길이는 2 이상 50 이하입니다.
- 모든 단어는 알파벳 소문자로만 이루어져 있습니다.
- 끝말잇기에 사용되는 단어의 뜻(의미)은 신경 쓰지 않으셔도 됩니다.
- 정답은 [ 번호, 차례 ] 형태로 return 해주세요.
- 만약 주어진 단어들로 탈락자가 생기지 않는다면, [0, 0]을 return 해주세요.


### 입출력 예

n                     | words                 |	result
--------------------- | --------------------- | --------------------- 
3                     |	["tank", "kick", "know", "wheel", "land", "dream", "mother", "robot", "tank"] | [3,3]
5                     |	["hello", "observe", "effect", "take", "either", "recognize", "encourage", "ensure", "establish", "hang", "gather", "refer", "reference", "estimate", "executive"] | [0,0]
2                     |	["hello", "one", "even", "never", "now", "world", "draw"] | [1,3]


### 입출력 예 설명

입출력 예 #1
3명의 사람이 끝말잇기에 참여하고 있습니다.
- 1번 사람 : tank, wheel, mother
- 2번 사람 : kick, land, robot
- 3번 사람 : know, dream, tank   
와 같은 순서로 말을 하게 되며, 3번 사람이 자신의 세 번째 차례에 말한 tank라는 단어가 1번 사람이 자신의 첫 번째 차례에 말한 tank와 같으므로 3번 사람이 자신의 세 번째 차례로 말을 할 때 처음 탈락자가 나오게 됩니다.

입출력 예 #2
5명의 사람이 끝말잇기에 참여하고 있습니다.   
- 1번 사람 : hello, recognize, gather
- 2번 사람 : observe, encourage, refer
- 3번 사람 : effect, ensure, reference
- 4번 사람 : take, establish, estimate
- 5번 사람 : either, hang, executive   
와 같은 순서로 말을 하게 되며, 이 경우는 주어진 단어로만으로는 탈락자가 발생하지 않습니다. 따라서 [0, 0]을 return하면 됩니다.

입출력 예 #3
2명의 사람이 끝말잇기에 참여하고 있습니다.
- 1번 사람 : hello, even, now, draw
- 2번 사람 : one, never, world   
와 같은 순서로 말을 하게 되며, 1번 사람이 자신의 세 번째 차례에 'r'로 시작하는 단어 대신, n으로 시작하는 now를 말했기 때문에 이때 처음 탈락자가 나오게 됩니다.

**풀이**
```python
def solution(n, words): 
    # n 사람 수 # words 리스트를 n의 갯수 만큼 반복검사
    answer = [0,0]
    words_check=[]    

    words_check.append(words[0])

    for w in range(1, len(words)):

        if words[w] in words_check: # 중복 검사
            answer[0]=w%n+1 # 사람
            answer[1]=w//n+1 # 틀린 회차
            break
    
        if words[w-1][-1]!=words[w][0]: # 끝말잇기 검사.
            print("error",w)
            answer[0]=w%n+1
            answer[1]=w//n+1
            break
            
        words_check.append(words[w])                
    return answer
```

**다른 풀이**
```python
def solution(n, words):
    for p in range(1, len(words)):
        if words[p][0] != words[p-1][-1] or words[p] in words[:p]: return [(p%n)+1, (p//n)+1]
    else:
        return [0,0]
```


💡 같은 파이썬 코드이지만, or를 통해 간결하게 표현한 것을 볼 수 있다. 깔끔하게 코딩하자...
