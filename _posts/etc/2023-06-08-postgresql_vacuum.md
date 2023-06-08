---
layout: post
title: "[Database] Postgrsql vacuum이란" #게시물 이름
tags: [Database, DBMS, MVCC, PostgreSQL, Vacuum] #태그 설정
categories: Database #카테고리 설정
author: # 작성자
  - Byungineer
#toc : true #Table of Contents
---

지난 MVCC 포스팅 참고...   
<https://byj1009.github.io/database/2023/06/01/MVCC.html>


## Postgresql Vacuum

<img src="/image/postgresql_vacuum.png" alt="postgresql_vacuum" style="height:700; width:1100px;"/>

### Postgresql Vacuum이란?

Postgresql Vacuum : PostgreSQL에서 실행되는 백그라운드 프로세스 또는 명령어.   
공식문서의 Synopsis를 살펴보면 다음과 같다.   

```
VACUUM [ ( option [, ...] ) ] [ table_and_columns [, ...] ]
VACUUM [ FULL ] [ FREEZE ] [ VERBOSE ] [ ANALYZE ] [ table_and_columns [, ...] ]

where option can be one of:

    FULL [ boolean ]
    FREEZE [ boolean ]
    VERBOSE [ boolean ]
    ANALYZE [ boolean ]
    DISABLE_PAGE_SKIPPING [ boolean ]
    SKIP_LOCKED [ boolean ]
    INDEX_CLEANUP { AUTO | ON | OFF }
    PROCESS_TOAST [ boolean ]
    TRUNCATE [ boolean ]
    PARALLEL integer

and table_and_columns is:

    table_name [ ( column_name [, ...] ) ]
```

위와 같은 vacuum 명령어를 통해 크게 4가지의 작업(기능)을 수행할 수 있다.

1. <span style="color:red;">임계치 이상의 Dead Tuple을 정리, FSM 반환</span>
2. <span style="color:red;">Transaction ID Wraparound 방지</span>
3. 통계정보 갱신
4. visibility map을 갱신하여 index scan 성능 향상

### Dead Tuple

참고사항으로, Postgresql에서는 Record를 Tuple이라 표현한다. 또한, MVCC 동작 방식이 Oracle, MySQL과 달리 Tuple(Record)별로 적용된다.   

<img src="/image/postgresql_deadtuple.png" alt="postgresql_deadtuple" style="height:400; width:2485px;"/>

**Postgresql_FSM**
```Plain
PostgreSQL의 Free Space Map (FSM)은 데이터베이스에서 빈 데이터 페이지를 식별하고 추적하는 데 사용되는 내부 데이터 구조입니다. 데이터베이스에서는 데이터를 페이지 단위로 저장하고 관리합니다. FSM은 이러한 페이지에서 빈 공간을 식별하여 새로운 데이터를 삽입할 때 사용 가능한 공간을 찾는 데 도움을 줍니다.

FSM은 두 가지 주요 구성 요소로 구성됩니다.

Free Space Map (FSM): FSM은 데이터 페이지에서 사용 가능한 빈 공간을 추적하는 비트맵 구조입니다. 각 비트는 페이지 내의 고유한 블록을 나타내며, 비트 값이 0이면 해당 블록에는 사용 가능한 공간이 있음을 나타내고, 1이면 해당 블록은 사용 중인 것을 의미합니다.

Visibility Map (VM): VM은 FSM의 성능을 향상시키기 위한 보조 맵입니다. VM은 페이지의 일부인 블록이 최근에 변경되었는지 여부를 추적합니다. 변경된 블록은 VM의 해당 비트를 설정하고, 변경되지 않은 블록은 비트를 비활성화합니다. 이를 통해 데이터를 읽을 때 FSM을 검사하는 데 필요한 I/O 작업을 줄일 수 있습니다.
```

1. Tuple의 UPDATE문이 실행되면, UPDATE된 Tuple이 테이블에 추가(UPDATE전 원본, DELETE Tuple이 FSM에 기록)
2. Tuple이 새로이 추가(INSERT)될 때, FSM에서 빈공간을 찾아 기록된다.

위 상황에서, UPDATE, DELETE되어 빈공간이 생겼을 경우, 이 것을 Dead Tuple이라 한다.   
(=UPDATE Transaction 완료되고, 원본 Tuple이 어디에도 참조되지 않는 Tuple이 될 때를 의미)   
-> Disk, Memory상에서의 데이터 구조를 생각하면, Transaction이 다수 발생하는 환경에서 Dead Tuple이 어떤 영향을 미치는지 상상해보면, Dead Tuple관리(vacuum작업)이 중요한 이유를 알 수 있다.   
-> JAVA Garbage Collection과 유사한 작업

