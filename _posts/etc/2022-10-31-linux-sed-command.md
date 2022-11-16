---
layout: post
title: "Linux SED Command" #게시물 이름
tags: [bash, script, shell, linux, streamlined editor, sed] #태그 설정
categories: Study #카테고리 설정
author: # 작성자
  - Byungineer
#toc : true #Table of Contents
---

SED(Streamlined Editor)는 Unix에서 텍스트를 분해하거나 변환하기 위한 프로그램이다. sed는 벨 연구소의 리 E. 맥마흔이 1973년부터 1974년까지 개발하였고, 현재 유닉스 등의 여러 가지 운영 체제에서 사용 가능하다.

### SED 명령어의 특징
1. vim과 달리 명령어 형태로 파일을 편집하며, 실시간 편집이 아니다.

2. 원본을 건드리지 않고 편집하기 때문에 작업이 완료되었어도 기본적으로 원본에는 전혀 영향이 없다.
(단, -i 옵션을 지정하면 원본을 바꾸게 된다.)


그래서 내부적으로 특수한 저장 공간인 버퍼를 사용합니다. 두 가지 버퍼는 패턴 버퍼(패턴 스페이스라고도 합니다)와 홀드 버퍼(홀드 스페이스라고도 합니다)입니다.

<img src="/image/streamlined_editor.png" alt="test" style="height: 200px; width:240px;"/>

1) 라인을 읽어 Pattern Space에 넣는다.
2) Pattern Space의 sed 명령을 실행한다.
3) 수정된 내용을 출력한다.
4) Pattern Space의 버퍼된 내용을 삭제하고 과정을 반복한다.

2) 와 3)의 과정 사이에 내용의 변경을 위해서 Hold Space로 변경이 되는 내용을 임시 버퍼(Hold Space)에 저장.


```bash
sed 's/regexp/replacement/g' inputFileName > outputFileName

sed -i "s/SELINUX=enforcing/SELINUX=disabled/g" /etc/selinux/config
```

sed options
-n
-e
-f
--follow-symlinks
-i
-c
-b
-l N
--posix
-r
-s
-u
-z