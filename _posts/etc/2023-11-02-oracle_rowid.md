---
layout: post
title: "[Oracle] Oracle Rowid 간단한 내용 정리" #게시물 이름
tags: [Database, DBMS, Oracle, Rowid, PSEUDOCOLUMN] #태그 설정
categories: Database #카테고리 설정
author: # 작성자
  - Byungineer
#toc : true #Table of Contents
---

Oracle to KUDU CDC를 구현하면서... Apache Kudu table에 반드시 필요한 PK로 사용하다가, 관련 에러가 발생해 Oracle rowid를 공부하고 내용을 정리해본다...

## Oracle Rowid

<img src="/image/postgresql_vacuum.png" alt="postgresql_vacuum" style="height:700; width:1100px;"/>

### Postgresql Vacuum이란?

ROWID 의사열
데이터베이스의 각 행에 대해 ROWID 의사열은 행의 주소를 반환합니다. Oracle 데이터베이스의 rowid 값에는 행을 찾는 데 필요한 정보가 포함되어 있습니다.

객체의 데이터 개체 번호
행이 위치한 데이터 파일의 데이터 블록
데이터 블록에서의 행 위치 (첫 번째 행은 0)
행이 위치한 데이터 파일 (첫 번째 파일은 1). 파일 번호는 테이블스페이스를 기준으로 상대적입니다.
일반적으로 rowid 값은 데이터베이스에서 행을 고유하게 식별합니다. 그러나 동일한 클러스터에 저장된 다른 테이블의 행은 동일한 rowid를 가질 수 있습니다.

ROWID 의사열의 값은 ROWID 또는 UROWID 데이터 형식을 가지고 있습니다. 자세한 내용은 "Rowid 데이터 형식" 및 "UROWID 데이터 형식"을 참조하십시오.

Rowid 값은 여러 중요한 용도가 있습니다:

단일 행에 가장 빠른 방법으로 액세스할 수 있습니다.
테이블의 행이 어떻게 저장되어 있는지 보여줄 수 있습니다.
테이블의 행에 대한 고유 식별자입니다.
ROWID를 테이블의 기본 키로 사용해서는 안 됩니다. 예를 들어 Import 및 Export 유틸리티를 사용하여 행을 삭제하고 다시 삽입하면 해당 행의 rowid가 변경될 수 있습니다. 행을 삭제하면 Oracle이 나중에 삽입된 새 행에 대해 해당 rowid를 다시 할당할 수 있습니다.

ROWID 의사열 값을 쿼리의 SELECT 및 WHERE 절에서 사용할 수는 있지만 이러한 의사열 값은 실제로 데이터베이스에 저장되지 않습니다. ROWID 의사열의 값을 삽입, 업데이트 또는 삭제할 수 없습니다.

1. <span style="color:red;">임계치 이상의 Dead Tuple을 정리, FSM 반환</span>
2. <span style="color:red;">Transaction ID Wraparound 방지</span>
3. 통계정보 갱신
4. visibility map을 갱신하여 index scan 성능 향상

### Dead Tuple

참고사항으로, Postgresql에서는 Record를 Tuple이라 표현한다. 또한, MVCC 동작 방식이 Oracle, MySQL과 달리 Tuple(Record)별로 적용된다.   

<img src="/image/postgresql_deadtuple.png" alt="postgresql_deadtuple" style="height:400; width:2485px;"/>

**Postgresql_FSM**
```Plain
PostgreSQL의 Free Space Map (FSM)은 데이터베이스에서 빈 데이터 페이지를 식별하고 추적하는 데 사용되는 내부 데이터 구조이다.

```

1. Tuple의 UPDATE문이 실행되면, UPDATE된 Tuple이 테이블에 추가(UPDATE전 원본, DELETE Tuple이 FSM에 기록)
2. Tuple이 새로이 추가(INSERT)될 때, FSM에서 빈공간을 찾아 기록된다.


###  Vacuum 과 Vacuum full의 차이




### Reference

- [테크블로그 – 우아한][woowa]
- [블로그 – DB 인사이드][ex-em]
- [티스토리 americanopeople][tstory]
- [Postgresql Documnet][postgresql]


[woowa]: https://techblog.woowahan.com/9478/
[ex-em]: https://blog.ex-em.com/1664
[tstory]: https://americanopeople.tistory.com/369
[postgresql]: https://www.postgresql.org/docs/current/sql-vacuum.html
