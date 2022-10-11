---
layout: post
title: "Bash Shell Scripts 명령어 결과 변수 저장" #게시물 이름
tags: [bash, script, shell, linux, automation] #태그 설정
categories: Study #카테고리 설정
author: # 작성자
  - Byungineer
#toc : true #Table of Contents
---

Bash shell Sciprt를 작성하며 Command 결과를 변수에 저장해야 하는 경우가 있다.

```bash
command1=`whoami`
echo $command1

command2=$(whoami)
echo $command2

```
command1 과 command2의 결과는 모두 같다.
-> `` (backtic)과 $()는 같다.

```bash
command3= $(ls -al)
echo $command3
echo "$command3"
```
결과를 원본 그대로(여러줄로 표시)하려면 ""(큰따옴표)를 사용.

### 명령어가 변수에 저장될 때는, 실행이 된다!
다음의 예를 통해서 위의 말이 무슨 말인지 쉽게 이해 가능하다.
```bash
command4=$(cat <<_EOT_ >> /etc/hosts
0.0.0.0 testserver
_EOT_
)
```
cat 명령어를 사용해 /etc/hosts 파일에 "0.0.0.0 testserver" 문장을 넣는 명령어의 결과를 저장하는 예시이다. 이러한 명령어를 결과를 변수에 저장하기 이전에, /etc/hosts 파일에 해당 문장을 넣는 명령어가 수행된 이후이며, 그 결과가 저장이 된다.

즉, echo $(command4)를 통해서 그 결과를 출력하는 것이며, 변수를 저장하는 과정에 명령어가 실행이 된 이후인 것.


### ${}와 $()의 차이
$(command) is “command substitution”
${parameter} is “parameter substitution”
