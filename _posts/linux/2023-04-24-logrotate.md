---
layout: post
title: "[Linux] Logrotate 사용 방법" #게시물 이름
tags: [Linux, log, logrotate, nohup] #태그 설정
categories: Study #카테고리 설정
author: # 작성자
  - Byungineer
#toc : true #Table of Contents
---

kubernetes에서 추출한 webapp log를 logrotate를 활용해 분할 저장하는 방법을 알아보자.

```bash
kubectl logs -f $(kubectl get pods -l role=web -o jsonpath='{.items[0].metadata.name}')  >  $PWD/cdsw_web1.log
```   

## logrotate 사용

logrotate를 이용하면 일,주,월,년 단위로 파일을 `분할 저장` 할 수 있다. /var/log/아래를 보면, messages-2023#### 혹은 vmware-#####.1.log 와 같이 로그 정보가 분할되어 저장된 것을 볼 수 있다.   
날짜, 파일크기와 같은 방식으로 파일을 분할할 수 있으며, 파일 저장 이름 양식 또한 설정 가능하다.

### 1. logrotate config 파일 생성 

config 파일을 생성하기 앞서, 필자가 테스트한 환경(CentOS7)에서는 logrotate가 이미 설치되어 있었다.   
필요하다면, `yum install logrotate` or `dnf install logrotate`를 하자.   

```bash
$ cd [작업 디렉토리]
$ vi /etc/logrotate.d/test_logrotate ## 해당 경로에 config 파일을 생성하면 daily cron이 스크랩해서 자동 등록됩니다. 
/root/test/cdsw_web1.log {
    daily
    compress
    dateext
    rotate 5
    missingok
    notifempty
    size +4096k
    create 644 root root
    copytruncate
}
```

### logrotate 옵션들

설정    | 의미
--------------------- | ---------------------
daily / weekly / monthly / yearly |	rotate 주기
rotate 개수	|   순환되어 보관될 파일 개수
compress |	순환될 파일 압축(gzip) 
nocompress | 순환될 파일 압축하지 않음
compressext 확장자명 | 압축된 백업로그파일에 지정할 확장자 설정
compresscmd 압축명 | gzip이외의 압축파일 지정 
cpmpressoptions 옵션 | 압축프로그램에 대한 옵션 설정(-9: 압축률 최대)
dateext	| 로그파일에  YYYYMMDD형식의 확장자 추가
errors | 메일주소	에러발생시 지정된 메일주소로 메일 발송
extention 확장자명	| 순환된 로그파일의 확장자 지정
ifempty	| 로그파일이 비어있는 경우 순환(기본값)
notifempty |	로그파일이 비어있는 경우 순환하지 않는다.
mail 메일주소	| 순환 후 이전 로그파일을 지정된 메일주소로 발송
maxage	| count로 지정된 날수가 지난 백업파일 삭제
missingok	| 로그파일이 없을 경우에도 에러처리하지 않는다.
prerotate / endscript	| 순환작업 전에 실행할 작업 설정
postrotate / endscript	| 순환작업 후에 실행할 작업 설정
sharedscripts	| prerotate, postrotate 스크립트를 한번만 실행
size | 사이즈	순환결과 파일사이즈가 지정한 크기를 넘징낳도록 설정
copytruncate	| 현재 로그파일의 내용을 복사하여 원본로그 파일의 크기를 0으로 생성


### 2. Logrotate 적용

필요한 /root/test/cdsw_web1.log 라는 로그파일에 적용할 logrotate Config 파일을 생성한 후 아래의 명령어를 사용. /etc/logrotate.d/ 디렉토리 하위에 생성 시, 자동으로 등록 됩니다.   

```
logrotate /etc/logrotate.d/test_logrotate
```

### 3. logrotate 적용 확인

logrotate에 등록되어 있는 파일 확인.

```
cat /var/lib/logrotate.status
```


---
### reference

[https://m.blog.naver.com][naver.com]

[naver.com] : https://m.blog.naver.com/PostView.naver?isHttpsRedirect=true&blogId=sory1008&logNo=221124291927





