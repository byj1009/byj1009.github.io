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

- Reference ID [ D3E9284E (send.mx.cdnetworks.com) ]
컴퓨터가 현재 동기화되어 있는 서버의 참조 ID 및 이름(or IP 주소).
127.127.1.1인 경우 컴퓨터가 외부 소스와 동기화되지 않고 "로컬" 모드가 작동 중임을 의미

- Stratum [ 3 ]
Stratum은 기준 시계가 연결된 컴퓨터에서 몇 단계 떨어져 있는지 나타냅니다.
-> 기준이 되는 절대적인 시계가 Stratum 1일 때, 2단계로 공용 NTP server가 설정된다. 따라서, 우리가 설정하는 Server는 3, 4층에서 시작하는 경우가 많다.

- Ref time [ Wed Jan 25 06:26:50 2023 ]
참조하는 NTP server(Reference server)로 부터 측정된 마지막 처리 시간(UTC)

- Systemtime [  0.000022406 seconds fast of NTP time ]
기준이 되는 NTP 서버의 시간 변동은 특정 응용 프로그램에 부정적인 결과를 초래할 수 있기 때문에 Chronyd는 시스템 시간을 변동하지 않는다. 대신 오류가 제거될 때까지 Systemtime의 속도를 약간 높이거나 느리게 한 다음 Systemtime이 정상 속도로 돌아가면 Systemtime의 모든 오류가 수정된다. 
결과적으로 시스템 클럭(gettime of day() 시스템 호출을 사용하는 다른 프로그램이나 셸의 date 명령으로 읽음)이 현재 실제 시간(서버 모드에서 작동할 때 NTP 클라이언트에 보고함)에 대한 크로니드의 추정치와 다를 기간이 있습니다. 이 라인에 보고된 값은 이 효과로 인한 차이입니다.

- Last offset [  +0.000028013 seconds ]
마지막 ntp time update 시 예상되는 Local time과의 offset

- RMS offset [ 0.000411049 seconds ]
Offset 값의 장기간 평균값.

- Frequency [ 27.216 ppm slow ]
"Frequency"는 Chronyd가 시간을 동기화하지 않는 동안 시간이 달라지는 비율을 말한다.

- Residual freq [ +0.002 ppm ]
기준이 되는 NTP 서버의 Frequency와 NTP 서버를 참조하는 서버의 Frequency간의 차이를 말한다. 

- Skew [ 0.071 ppm ]
Skew는 Frequency에 기반한 추정 오차

- Root delay [ 0.011276114 seconds ]
최종적으로 동기화되는 Stratum-1(폐쇠망에서는 Root NTP Server, 1계층이 아닐 수 있음) 시스템에 대한 네트워크 경로 지연의 합계.

- Root dispersion [ 0.017682148 seconds ]
최종적으로 동기화되는 Stratum-1(폐쇠망에서는 Root NTP Server, 1계층이 아닐 수 있음)과 동기화되는 모든 dispersion(분산)의 합이다. 
dispersion(분산)은 clock resolution, 통계적 측정 변화 등으로 인해 발생한다.

- clock resolution : 10시 20분 59초라는 시간을 표현할 때, 사실은 10시 20분 58.000009123초 일 수 있다. 시간의 단위 minutes, seconds, microseconds, nano... 와 같이 해상도(작은 단위까지 쪼개어 본다?)를 높일 수 있다.

- Leap status [ Normal ]
Normal, Insert second, Delete second or Not synchronized와 같은 NTP 설정 상태.


## chronyc Sources -v
<img src="/image/chrony3.png" alt="chrony3" style="height: 240x; width:320px;"/>
- Poll
소스가 폴링될 때, 초당 이진 로그 알고리즘의 간격으로 표시합니다. 따라서 값이 6이면 64초마다 측정이 수행되고 있음을 나타냅니다. chronyd는 일반적인 조건에 따라 폴링 속도를 자동으로 변경합니다.

<aside>
💡 폴링(polling)이란 하나의 장치(또는 프로그램)가 충돌 회피 또는 동기화 처리 등을 목적으로 다른 장치(또는 프로그램)의 상태를 주기적으로 검사하여 일정한 조건을 만족할 때 송수신 등의 자료처리를 하는 방식을 말한다. 이 방식은 버스, 멀티포인트 형태와 같이 여러 개의 장치가 동일 회선을 사용하는 상황에서 주로 사용된다. 서버의 제어 장치(또는 프로그램)는 순차적으로 각 단말 장치(또는 프로그램)에 회선을 사용하기 원하는지를 물어본다.
</aside> 

- Reach
8진수로 인쇄된 소스의 도달 레지스터. 레지스터에는 8비트가 있으며 소스로부터 수신되거나 누락된 모든 패킷에 대해 업데이트된다.
ex) 377 -> 1111 1111 (2)인데, 패킷전달 정상(1) 에러(0). >> 따라서 Reach 377 값은 최근 8번의 모든 전송에 대해 유효한 응답이 수신되었음을 나타낸다.

- LastRx
마지막 샘플이 원본에서 수신된 지 얼마나 오래되었는지 표시한다. default=seconds, m, h, dory는 분, 시간, 일 또는 년
10년 값은 이 소스에서 받은 샘플이 아직 없음을 나타낸다.

- Rast sample

## chronyc sourcestats
sourcestats 명령은 현재 크로니드에서 검사 중인 각 소스에 대한 drift rate 및 추정 프로세스에 대한 offset 정보를 표시
<img src="/image/chrony3.png" alt="chrony4" style="height: 240x; width:320px;"/>

- NP
서버에 대해 현재 보존 중인 샘플 포인트 수. 즉, 일정 주기로 NTP server로 부터 받아온 샘플(시간)의 갯수
drift rate 및 현재 시점의 offset은 NP 값을 통해 선형 회귀 분석을 수행하여 추정.

- NR
마지막 회귀 분석 후 부호가 같은 잔차의 런 수입니다. 이 숫자가 표본 수에 비해 너무 작아지기 시작하면 직선이 더 이상 데이터에 적합하지 않다는 것을 나타냅니다. 런 수가 너무 낮으면 chronyd는 오래된 표본을 폐기하고 런 수가 허용될 때까지 회귀 분석을 다시 실행합니다.

- Span
가장 오래된 샘플과 가장 최근 샘플 사이의 간격입니다. 
default : Seconds

- Freq Skew
이 값은 Freq에 대한 추정 오차 한계(백만 개당 부품 수)입니다.

---
### reference

[https://jfearn.fedorapeople.org](Fedorapeople.org)
[Fedorapeople.org]: https://jfearn.fedorapeople.org/fdocs/en-US/Fedora_Draft_Documentation/0.1/html/System_Administrators_Guide/sect-Checking_if_chrony_is_synchronized.html

[https://chrony.tuxfamily.org](chrony.tuxfamily.org)
[chrony.tuxfamily.org] : https://chrony.tuxfamily.org/doc/3.3/chronyc.html