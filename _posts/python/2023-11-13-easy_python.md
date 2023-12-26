---
layout: post
title: "[Python] kafka-python을 통한 실시간 kudu cdc" #게시물 이름
tags: [pyhton, Kafka, kudu, consumer, 카프카, CDC] #태그 설정
categories: python #카테고리 설정
author: # 작성자
  - Byungineer
#toc : true #Table of Contents
---

```python
abs(num) # 절댓값
pow(4, 2) # 4^2
max(5, 12) # 12
min(5, 12) # 5
round(3.14) # 3 default가 0

from math import *
floor(4.99) # 4 내림
ceil(3.14) # 4 올림
sqrt(16) # 4 제곱근
```


```python
passid = 990120-1234567
passid[:6] # 처음부터 5까지 6미포함
passid[7:] # 7부터 끝
passid[-7:] # 뒤에서 7번째부터 끝까지
```
```python
python = "Python is Amazing"
python.lower() # 소문자변환
python.upper() # 대문자 변환
python[0].isupper() # 0번째 문자 대문자 판별 > True/False
len(python) # 문자열 길이
python.replace("Python", "Java") # 문자 변환

python.index("n") # "n" 문자 위치 반환 ( 첫번째 )

python.index("n", index + 1) # "n"의 2번째 문자열 위치

python.find("Java") # 없으면 -1 반환
python.index("Java") # 없으면 에러
```

```python
print("나는 %d살입니다." % 20) # #decimal
print("나는 %s을 좋아해요." % "파이썬") # #string
print("Apple은 %c로 시작합니다." % "A") # #character

print("나는 %s색과 %s색을 좋아해요." % ("파란","빨간")))
```

```python
print("나는 {}살입니다.".format(20))
print("나는 {0}색과 {1}색을 좋아해요.".format("파란","빨간"))
print("나는 {color1}색과 {color2}색을 좋아해요.".format(color1="파란", color2="빨간"))
```

```python
color1="파란"
color2="빨간"
print(f"나는 {color1}색과 {color2}색을 좋아해요.") # python 3 이상에서만 가능 f-string
```

escape문자

```python
#\n #줄바꿈
#\", \' # 문장 내 따옴표 사용
# \\ 문장내 \ 사용
# \r 커서 맨 앞 이동
#example
print("Red Apple\rPine") #Pine Apple
# \b 백스페이스
print("Redd\bApple") # RedApple
# \t tab 
```

```python
"""http://naver.com 입력,
1. http:// 제외
2. . 이후 제외
3. 남은 글자 중 처음 세자리, 글재 갯수, 글자 내 'e' 갯수 + 1
"""
url = "http://naver.com"
passurl = url[7:].split(".")[0] 
# passurl = url.replace("http://", "")
# passurl = passurl[:passurl.index(".")] # index로 "."이 처음 나오는 위치까지 [] slicing
passwd = passurl[:3] + str(len(passurl)) + str(passurl.count("e")) + "!"
```

### list

```python
subway = ['a', 'c', 'd']
subway.index('c') # c의 위치, 1
subway.append('e') # 맨 뒤에 e 추가
subway.insert(1,'b') # 1번째 위치에 b 추가 [a,b,c,d,e]
subway.pop() # 맨 뒤에 제거
subway.count("a") # list내에 'a' 몇 개?

# 정렬
num_list = [5,2,4,3,1]
num_list.sort() # 오름차순 정렬
num_list.reverse() # 뒤집기

num_list.clear() # 리스트 요소 모두 제거

tmp_list = [7,7,7]
num_list.extend(tmp_list) # num_list 뒤로 tmp_list 요소 추가
```

### dictionary
```python
cabinet = {1: "a", 2: "b"} # key : value

print(cabinet[1]) # key 값이 없으면 에러가 밠애
print(cabinet.get(1)) # key 값이 없으면 None 출력

print(cabinet.get(3, "사용 가능")) # 3이라는 key 값으면 출력
print(1 in cabinet) # True
print(3 in cabinet) # False
# 추가
cabinet[3] = "c" # key, value가 있으면 update

# 삭제
del cabinet[3]
cabinet.clear() # 모든 key value 제거

print(cabinet.keys()) # key 출력
print(cabinet.values()) # value 출력
print(cabinet.items()) # key, value 쌍
```

