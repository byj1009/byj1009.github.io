---
layout: post
title: "Chronyc 동기화 체크" #게시물 이름
tags: [Linux, Network, NTP, Chrony, 시간동기화] #태그 설정
categories: Study #카테고리 설정
author: # 작성자
  - Byungineer
#toc : true #Table of Contents
---

Compute Clustering을 위해 필수적인 시간 동기화를 위해 Chrony를 우리는 ntpd 혹은 chrony를 사용한다.

Chrony의 동기화 여부를 체크하기 위한 명령어를 알아보고, 각 필드에 대한 의미를 정리해본다.
```
chronyc tracking

chronyc sources

chronyc sourcestats
```

## chronyc tracing
<img src="/image/chrony1.png" alt="chrony1" style="height: 240x; width:320px;"/>
<img src="/image/chrony2.png" alt="chrony2" style="height: 240px; width:320px;"/>

### Reference ID [ D3E9284E (send.mx.cdnetworks.com) ]
컴퓨터가 현재 동기화되어 있는 서버의 참조 ID 및 이름(or IP 주소).
127.127.1.1인 경우 컴퓨터가 외부 소스와 동기화되지 않고 "로컬" 모드가 작동 중임을 의미

### Stratum [ 3 ]
Stratum은 기준 시계가 연결된 컴퓨터에서 몇 단계 떨어져 있는지 나타냅니다.
-> 기준이 되는 절대적인 시계가 Stratum 1일 때, 2단계로 공용 NTP server가 설정된다. 따라서, 우리가 설정하는 Server는 3, 4층에서 시작하는 경우가 많다.

### Ref time [ Wed Jan 25 06:26:50 2023 ]
참조하는 NTP server(Reference server)로 부터 측정된 마지막 처리 시간(UTC)

### Systemtime [  0.000022406 seconds fast of NTP time ]
기준이 되는 NTP 서버의 시간 변동은 특정 응용 프로그램에 부정적인 결과를 초래할 수 있기 때문에 Chronyd는 시스템 시간을 변동하지 않는다. 대신 오류가 제거될 때까지 Systemtime의 속도를 약간 높이거나 느리게 한 다음 Systemtime이 정상 속도로 돌아가면 Systemtime의 모든 오류가 수정된다. 
결과적으로 시스템 클럭(gettime of day() 시스템 호출을 사용하는 다른 프로그램이나 셸의 date 명령으로 읽음)이 현재 실제 시간(서버 모드에서 작동할 때 NTP 클라이언트에 보고함)에 대한 크로니드의 추정치와 다를 기간이 있습니다. 이 라인에 보고된 값은 이 효과로 인한 차이입니다.

### Last offset [  +0.000028013 seconds ]
마지막 ntp time update 시 예상되는 Local time과의 offset

### RMS offset [ 0.000411049 seconds ]
Offset 값의 장기간 평균값.

### Frequency [ 27.216 ppm slow ]
"Frequency"는 Chronyd가 시간을 동기화하지 않는 동안 시간이 달라지는 비율을 말한다.

### Residual freq [ +0.002 ppm ]
기준이 되는 NTP 서버의 Frequency와 NTP 서버를 참조하는 서버의 Frequency간의 차이를 말한다. 

### Skew [ 0.071 ppm ]
Skew는 Frequency에 기반한 추정 오차

### Root delay [ 0.011276114 seconds ]
최종적으로 동기화되는 Stratum-1(폐쇠망에서는 Root NTP Server, 1계층이 아닐 수 있음) 시스템에 대한 네트워크 경로 지연의 합계.

### Root dispersion [ 0.017682148 seconds ]
최종적으로 동기화되는 Stratum-1(폐쇠망에서는 Root NTP Server, 1계층이 아닐 수 있음)과 동기화되는 모든 dispersion(분산)의 합이다. 
dispersion(분산)은 clock resolution, 통계적 측정 변화 등으로 인해 발생한다.

clock resolution : 10시 20분 59초라는 시간을 표현할 때, 사실은 10시 20분 58.000009123초 일 수 있다. 시간의 단위 minutes, seconds, microseconds, nano... 와 같이 해상도(작은 단위까지 쪼개어 본다?)를 높일 수 있다.

### Leap status [ Normal ]
Normal, Insert second, Delete second or Not synchronized와 같은 NTP 설정 상태.



---
### reference

[https://jfearn.fedorapeople.org](Fedorapeople.org)
[Fedorapeople.org]: https://jfearn.fedorapeople.org/fdocs/en-US/Fedora_Draft_Documentation/0.1/html/System_Administrators_Guide/sect-Checking_if_chrony_is_synchronized.html


