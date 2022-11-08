---
layout: post
title: "Apache Iceberg" #게시물 이름
tags: [Apache, Iceberg, apache iceberg, hive, impala, table, table format, 아이스버그] #태그 설정
categories: Study #카테고리 설정
author: # 작성자
  - Byungineer
#toc : true #Table of Contents
---


# Apache Iceberg

아파치 아이스버그는 거대한 분석 데이터 세트를 위한 개방형 테이블 형식이다. 아이스버그는 SQL 테이블처럼 작동하는 고성능 테이블 포맷을 사용하여 Spark, Trino, PrestoDB, Flink, Hive and Impala 를 포함한 컴퓨팅 엔진에 테이블을 추가합니다.

또한, 아파치 아이스버그는 단일 테이블에 수십 페타바이트의 데이터가 포함될 수 있는 프로덕션에서 사용되며 분산 SQL 엔진 없이도 이러한 거대한 테이블을 읽을 수 있습니다.

### 특징

- Schema evolution(Add, Drop, Rename, Update, Reorder)은 실수로 데이터를 삭제하는 것을 방지.
- Hidden Partitioning은 잘못된 결과나 매우 느린 쿼리를 유발하는 사용자 실수를 방지.
- Partition layout evolution 데이터 볼륨 또는 쿼리 패턴이 변경되면 테이블의 레이아웃을 업데이트.
- Time travel 정확히 동일한 테이블 스냅샷을 사용하는 재현 가능한 쿼리를 활성화하거나 사용자가 쉽게 변경 내용을 검토할 수 있도록 합니다.
- Version rollback을 사용하면 테이블을 양호한 상태로 재설정하여 문제를 신속하게 해결할 수 있습니다.

- 검색 계획이 빠름 – 테이블을 읽거나 파일을 찾는 데 분산 SQL 엔진이 필요하지 않음
- 고급 필터링 – 테이블 메타데이터를 사용하여 파티션 및 열 수준 통계를 사용하여 데이터 파일 삭제

아이스버그는 결국 일관된 클라우드 객체 저장소의 정확성 문제를 해결하기 위해 설계되었다.

- 모든 클라우드 스토어와 함께 작동하며 HDFS에 있을 때 목록 표시 및 이름 변경을 방지하여 NN 혼잡을 줄입니다.
- 직렬화 가능한 격리 – 테이블 변경은 원자적이며 독자는 부분적 또는 커밋되지 않은 변경 내용을 볼 수 없음
- Multiple concurrent writers가 낙관적인 동시성을 사용하며, 쓰기 충돌 시에도 호환되는 업데이트가 성공하도록 재시도합니다.

## 

<aside>
💡 Apache Iceberg는 중첩된 구조에서도 테이블 스키마를 Evolution(Add, Drop, Rename, Update, Reorder)시키거나 데이터 볼륨이 변경될 때 파티션 레이아웃을 변경할 수 있습니다. 빙산은 테이블 데이터를 다시 쓰거나 새 테이블로 마이그레이션하는 것과 같은 비용이 많이 드는 작업을 요구하지 않습니다.

예를 들어 하이브 테이블 파티셔닝은 변경할 수 없으므로 일별 파티션 레이아웃에서 시간별 파티션 레이아웃으로 이동하려면 새 테이블이 필요합니다. 쿼리는 파티션에 의존하므로 새 테이블에 대해 쿼리를 다시 작성해야 합니다. 경우에 따라 열 이름 변경과 같은 간단한 변경도 지원되지 않거나 데이터 정확성 문제가 발생할 수 있습니다.

</aside>

아이스버그 스키마 업데이트는 메타데이터 변경 사항이므로 업데이트를 수행하기 위해 데이터 파일을 다시 작성할 필요가 없습니다.

지도 키는 동일성을 변경하는 구조 필드를 추가하거나 삭제할 수 없습니다.

**아이스버그는 표의 각 열을 추적하기 위해 고유한 ID를 사용합니다. 열을 추가하면 새 ID가 할당되므로 기존 데이터가 실수로 사용되지 않습니다.**

### Hive table의 구조

아이스버그를 이해하기 위해 HIve table의 구조를 살펴보면 다음과 같다.

Hive table : Organize data in a Directory tree

Filter : WHERE date = ‘20180513’ AND hour = 19

<img src="/image/hive_table_archi.png" alt="hive_table_architecture" style="height: 200px; width:240px;"/>

이러한 구조의 문제는 크기가 큰 테이블의 경우에 너무 큰 디렉토리 구조를 가지게 된다는 것이다. 이러한 문제를 해결하기 위해서 Hive Metastore를 사용하여 Partition정보를 추적한다.

date=20180513/hour=19 → hdfs:/…/date=20180513/hour=19 (HDFS 파일 시스템 경로)

즉, 테이블의 상태 정보(메타데이터)는 Hive Metastore 와 파일시스템 두 곳에 저장이 된다.

이러한 Hive table의 이점은 Hive,Spark, Presto, Flink, Pig와 같은 엔진에서 사용 가능하며, Hudi, NiFi, Flume, Sqoop과 같은 툴 사용 가능.

### 아이스버그 구조

아이스버그의 가장 큰 특징은, 시간의 변화에 따른 테이블 내의 모든 파일들의 변화를 추적 할 수 있는 것이다. 아이스버그에서는 Hbase와 같이 Snapshot을 활용해 테이블의 파일 정보를 기록한다. 각 Write, Commit 작업이 수행될 때 새로운 Snapshot이 생성된다.

<img src="/image/iceberg_snapshot1.png" alt="test" style="height: 200px; width:240px;"/>

아이스버그의 테이블 정보를 읽을 때는, 가장 최신의 Snapshot 정보를 활용해 Read작업을 수행하며, Write작업이 발생하면 새로운 Snapshot이 생성된다. 이러한 작업은 동시에 수행이 가능하다.


<img src="/image/iceberg_snapshot2.png" alt="test" style="height: 200px; width:240px;"/>


Iceberg 설정 정보