### tuple
변경이 불가능하나 list보다 처리 속도가 빠름
```python
tmp_tuple = ("a", "b")
print(tmp_tuple[0], tmp_tuple[1])

#example
name, age, hobby = ("byun", 32, "coding")
print(name, age, hobby)
```

### set 집합
중복이 안되며, 순서가 없음

```python
tmp_set = {1,2,3,3,3} # {1,2,3}

# set, 집합 생성
java = {"a", "b", "c"}
python = set(["a", "d"])

#교집합
print(java & python) # a
print(javax.intersection(python))

# 합집합
print(java | python) # a, b, c, d
print(java.union(python))

# 차집합
print(java - python) # b, c
print(javax.difference(python))

# 추가
python.add("b")
# 제거
python.remove("d")
```

tmp_list = list(range(1,21))  # [1,2,3,4,5, ... ,19, 20]


### 한줄 for
```python
#example
num = [1,2,3,4,5]
num_100 = [n+100 for n in num]
```

### Function
```python
def function_name(전달자1,전달자2, ...):
   #...
  print("test")
  return 반환자1, 반환자2, ...

#example
def deposit(balance, money):
  print("입금완료. 잔액 {0}".format(balance + money))
  return balance + money
def withdraw(balance, money):
  if balance >= money:
    print("출금완료. 잔액 {0}".format(balance - money))
    return balance - money
  else:
    print("출금불가. 잔액 {0}".format(balance))
    return balance
def withdraw_night(balance, money):
  commission = 100 #수수료
  return commission, balance - money - commission # 튜플형식

balance = 0 # 잔액 초기화
balance = deposit(balance, 1000) # 입금
balance = deposit(balance, 500) # 출금
commission, balance = withdraw_night(balance, 500)
print("수수료 {0}, 잔액{1}".format(commission, balance))
```

### 기본값
함수에 전달자에 값을 넣지 않으면 default로 입력되는 값
```python
def profile(name, age=25, main_lang="python"):
  print("이름{0}, 나이{1}, 언어{2}".format(name,age,main_lang))

profile("tester") #이름tester, 나이25, 언어python
```

### 가변인자
```python
def profile(name, age, lang1, lang2, lang3)
    print("이름 : {0}\t 나이 : {1}\t".format(name, age), end=" ")
    print(lang1, lang2, lang3)

def profile(name, age, *language):
    print("이름 : {0}\t 나이 : {1}\t".format(name, age), end=" ") # end=" " 줄바꿈 안함
    for lang in language:
      print(lang, end=" ")
    print() #줄바꿈
```

### 전역, 지역변수
```python
# 전역변수 사용하면 코드 혼동오기 쉬움
num = 10

def checkpoint(tmp):
  global gun
  num = num - tmp
  print("num 값 : {0}".format(num))

print(num) # 10
checkpoint(2) # num 값 : 8
print(num) # 8
```

지역변수를 사용해 코딩
```python
num = 10

def checkpoint_ret(num, tmp):
  num = num - tmp
  print("num 값 : {0}".format(num))
  return num
print(num) # 10
gun = checkpoint_ret(num, 2)
print(num) # 8
```


### 퀴즈
```python
"""
표준 체중 구하는 프로그램 작성
남자 : 키(m) * 키 * 22
여자 : 키 * 키 * 21 

조건 1 : 함수 내 계산. std_weight(height,gender)
조건 2 : 표준 체중 소수점 둘째자리

ex) 키 175cm 남자의 표준 체중은 67.38kg 입니다.
"""

def std_weight(height, gender):
    if gender == "남자":
        return height * height * 22
   else: # 여자
        return  height * height * 21

height = 175
gender = "남자"
weight = round(std_weight(height / 100, gender),2) # cm > m / 반올림

print("키 {0}cm {1}의 표준 체중은 {2}}kg 입니다.".format(height, gender, weight))
```


