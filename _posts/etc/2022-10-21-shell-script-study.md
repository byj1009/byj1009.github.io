---
layout: post
title: "[Linux] Bash Shell Scripts 작성에 사용한 문법 정리" #게시물 이름
tags: [bash, script, shell, linux, automation, cloudera, Cloudera Data Platform, CDP, Cloudera Manager, CM] #태그 설정
categories: Linux #카테고리 설정
author: # 작성자
  - Byungineer
#toc : true #Table of Contents
---

Cloudera Data Platform, Cloudera Manager를 설치하기 위해서 작성했던 스크립트의 주요 명령어를 정리해본다.

1_ set -e
Shell Scripts는 기본적으로, 에러가 발생하더라도 스크립트의 모든 내용이 실행되도록 되어 있다. 아래의 명령어를 스크립트의 문두에 작성해주면, 에러가 발생한 시점까지만 명령어가 실행된다.
```bash
set -e
```

2_ source [file]
source 명령어를 통해, 환경변수와 서버정보 파일을 불러올 수 있다.
source는 . 과 같고, 스크립트를 실행하는 명령어이다. 따라서, 설치에 필요한 명령어가 적힌 Shell Script와 호스트정보와 같이 변경이 필요한 텍스트, 스크립트 파일을 분리해서 관리하면 사용이 편하다.

```bash
source $PWD/server_info
```

3_ sed (streamlined editor)
파일을 수정하기 위해서는 sed 혹은 cat 명령어르 사용할 수 있다. 하지만, 특정 단어를 바꾸거나 그 다음에 내용을 추가하기 위해서는 sed 명령어를 사용하면 된다.

- sed -i "s/[바꾸고 싶은 부분]/[바꿀 부분]/g" [file 경로]
- sed -i "/[위치 검색]/a\[추가할 내용]" [file 경로]

```bash
#/etc/selinux/config 파일의 SELINUX=enforcing를 SELINUX=disabled로 변경 
echo $(sed -i "s/SELINUX=enforcing/SELINUX=disabled/g" /etc/selinux/config)
#/etc/chrony.conf 파일의 #local stratum 10의 아래에 local stratum 4 추가  
echo $(sed -i "/#local stratum 10/a\local stratum 4" /etc/chrony.conf)
```
sed 명령어 많은 옵션이 존재하며, 사용도가 다양하기 때문에 다른 포스팅에서 더 자세하게 다루도록 하겠다.

4_ IF문 File, Directory 검색
설치 자동화 스크립트를 작성할 때, 항상 문제(에러)가 되었던 건, 설치에 필요한 파일의 이름이 다르거나, 경로가 달라서 문제가 발생했다.
이러한 에러를 최대한 배제하기 위해서 if문을 사용한다.

```bash
# Directory가 해당 경로에 존재하는가.
if [ -d "[디렉토리 경로]" ]; then

# File이 해당 경로에 존재하는가.
if [ -f "[파일 경로]" ]; then

#cm이라는 이름이 들어간 디렉토리가 해당 경로에 존재하는가
if [ -d "$(find /var/www/html/ -name 'cm*')" ]; then
```

5_ basename
find 명령어를 통해서 원하는 파일의 경로를 찾았을 때, 상위 경로를 제외하기 위해서는 basename 명령어를 사용하면 된다.
dirname 명령어는 마지막 '/'를 이전의, 상위 경로를 출력합니다.

```bash
test_directory=/root/test_dir/123
exam_base_dir=$(basename ${test_directory})

#test_directory > /root/test_dir/123
#exam_base_dir=123
```

6_ cat
cat은 파일들을 인자로 받아서 해당 파일들을 연결해 표준출력으로 출력하는 명령어
cat command를 이용해 파일의 내용을 새로 작성하거나, 내용을 추가할 수 있다.

이때, cat <<_EOF_ 명령어를 사용하면, 다음 _EOF_ 나올 때 까지의 복수의 사용자 입력을 가져올 수 있다.

- cat <<_EOF_ >> [file name] : 내용 추가
- cat <<_EOF_ > [file name]: 내용 덮어 쓰기(파일 덮어쓰기)

추가적으로 EOF(End of File)로서, EOT(End of Text)로 사용도 하기도 하며, 그 어떤 문자를 사용해도 상관없다.
```bash
# 내용 추가하기
cat <<_EOF_ >> /root/.bashrc
export JAVA_HOME=/usr/java/jdk1.8.0_232-cloudera
export PATH=\$JAVA_HOME/bin:\$PATH
_EOF_

or
# 파일 생성 or 파일 덮어쓰기
cat <<_EOF_ > /root/test
echo "Hello world"
_EOF_
```
