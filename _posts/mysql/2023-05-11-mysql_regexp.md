---
layout: post
title: "[mysql] MYSQL 정규표현식 이해 및 정리" #게시물 이름
tags: [mysql, SQL, regexp, 정규표현식] #태그 설정
categories: SQL #카테고리 설정
author: # 작성자
  - Byungineer
#toc : true #Table of Contents
---

## 정규표현식이란
_정규 표현식(正規表現式, 영어: regular expression, 간단히 regexp 또는 regex, rational expression) 또는 정규식(正規式)은 특정한 규칙을 가진 문자열의 집합을 표현하는 데 사용하는 형식 언어이다. 정규 표현식이라는 문구는 일치하는 텍스트가 준수해야 하는 "패턴"을 표현하기 위해 특정한 표준의 텍스트 신택스를 의미하기 위해 사용된다._   
<www.ko.wikipedia.org/wiki/정규_표현식>

### 정규표현식 패턴

**POSIX 기본 및 확장 표준 문법**

| 메타문자 | 기능 | 설명 |
| --- | --- | --- |
| . | 문자 | 1개의 문자와 일치한다. 단일행 모드에서는 새줄 문자를 제외한다. |
| [ ] | 문자 클래스 | "["과 "]" 사이의 문자 중 하나를 선택한다. "¦"를 여러 개 쓴 것과 같은 의미이다. 예를 들면 [abc]d는 ad, bd, cd를 뜻한다. 또한, "-" 기호와 함께 쓰면 범위를 지정할 수 있다. "[a-z]"는 a부터 z까지 중 하나, "[1-9]"는 1부터 9까지 중의 하나를 의미한다. |
| [^ ] | 부정 | 문자 클래스 안의 문자를 제외한 나머지를 선택한다. 예를 들면 [^abc]d는 ad, bd, cd는 포함하지 않고 ed, fd 등을 포함한다. [^a-z]는 알파벳 소문자로 시작하지 않는 모든 문자를 의미한다. |
| ^ | 처음 | 문자열이나 행의 처음을 의미한다. |
| $ | 끝 | 문자열이나 행의 끝을 의미한다. |
| ( ) | 하위식 | 여러 식을 하나로 묶을 수 있다. "abc¦adc"와 "a(b¦d)c"는 같은 의미를 가진다. |
| \n | 일치하는 n번째 패턴 | 일치하는 패턴들 중 n번째를 선택하며, 여기에서 n은 1에서 9 중 하나가 올 수 있다. |
| * | 0회 이상 | 0개 이상의 문자를 포함한다. "a*b"는 "b", "ab", "aab", "aaab"를 포함한다. |
| {m, n} | m회 이상 n회 이하 | "a{1,3}b"는 "ab", "aab", "aaab"를 포함하지만, "b"나 "aaaab"는 포함하지 않는다. |

**POSIX 확장 문법**

| 메타문자 | 기능 | 설명 |
| --- | --- | --- |
| ? | 0 또는 1회 | "a?b"는 "b", "ab"를 포함한다. |
| + | 1회 이상 | "a+b"는 "ab", "aab", "aaab"를 포함하지만 "b"는 포함하지 않는다. |
| ¦ | 선택 | 여러 식 중에서 하나를 선택한다. 예를 들어, "abc¦adc"는 abc와 adc 문자열을 모두 포함한다. |

**문자 클래스**

| POSIX | 비표준 | ASCII | 설명 |
| --- | --- | --- | --- |
| [:alnum:] |  | [A-Za-z0-9] | 영숫자 |
|  | [:word:] | [A-Za-z0-9_] | 영숫자 + "_" |
|  |  | [^A-Za-z0-9_] | 낱말이 아닌 문자 |
| [:alpha:] |  | [A-Za-z] | 알파벳 문자 |
| [:blank:] |  | [ \t] | 공백과 탭 |
|  |  | (?<=\W)(?=\w)|(?<=\w)(?=\W) | 낱말 경계 |
| [:cntrl:] |  | [\x00-\x1F\x7F] | 제어 문자 |
| [:digit:] |  | [0-9] | 숫자 |
|  |  | [^0-9] | 숫자가 아닌 문자 |
| [:graph:] |  | [\x21-\x7E] | 보이는 문자 |
| [:lower:] |  | [a-z] | 소문자 |
| [:print:] |  | [\x20-\x7E] | 보이는 문자 및 공백 문자 |
| [:punct:] |  | [][!"#$%&'()*+,./:;<=>?@\^_`{|}~-] | 구두점 |
| [:space:] |  | [ \t\r\n\v\f] | 공백 문자 |
|  |  | [^ \t\r\n\v\f] | 공백이 아닌 모든 문자 |
| [:upper:] |  | [A-Z] | 대문자 |
| [:xdigit:] |  | [A-Fa-f0-9] | 16진수 |

### MYSQL에서의 정규표현식 활용 예시

MYSQL 8버전 이상부터는 POSIX Extended Regular Expression(ERE)를 지원(사용)한다고 명시가 되어 있다.   

이해를 위해 MYSQL regexp 예시를 통해 활용 방법을 알아보자.
```SQL
# a로 시작하는 이름 조회
SELECT name FROM Example_table WHERE name LIKE 'a%'
SELECT name FROM Example_table WHERE name REGEXP('^a')

# 이름의 스펠링 중에 3번째에 a가 들어가는 이름 조회
SELECT name FROM Example_table WHERE name LIKE '___a____'
SELECT name FROM Example_table WHERE name REGEXP('...a....}')
SELECT name FROM Example_table WHERE name REGEXP('.{3}a{4}')

#글자수 제한을 두기 위해서는 끝에 $ 표시 exaple : 4번째에 "a"가 있고 8자리 name
SELECT name FROM Example_table WHERE name REGEXP('.{3}a{4}$')

# 숫자로만 이루어진 문자열 조회
SELECT name FROM Example_table WHERE name REGEXP('^[0-9]+$'); 
SELECT name FROM Example_table WHERE name REGEXP('^\d$');
SELECT name FROM Example_table WHERE name REGEXP('^[:digit:]$');

```

Mysql 뿐만 아니라 bash, Python, Java, 등등 다양한 프로그래밍 언어에서 다양하게 활용이 가능한 정규표현식... 알아두면 업무에 큰 도움이 될 것 같다.   

~~... 아니 꼭 알아야하는 기초적인 내용에 가까울 듯~~ 


---

### Reference

- [정규표현식 wikipedia][ref]
[ref]: https://ko.wikipedia.org/wiki/정규_표현식