### 표준입출력
```python

print("Python", "Java", sep=",", end="?") # sep 기본 공백, end 기본 줄바꿈>> 따라서 이 다음 출력이 같은 줄에 나오게 됨

import sys
print("Python", "Java", file=sys.stdout) # stdout으로 출력
print("Python", "Java", file=sys.stderr) # stderr로 출력


scores = {"수학":0, "영어":50, "코딩":100} # dict type
for subject, score in scores.items(): # items key,val 반환
    print(subject.ljust(4), str(score).rjust(4), sep=":")
    # ljust 왼쪽정렬 4만큼 공간 확보, rjust 오른쪽 정렬

for num in range(1, 21):
    print("대기번호 : " + str(num).zfill(3))
    # 대기번호 : 001
    # 대기번호 : 002 공백을 0으로 채움

```



### 다양한 출력
```python
print("{0: >10}".format(500)) #     500 //빈공간 5칸
print("{0: >+10}".format(500)) #    +500 //빈공간 4칸
print("{0: >+10}".format(-500)) #    -500 //빈공간 4칸

print("{0:_<10}".format(500)) #500_____ // _ 5개

print("{0:,}".format(1000000)) #1,000,000 //3자리마다 ,
print("{0:+,}".format(1000000)) #+1,000,000 //3자리마다 ,
print("{0:-,}".format(-1000000)) #-1,000,000 //3자리마다 ,

print("{0:^<+30,}".format(1000000000000)) #+1,000,000,000,000^^^^^^ //30자리수 까지 ^ 추가

print("{0:f}".format(5/3)) #1.666667 // 소수점 표시
print("{0:.2f}".format(5/3)) #1.67 // 소수점 표시, 3에서 반올림
```


### 파일쓰기
```python
score_file = open("score.txt", "w", encoding="utf8") #덮어쓰기
print("test1", file=score_file)
print("test2", file=score_file)
score_file.close()

score_file = open("score.txt", "a", encoding="utf8") # append
score_file.write("test3\n") # 줄바꿈이 안됨
score_file.write("test4")
score_file.close()
```

### 파일 읽기
```python
score_file = open("score.txt", "r", encoding="utf8")
print(score_file.read()) # 전체읽기
score_file.close()

score_file = open("score.txt", "r", encoding="utf8")
print(score_file.readline(), end="") # 한줄씩 읽기, 읽고 커서는 다음줄로
print(score_file.readline(), end="")
score_file.close()


score_file = open("score.txt", "r", encoding="utf8")
while True:
    line = score_file.readline()
    if not line:
        break
    print(line)
score_file.close()


score_file = open("score.txt", "r", encoding="utf8")
lines = score_file.readlines() # 리스트 형태로 lines에 저장
```


### pickle
python의 변수, 데이터를 파일 형태(pickle)로 저장하고, 불러오기 위한 라이브러리
```python
import pickle

profile_file = open("profile.pickle", "wb") #write, binary
profile = {"이름":"아무개", "나이":30, "취미":["축구","골프","바보"]}
pickle.dump(profile, profile_file) # file에 저장
profile_file.close()


profile_file = open("profile.pickle", "rb") #read, binary
profile = pickle.load(profile_file)
print(profile) #{"이름":"아무개", "나이":30, "취미":["축구","골프","바보"]}
profile_file.close()
```

### with

```python
# 별도로 close() 할 필요가 없음
with open("score.txt", "w", encoding="utf8") as score_file:
    score_file.write("test1")

with open("score.txt", "r", encoding="utf8") as score_file:
    print(score_file.read())
```


### Class
def 생성자
객체는 클래스로 부터 만들어지는 값이면서 클래스의 인스턴스라고 한다.

