---
layout: post
title: "Bash Shell Scripts 작성 팁 정리" #게시물 이름
tags: [bash, script, shell, linux, automation] #태그 설정
categories: Study #카테고리 설정
author: # 작성자
  - Byungineer
#toc : true #Table of Contents
---
# 제목 없음

빅데이터 플랫폼을 구축하며 데이터 파이프라인을 구성하기 위한 다수의 서버(VM) 세팅과정이 필요로 했다. 플랫폼 구축을 하기 위한 사전 작업의 자동화를 계획하며 Bash Shell 공부를 시작하게 되었다. Linux에서 이러한 작업을 자동화하기 위해 가장 기본이 되는 Shell Scripts를 작성할 때 유용한 정보들을 내 입맛에 맞게 정리한 글이다.

Python 기반의 Ansible을 사용해 자동화가 가능한데, 이것은 나중에 포스팅하기로..

## Bash Shell 작성 팁.

1. 스크립트에서 항상 주석 사용

<aside>
💡 # 주석
#TecMint is the best site for all kind of Linux articles

</aside>

2. 에러 발생시 스크립트 종료
bash는 특정 명령이 실패하더라도 스크립트를 계속 실행한다.
명령이 실패 할 때 스크립트를 종료

```bash
#let script exit if a command fails
set -o errexit
OR
set -e
```
논리적 오류를 일으킬 수 있는 선언되지 않은 스크립트를 사용, bash가 선언되지 않은 변수를 사용하려고 할 때 스크립트를 종료
```bash
#let script exit if an unsed variable is used
set -o nounset
OR
set -u
```

3. 큰 따옴표를 사용하여 변수 참조
변수를 참조하는 동안 큰 따옴표( “ “ )를 사용하면 단어 분할 (공백 관련) 및 와일드 카드 인식 및 확장을 방지

```bash
#!/bin/bash
echo "Names without double quotes"
echo
names="Tecmint FOSSMint Linusay"
for name in $names; do
echo "$name"
done
echo

echo "Names with double quotes"
echo
for name in "$names"; do
echo "$name"
done

exit 0
```
<img src="/image/shell_image.png" alt="bash shell script" style="height: 100px; width:100px;"/>


<aside>
💡 기본적으로 shell script는 공백을 기준으로 해석을 함. 공백을 문자로 인식하기 위해서는 별도의 설정이 필요!
spacke=”space string” 에서 공백을 문자로 인식 시키기 위해서는 변수 호출시에 “” 를 사용하여야 한다.
if [ ${space} = "space string" ]; then        >>        if [ "${space}" = "space string" ]; then

</aside>

4. 함수 사용

코드를 모듈화하고 스크립트를 더 읽기 쉽고 재사용

```bash
function check_root(){
command1;
command2;
}

OR
check_root(){
command1;
command2;
}

OR
check_root(){ command1; command2; }
```

5. $() 사용
명령 대체는 명령을 출력으로 대체합니다. 명령 대체를 위해 역 따옴표(backtic, ` `) 대신 ,$() 사용

```bash
#둘다 같은 의미.
user=`echo “$UID”`
user=$(echo “$UID”)
```

6. 읽기 전용을 사용하여 정적 변수 선언

Readonly 옵션을  통해서 스크립트에서 변수 변경이 불가능 하도록(상수) 설정 가능

```bash
# passwd_file, group_file을 스크립트 중간에 수정하면 에러 발생
readonly passwd_file="/etc/passwd"
readonly group_file="/etc/group"
```

7. ENVIRONMENT 변수에는 대문자 이름을 사용하고 맞춤 변수에는 소문자를 사용합니다.

bash shell 에서의 변수는 대소문자가 구분이 된다. 충돌을 방지하기 위해서 상수는 대문자, 변수는 소문자로 작성.

```bash
# 정의 파일명은 상수이므로 대문자
CONFIGFILE="myapp.conf"

# 반복 카운터는 변수이므로 소문자
i=0

# 환경 변수는 대문자
JAVA_HOME="~~~"
MY_TMDIR="/var/tmp"
export MY_TMPDIR
```

8. 긴 스크립트에 대해 항상 디버깅 수행

---

Reference
Linux에서 효과적인 Bash 스크립트를 작성하기위한 10 가지 유용한 팁
[https://ko.linux-console.net/?p=2112#gsc.tab=0](https://ko.linux-console.net/?p=2112#gsc.tab=0)
[[ShellScript] 쉘 스크립트 사용법 (변수를 사용하는 법)](https://shlee1990.tistory.com/917)
[https://chanchan-father.tistory.com/802](https://chanchan-father.tistory.com/802)