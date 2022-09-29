---
layout: post
title: "Bash Shell Scripts 작성 팁 정리" #게시물 이름
tags: [bash, script, shell, linux, automation] #태그 설정
categories: Study #카테고리 설정
author: # 작성자
  - Byungineer
#toc : true #Table of Contents
---

빅데이터 플랫폼을 구축하며 데이터 파이프라인을 구성하기 위한 다수의 서버(VM) 세팅과정이 필요하다. Linux에서 이러한 작업을 자동화하기 위해 가장 기본이 되는 Shell Scripts를 작성할 때 유용한 정보들을 정리한 글이다. (사용자에 따라 Python 기반으로 작성이 가능한 Ansible을 이용한 자동화가 더 편리할지도...)


Bash Shell을 학습하며 도움이 되는 팁.

쉘 스크립팅은 Linux에서 배우고 수행 할 수있는 가장 쉬운 프로그래밍 형식입니다. 더구나, 작업 자동화, 새로운 간단한 유틸리티/도구 개발을위한 시스템 관리에 필요한 기술입니다.

이 기사에서는 효과적이고 신뢰할 수있는 bash 스크립트를 작성하기위한 10 가지 유용하고 실용적인 팁을 공유하며 다음과 같은 내용을 포함합니다.

1. 스크립트에서 항상 주석 사용
이것은 쉘 스크립팅뿐만 아니라 다른 모든 종류의 프로그래밍에 적용되는 권장 방법입니다. 스크립트에 주석을 작성하면 스크립트의 다른 부분이하는 일을 이해하는 데 도움이됩니다.

우선 주석은 \u003ccode\u003e # \u003c/ code\u003e 기호를 사용하여 정의됩니다.

#TecMint is the best site for all kind of Linux articles
2. 실패시 스크립트 종료
때때로 bash는 특정 명령이 실패하더라도 스크립트를 계속 실행하여 나머지 스크립트에 영향을 미칠 수 있습니다 (결국 논리적 오류가 발생할 수 있음). 명령이 실패 할 때 스크립트를 종료하려면 아래 줄을 사용하십시오.

#let script exit if a command fails
set -o errexit 
OR
set -e
3. Bash가 선언되지 않은 변수를 사용할 때 스크립트 종료
Bash는 논리적 오류를 일으킬 수있는 선언되지 않은 스크립트를 사용하려고 할 수도 있습니다. 따라서 다음 줄을 사용하여 bash가 선언되지 않은 변수를 사용하려고 할 때 스크립트를 종료하도록 지시합니다.

#let script exit if an unsed variable is used
set -o nounset
OR
set -u
4. 큰 따옴표를 사용하여 변수 참조
참조하는 동안 (변수 값 사용) 큰 따옴표를 사용하면 단어 분할 (공백 관련) 및 불필요한 글 로빙 (와일드 카드 인식 및 확장)을 방지하는 데 도움이됩니다.

아래 예를 확인하십시오.

#!/bin/bash
#let script exit if a command fails
set -o errexit 

#let script exit if an unsed variable is used
set -o nounset

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
파일을 저장하고 종료 한 후 다음과 같이 실행하십시오.

$ ./names.sh

5. 스크립트에서 함수 사용
아주 작은 스크립트 (몇 줄의 코드 포함)를 제외하고는 항상 함수를 사용하여 코드를 모듈화하고 스크립트를 더 읽기 쉽고 재사용 가능하게 만드는 것을 잊지 마십시오.

함수 작성 구문은 다음과 같습니다.

function check_root(){
	command1; 
	command2;
}

OR
check_root(){
	command1; 
	command2;
}
한 줄 코드의 경우 다음과 같이 각 명령 뒤에 종료 문자를 사용합니다.

check_root(){ command1; command2; }
6. 문자열 비교를 위해 \u003d\u003d 대신 \u003d 사용
\u003ccode\u003e \u003d\u003d \u003c/ code\u003e는 \u003ccode\u003e \u003d \u003c/ code\u003e의 동의어이므로 문자열 비교에 단일 \u003ccode\u003e \u003d \u003c/ code\u003e 만 사용합니다. 예를 들면 다음과 같습니다.

value1=”tecmint.com”
value2=”fossmint.com”
if [ "$value1" = "$value2" ]
7. 대체를 위해 레거시‘명령’대신 사용
명령 대체는 명령을 출력으로 대체합니다. 명령 대체를 위해 역 따옴표 \u003ccode\u003e \"command\"\u003c/ code\u003e 대신 \u003ccode\u003e \u0026 # 36 (command) \u003c/ code\u003e를 사용하세요.

이것은 shellcheck 도구에서도 권장됩니다 (셸 스크립트에 대한 경고 및 제안 표시). "예를 들면 :

user=`echo “$UID”`
user=$(echo “$UID”)
8. 읽기 전용을 사용하여 정적 변수 선언
정적 변수는 변경되지 않습니다. "스크립트에 정의 된 값은 변경할 수 없습니다.