```python
class Unit:
    def __init__(self, name, hp, damage):
          self.name = name
          self.hp = hp
          self.damage = damage
          print("{0} 유닛이 생성 되었습니다.".format(self.name))
          print("체력 {0}, 공격력 {1}".format(self.hp, self.damage))          

marine1 = Unit("마린", 40, 5)
marine2 = Unit("마린", 40, 5)
```

### 멤버 변수

클래스 내에서 선언된 변수.

```python
class Unit:
    def __init__(self, name, hp, damage):
          self.name = name # 멤버 변수
          self.hp = hp # 멤버 변수
          self.damage = damage # 멤버 변수
          print("{0} 유닛이 생성 되었습니다.".format(self.name))
          print("체력 {0}, 공격력 {1}".format(self.hp, self.damage))          

wraith1 = Unit("레이스", 80, 5)
print("유닛 이름 : {0}, 공격력 : {1}".format(warith1.name, wraith1.damage)) # 멤버 변수를 외부에서 활용하는 예

# 마인드 컨트롤 한 경우
wraith2 = Unit("마컨된 레이스", 80, 5)
wraith2.clocking = True # Unit클래스 에는 없는 변수를 새로 생성 

if wraith2.clocking == True:
    print("{0} 는 현재 클로킹 상태입니다.".format(warith2.name))

#wraith1에는 clocking이라는 변수를 사용할 수 없다.
#if wraith1.clocking == True:
#    print("{0} 는 현재 클로킹 상태입니다.".format(warith2.name))
```

### 메소드
```python
#일반 유닛
class Unit:
    def __init__(self, name, hp, damage):
          self.name = name # 멤버 변수
          self.hp = hp # 멤버 변수
          self.damage = damage # 멤버 변수
          print("{0} 유닛이 생성 되었습니다.".format(self.name))
          print("체력 {0}, 공격력 {1}".format(self.hp, self.damage))          
# 공격유닛
class AttackUnit:
    def __init__(self, name, hp, damage):
        self.name = name
        self.hp = hp
        self.damage = damage
    
    def attack(self, location):
        print("{0} : {1} 방향으로 적군을 공격. [공격력 {2}]"\
        .format(self.name, location, self.damage)) ## attack 함수에 전달된 location 변수 활용, self가 붙은 변수는 클래스 내에 정해진 변수값 활용.
    
    def damaged(self, damage):
        print("{0} : {1} 데미지를 입었습니다.".format(self.name, damage))
        self.hp -= damage
        print("{0} : 현재 체력은 {1}.".format(self.name, self.hp))
        if self.hp <= 0:
            print("{0} : 파괴.".format(self.name))

firebat1 = AttackUnit("파이어뱃", 50, 16) #유닛 생성
firebat.attack("5시") # AttackUnit의 attack 메소드 활용
#2번 공격받음
firebat1.damaged(25)
firebat1.damaged(25)
```


### 상속
```python
#일반 유닛
class Unit:
    def __init__(self, name, hp, damage):
          self.name = name # 멤버 변수
          self.hp = hp # 멤버 변수
   
# 공격유닛
class AttackUnit:
    def __init__(self, name, hp, damage):
        self.name = name
        self.hp = hp
        self.damage = damage
    
    def attack(self, location):
        print("{0} : {1} 방향으로 적군을 공격. [공격력 {2}]"\
        .format(self.name, location, self.damage)) ## attack 함수에 전달된 location 변수 활용, self가 붙은 변수는 클래스 내에 정해진 변수값 활용.
    
    def damaged(self, damage):
        print("{0} : {1} 데미지를 입었습니다.".format(self.name, damage))
        self.hp -= damage
        print("{0} : 현재 체력은 {1}.".format(self.name, self.hp))
        if self.hp <= 0:
            print("{0} : 파괴.".format(self.name))

# 메딕같은 경우는 공격능력이 없음. 따라서 Unit 함수로 만들 수 있다.
# 그런데 Unit, AttackUnti 클래스는 중복되는 내용들이 있음. 이 경우에 상속의 개념을 사용할 수 있다.


class Unit: #부모 클래스
    def __init__(self, name, hp):
          self.name = name # 멤버 변수
          self.hp = hp # 멤버 변수
   
# 공격유닛
class AttackUnit(Unit): # 자식 클래스
    def __init__(self, name, hp, damage):
        #self.name = name
        #self.hp = hp
        Unit.__init__(self, name, hp) # Unit 클래스의 init 메소드를 호출해서 중복되는 name, hp 변수를 생성
        self.damage = damage
    
    def attack(self, location):
        print("{0} : {1} 방향으로 적군을 공격. [공격력 {2}]"\
        .format(self.name, location, self.damage)) ## attack 함수에 전달된 location 변수 활용, self가 붙은 변수는 클래스 내에 정해진 변수값 활용.
    
    def damaged(self, damage):
        print("{0} : {1} 데미지를 입었습니다.".format(self.name, damage))
        self.hp -= damage
        print("{0} : 현재 체력은 {1}.".format(self.name, self.hp))
        if self.hp <= 0:
            print("{0} : 파괴.".format(self.name))

```



