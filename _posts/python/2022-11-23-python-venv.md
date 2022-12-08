---
layout: post
title: "Python 가상환경 구성" #게시물 이름
tags: [Data Engineering, Data Engineer, 데이터엔지니어, Big data, python, python3, Visual Studio, vscode, 가상환경, Venv, Virtual, study] #태그 설정
categories: python #카테고리 설정
author: # 작성자
  - Byungineer
#toc : true #Table of Contents
---


### Python venv가 무엇인가?
파이썬을 시작하기에 앞서 우리는 파이썬 가상환경을 생성해야 한다. 파이썬을 입문하기 위해서 관련서적을 살펴보면 빠지지 않고 나오는 내용이 Virtual Environment, 가상환경을 생성하는 것으로 시작한다. 

파이썬 가상환경은, 하나의 PC에서 프로젝트 별로 독립된 파이썬 실행 환경을 구성하기 위해서 사용한다. 즉, 파이썬 프로그래밍 환경이 A는 python2.6버전, B는 python3.7버전, C는 python3.7버전이지만 B와는 다른 Python Package를 사용할 때는 사용환경을 구별해주어야 관리가 쉽고, 버전 호완성으로 인한 에러를 피할 수 있다.

<aside>
Python2에서는 가상환경을 생성하기 위해서는 virtualenv라는 외부 패키지를 별도로 설치해야만 python 가상환경을 생성할 수 있었다. 하지만, python3에서는 venv라는 모듈이 내장이 되어 있기 때문에 별도의 설치없이 명령어를 통해 손쉽게 생겅 가능하다.
</aside>

### Visual Studio를 이용한 Python3 가상환경 생성
Visual Studio에서 CMD terminal을 열고 아래와 "python -m venv [가상환경 명]" 명령어로 생성.

```
PS C:\python_venv> python -m venv pythom3.10_venv
PS C:\python_venv> cd .\pythom3.10_venv\
PS C:\python_venv\pythom3.10_venv> dir


    디렉터리: C:\python_venv\pythom3.10_venv


Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
d-----      2022-11-23   오후 4:36                Include
d-----      2022-11-23   오후 4:36                Lib
d-----      2022-11-23   오후 4:36                Scripts
-a----      2022-11-23   오후 4:36             91 pyvenv.cfg
```

---
## Python 가상환경 활성화/비활성화 하기
### 1. CMD terminal 이용
생성한 Python 가상환경의 디렉토리(C:\python_venv\pythom3.10_venv)에 있는 Scripts로 이동.
```
    디렉터리: C:\python_venv\pythom3.10_venv\Scripts


Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
-a----      2022-11-23   오후 4:36           2092 activate
-a----      2022-11-23   오후 4:36           1021 activate.bat
-a----      2022-11-23   오후 4:36          19611 Activate.ps1
-a----      2022-11-23   오후 4:36            393 deactivate.bat
-a----      2022-11-23   오후 4:36         106360 pip.exe
-a----      2022-11-23   오후 4:36         106360 pip3.10.exe
-a----      2022-11-23   오후 4:36         106360 pip3.exe
-a----      2022-11-23   오후 4:36         242408 python.exe
-a----      2022-11-23   오후 4:36         232688 pythonw.exe
```
아래의 명령어로 활성화
```
source activate.bat
# or
.\activate.bat
```

비활성화
```
source deactivate.bat
# or
.\deactivate.bat
```

### 2. Visual studio 설정창 이용
Ctrl + Shift + p 를 입력하면 Visual Studio Code 상단에 설정창이 열린다. 해당 설정창에서 Python: Select Interpreter > 가상환경을 선택하면 활성화 된다.

<img src="/image/vscode_python.PNG" alt="python_venv" style="height: 200px; width:600px;"/>

위와 같이, 생성한 가상환경의 python.exe가 보이지 않는다면, 가상환경 경로의 python.exe를 찾아 등록하면 된다.




### 참고
파이썬 가상환경을 활성화하는 activate.bat 파일은 아래의 스크립트로 작성되어 있다.
또한, bat 확장자는 배치파일(batch file)로서 명령 인터프리터에 의해 실행되게끔 고안된 명령어들이 나열되어 있는 텍스트 파일이다. MS-DOS, OS/2, Windows에서 사용된다.
```
PS C:\python_venv\pythom3.10_venv\Scripts> cat activate.bat
@echo off

rem This file is UTF-8 encoded, so we need to update the current code page while executing it
for /f "tokens=2 delims=:." %%a in ('"%SystemRoot%\System32\chcp.com"') do (
    set _OLD_CODEPAGE=%%a
)
if defined _OLD_CODEPAGE (
    "%SystemRoot%\System32\chcp.com" 65001 > nul
)

set VIRTUAL_ENV=C:\python_venv\pythom3.10_venv

if not defined PROMPT set PROMPT=$P$G

if defined _OLD_VIRTUAL_PROMPT set PROMPT=%_OLD_VIRTUAL_PROMPT%
if defined _OLD_VIRTUAL_PYTHONHOME set PYTHONHOME=%_OLD_VIRTUAL_PYTHONHOME%

set _OLD_VIRTUAL_PROMPT=%PROMPT%
set PROMPT=(pythom3.10_venv) %PROMPT%

if defined PYTHONHOME set _OLD_VIRTUAL_PYTHONHOME=%PYTHONHOME%
set PYTHONHOME=

if defined _OLD_VIRTUAL_PATH set PATH=%_OLD_VIRTUAL_PATH%
if not defined _OLD_VIRTUAL_PATH set _OLD_VIRTUAL_PATH=%PATH%

set PATH=%VIRTUAL_ENV%\Scripts;%PATH%
set VIRTUAL_ENV_PROMPT=(pythom3.10_venv)

:END
if defined _OLD_CODEPAGE (
    "%SystemRoot%\System32\chcp.com" %_OLD_CODEPAGE% > nul
    set _OLD_CODEPAGE=
)
```