readonly passwd_file=”/etc/passwd”
readonly group_file=”/etc/group”
9. ENVIRONMENT 변수에는 대문자 이름을 사용하고 맞춤 변수에는 소문자를 사용합니다.
모든 bash 환경 변수는 대문자로 이름이 지정되므로 변수 이름 충돌을 방지하기 위해 소문자를 사용하여 맞춤 변수 이름을 지정합니다.

#define custom variables using lowercase and use uppercase for env variables
nikto_file=”$HOME/Downloads/nikto-master/program/nikto.pl”
perl “$nikto_file” -h  “$1”
10. 긴 스크립트에 대해 항상 디버깅 수행
수천 줄의 코드로 bash 스크립트를 작성하는 경우 오류를 찾는 것이 악몽이 될 수 있습니다. 스크립트를 실행하기 전에 쉽게 문제를 해결하려면 몇 가지 디버깅을 수행하십시오. 아래 제공된 가이드를 읽고이 팁을 숙지하십시오.

How To Enable Shell Script Debugging Mode in Linux
How to Perform Syntax Checking Debugging Mode in Shell Scripts
How to Trace Execution of Commands in Shell Script with Shell Tracing
그게 다야! "공유 할 다른 최고의 bash 스크립팅 사례가 있습니까? 그렇다면 아래 의견 양식을 사용하십시오.








Shell Script에서 $0, $1, ...$N, $*, $@, $#은 특별한 의미를 갖는다. 이것들이 어떻게 사용되는지 간단한 예제를 통해 익힌다.

$0 : Script를 실행시킬 때 프로그램의 이름이 포함된 첫 번째 문자열이 저장된다.
$1, ...$N : argument들이 순서대로 저장된다. 위치 매개변수( Positional Parameter )라고 불리운다.
$* : 모든 위치 매개변수들로 구성된 단일 문자열
$@ : 자체로는 $*와 비슷하나 "$@"은 "$*"와  차이가 있다. "$@"은 "$1", ..."$N"과 같다.
$# : 위치 매개변수의 갯수가 저장된다.


실행 예
arg.sh
```
#!/bin/sh
echo '$0' $0
echo '$1' $1
echo '$2' $2
echo '$*' $*
echo '$@' $@
echo '$#' $#
echo '$?' $?
echo '$$' $$
```
[study@mail variables]$ ./arg.sh a b c d e
$0 ./arg.sh #프로그램의 이름이 포함된 첫 번째 문자열 저장
$1 a            # shell 뒤에 작성한 첫번째 argument 'a'
$2 b            # 2번째 argument
$* a b c d e    # 모든 argument으로 구성된 단일 문자열 'a b c d e'
$@ a b c d e    # $1, $2, $3, $4, ... 
$# 5            # Argument 갯수
$? 0
$$ 9566

[study@mail variables]$ ./arg.sh 'a b c' d e

$0 ./arg.sh

$1 a b c

$2 d

$* a b c d e

$@ a b c d e

$# 3

$? 0

$$ 9567

[study@mail variables]$ ./arg.sh "a b c" d e

$0 ./arg.sh

$1 a b c

$2 d

$* a b c d e

$@ a b c d e

$# 3

$? 0

$$ 9568

[study@mail variables]$ ./arg.sh "a b c"d e

$0 ./arg.sh

$1 a b cd

$2 e

$* a b cd e

$@ a b cd e

$# 2

$? 0

$$ 12974

arg2.sh

#!/bin/sh

echo '$0' $0

echo '$1' $1

echo '$2' $2

echo '$*' $*

echo '$@' $@

echo '$#' $#

echo '$?' $?

echo '$$' $$

for i in $*

  do echo item:$i

done


for i in $@

  do echo item:$i

done


[study@mail variables]$ ./arg2.sh "a b c" d e

$0 ./arg2.sh

$1 a b c

$2 d

$* a b c d e

$@ a b c d e

$# 3

$? 0

$$ 12980

item:a

item:b

item:c

item:d

item:e

item:a

item:b

item:c

item:d

item:e


arg3.sh

#!/bin/sh

echo '$0' $0

echo '$1' $1

echo '$2' $2

echo '$*' $*

echo '$@' $@

echo '$#' $#

echo '$?' $?

echo '$$' $$

for i in "$*"

  do echo item:$i

done

for i in "$@"

  do echo item:$i

done

[study@mail variables]$ ./arg3.sh "a b c" d e

$0 ./arg3.sh

$1 a b c

$2 d

$* a b c d e

$@ a b c d e

$# 3

$? 0

$$ 12982

item:a b c d e

item:a b c

item:d

item:e

"$@"와 같이 따옴표를 사용하면 따옴표로 값들이 묶여져 처리된다.




Reference
Linux에서 효과적인 Bash 스크립트를 작성하기위한 10 가지 유용한 팁
https://ko.linux-console.net/?p=2112#gsc.tab=0
Bash 입문자를 위한 핵심요약 정리(Shell Script)
https://blog.gaerae.com/2015/01/bash-hello-world.html