### 다중상속
부모 클래스가 다수 인 경우를 말함.
```python
class Unit: #부모 클래스
    def __init__(self, name, hp):
          self.name = name # 멤버 변수
          self.hp = hp # 멤버 변수
   
# 공격유닛
class AttackUnit(Unit): # 자식 클래스
    def __init__(self, name, hp, damage):
        #self.name = name
        #self.hp = hp
        Unit.__init__(self, name, hp) # Unit 클래스의 init 메소드를 호출해서 중복되는 name, hp 변수를 생성
        self.damage = damage
    
    def attack(self, location):
        print("{0} : {1} 방향으로 적군을 공격. [공격력 {2}]"\
        .format(self.name, location, self.damage)) ## attack 함수에 전달된 location 변수 활용, self가 붙은 변수는 클래스 내에 정해진 변수값 활용.
    
    def damaged(self, damage):
        print("{0} : {1} 데미지를 입었습니다.".format(self.name, damage))
        self.hp -= damage
        print("{0} : 현재 체력은 {1}.".format(self.name, self.hp))
        if self.hp <= 0:
            print("{0} : 파괴.".format(self.name))

# 드랍쉽을 정의
def Flyable: # 공격 불가능 공중 유닛
    def __init__(self, flying_speed):
        self.flying_speed = flying_speed
    
    def fly(self, name, location):
        print("{0} : {1} 방향으로 날아감. [속도 {2}]".format(name, location, self,flying_speed))

def FlyableAttackUnit(AttackUnit, Flyable): # 공중 유닛이며 공격이 가능한 클래스
    def __init__(self, name, hp, damage, flying_speed):
        AttackUnit.__init__(self, name, hp, damage) # 초기화
        Flyable.__init__(self, flying_speed)

# 발키리 : 공중 공격 유닛, 한번에 14번 공격
valkyrie = FlyableAttackUnit("발키리", 200, 6, 5) #AttackUnit과, Unit클래스의 유닛 정의 하는 부분 // 유닛 생성
valkyrie.fly(valkyrie.name, "3시")# Flyable 클래스의 fly함수 호출 Flyable __init__을 보면 flying_speed만을 변수로 입력 받기 대문에 name을 명시하려면 별도로 변수를 추가해야함.
```