###  Vacuum 과 Vacuum full의 차이

- Vacuum(autovacuum) 
  - FSM에 Dead Tuple 영역 반환 
  - OS DISK 자체 공간 반환 X 
  - 즉, Table의 사이즈는 감소하지 않을 수 있다. 
  - vacuum 작업 중, DML 사용 가능

- Vacuum full
  - FSM에 Dead Tuple 반환
  - OS DISK 공간 반환
  - 제거된 Dead Tuple 만큼 Table의 크기 감소
  - Access Exclusive Lock, DML & SELECT 모두 사용 불가능

<img src="/image/postgresql_vacuumfull.png" alt="postgresql_deadtuple" style="height:480; width:590;"/>

### Transaction ID Wraparound

PostgreSQL의 Transaction ID Wraparound은 데이터베이스에서 사용되는 트랜잭션 ID(XID)가 한계에 도달할 때 발생하는 문제이다. PostgreSQL은 32비트로 구성된 트랜잭션 ID를 사용하며, 이는 4,294,967,295개(Unsigned INT)의 고유한 트랜잭션 ID 값을 표현할 수 있다. 하지만 데이터베이스가 긴 시간 동안 활발하게 운영되고 많은 트랜잭션이 발생하는 경우, 트랜잭션 ID가 한계에 도달 가능성이 있고, 한계치를 넘어서면 기존의 데이터가 미래의 데이터(쓰레기 데이터)라고 인식을 하는 상황이 발생한다.

Transaction ID Wraparound가 발생할 때의 문제 상황 2가지   
- 가장 오래된 활성 트랜잭션 ID가 한계에 근접할 때: 데이터베이스에서 가장 오래된 활성 트랜잭션 ID가 한계에 가까워지면, 이 트랜잭션 ID보다 오래된 모든 트랜잭션은 더 이상 확인할 수 없게 됩니다. 이는 데이터 무결성 문제를 발생시킬 수 있습니다.
- VACUUM 프로세스의 부재 또는 지연: VACUUM 프로세스는 사용하지 않는 데이터를 정리하고 트랜잭션 ID를 재사용합니다. 하지만 VACUUM 프로세스가 충분히 실행되지 않거나 지연되는 경우, 트랜잭션 ID가 고갈되는 문제가 발생할 수 있습니다.


<img src="/image/postgresql_wraparound.png" alt="postgresql_wraparound" style="height:700; width:880;"/>


Postgresql에서는 이러한 Transaction ID Wraparound를 방지하기 위해 AGE(Current XID - 생성 시점 XID), Frozen XID(XID =2인 예약된 값)에 의해 관리 된다.   
- Transaction ID Wraparound의 방지를 위해 vacuum_freeze_min_age(default 5천만)을 넘을 때, Anti Wraparound Vacuum이 수행
- Tuple, Table이 각각의 Age를 가지고 있으며, Table은 가장 큰 Tuple의 Age를 의미하므로, Anti Wraparound Vacuum 대상 여부 판단 가능

### 통계 정보 갱신 & VM 정보 갱신

- PostgreSQL 통계 정보 갱신
  - Query Optimizing, 각 테이블에 저장된 자료를 바탕으로 수집된 통계 정보를 이용
  - 통계 정보 갱신 작업이 제대로 되지 않으면 의도 되지 않은 쿼리 실행 계획이 짜여짐
  - 전체적인 데이터베이스 성능을 떨어뜨림

- 인덱스 전용 검색 성능 향상하는데 이용하는 실자료 지도(visibility map, vm) 정보를 갱신
  - 지도 정보는 인덱스 전용 쿼리들에 대해서 빠른 응답을 제공
  - 인덱스 전용 검색인 경우는 테이블 페이지를 검색하지 않고, 우선적으로 vm에서 해당 자료검색
  - Vaccum 작업은 이미 지도 정리 작업이 끝난 것에 대해서는 더 이상 그 작업을 하지 않는다.




### Reference

- [테크블로그 – 우아한][woowa]
- [블로그 – DB 인사이드][ex-em]
- [티스토리 americanopeople][tstory]
- [Postgresql Documnet][postgresql]


[woowa]: https://techblog.woowahan.com/9478/
[ex-em]: https://blog.ex-em.com/1664
[tstory]: https://americanopeople.tistory.com/369
[postgresql]: https://www.postgresql.org/docs/current/sql-vacuum.html