### 연산자 오버라이딩
자식 클래스에서 정의한 메소드 이용
```python
class Unit: #부모 클래스
    def __init__(self, name, hp, spped):
          self.name = name # 멤버 변수
          self.hp = hp # 멤버 변수
          self.spped = speed

    def move(self, location):
        print("[지상 유닛 이동]")
        print("{0} : {1} 방향으로 이동. [속도] {2}]".format(self.name, location, self.speed))
# 공격유닛
class AttackUnit(Unit): # 자식 클래스
    def __init__(self, name, hp, speed, damage):
        #self
        Unit.__init__(self, name, hp, speed) # Unit 클래스의 init 메소드를 호출해서 중복되는 name, hp 변수를 생성
        self.damage = damage
    
    def attack(self, location):
        print("{0} : {1} 방향으로 적군을 공격. [공격력 {2}]"\
        .format(self.name, location, self.damage)) ## attack 함수에 전달된 location 변수 활용, self가 붙은 변수는 클래스 내에 정해진 변수값 활용.
    
    def damaged(self, damage):
        print("{0} : {1} 데미지를 입었습니다.".format(self.name, damage))
        self.hp -= damage
        print("{0} : 현재 체력은 {1}.".format(self.name, self.hp))
        if self.hp <= 0:
            print("{0} : 파괴.".format(self.name))

# 드랍쉽을 정의
def Flyable: # 공격 불가능 공중 유닛
    def __init__(self, flying_speed):
        self.flying_speed = flying_speed
    
    def fly(self, name, location):
        print("{0} : {1} 방향으로 날아감. [속도 {2}]".format(name, location, self,flying_speed))

def FlyableAttackUnit(AttackUnit, Flyable): # 공중 유닛이며 공격이 가능한 클래스
    def __init__(self, name, hp, damage, flying_speed):
        AttackUnit.__init__(self, name, hp, 0, damage) # 지상 스피드는 0으로 하기 위해서 0 넣어둠
        Flyable.__init__(self, flying_speed)

vulture = AttackUnit("벌쳐", 80, 10, 20) # 이름, 체력, 속도, 공격력
battlecruiser = FlyableAttackUnit("배틀크루저", 500, 25 , 3)

vulture.move("11시")
battlecruiser.fly(battlecruiser.name, "9시")
# 위와 같은 경우 지상, 공중 유닛의 이동하는 메소드가 이름이 다르다 move != fly... 귀찮으니 수정이 필요.
```

수정된 내용...


```python
class Unit: #부모 클래스
    def __init__(self, name, hp, spped):
          self.name = name # 멤버 변수
          self.hp = hp # 멤버 변수
          self.spped = speed

    def move(self, location):
        print("[지상 유닛 이동]")
        print("{0} : {1} 방향으로 이동. [속도] {2}]".format(self.name, location, self.speed))
# 공격유닛
class AttackUnit(Unit): # 자식 클래스
    def __init__(self, name, hp, speed, damage):
        #self
        Unit.__init__(self, name, hp, speed) # Unit 클래스의 init 메소드를 호출해서 중복되는 name, hp 변수를 생성
        self.damage = damage
    
    def attack(self, location):
        print("{0} : {1} 방향으로 적군을 공격. [공격력 {2}]"\
        .format(self.name, location, self.damage)) ## attack 함수에 전달된 location 변수 활용, self가 붙은 변수는 클래스 내에 정해진 변수값 활용.
    
    def damaged(self, damage):
        print("{0} : {1} 데미지를 입었습니다.".format(self.name, damage))
        self.hp -= damage
        print("{0} : 현재 체력은 {1}.".format(self.name, self.hp))
        if self.hp <= 0:
            print("{0} : 파괴.".format(self.name))

# 드랍쉽을 정의
def Flyable: # 공격 불가능 공중 유닛
    def __init__(self, flying_speed):
        self.flying_speed = flying_speed
    
    def fly(self, name, location):
        print("{0} : {1} 방향으로 날아감. [속도 {2}]".format(name, location, self,flying_speed))

def FlyableAttackUnit(AttackUnit, Flyable): # 공중 유닛이며 공격이 가능한 클래스
    def __init__(self, name, hp, damage, flying_speed):
        AttackUnit.__init__(self, name, hp, 0, damage) # 지상 스피드는 0으로 하기 위해서 0 넣어둠
        Flyable.__init__(self, flying_speed)
    
    def move(self, location): ## move 함수를 재정의.
        print("[공중 유닛 이동]")
        self.fly(self.name, location)



vulture = AttackUnit("벌쳐", 80, 10, 20) # 이름, 체력, 속도, 공격력
battlecruiser = FlyableAttackUnit("배틀크루저", 500, 25 , 3)

vulture.move("11시")
battlecruiser.move("9시")
