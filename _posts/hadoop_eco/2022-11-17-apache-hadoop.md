---
layout: post
title: "Apache Hadoop 개념 정리" #게시물 이름
tags: [Apache, Hadoop, HDFS, 하둡, Cloudera, study] #태그 설정
categories: Study #카테고리 설정
author: # 작성자
  - Byungineer
toc : true #Table of Contents
---

Cloudera Data Platform을 다루며, Hadoop Ecosystem의 모체가 되는 Hadoop의 구조, 특징 및 기능에 대해 개념을 확실하게 가져가기 위해 내용 정리를 해본다.

## Hadoop 버전별 특징
Apache Hadoop은 현재 Ver3로, 2011년에 Hadoop(ver1)이 정식 발표된 이후로 구조적, 기능적인 발전이 있었다. 핵심적인 버전별 특징에 대해 정리하며 Hadoop의 특징을 간략하게 살펴보자.

- Hadoop v1 : 
  - 분산저장(HDFS) : 네임노드(Namenode) + 데이터노드(Datanode)
  - 병렬처리(MapReduece) : 잡트래커(Job Tracker) + 태스크트래커(Task Tracker)
    - 잡트래커 : 병렬처리 중인 작업의 진행 관리, 자원 관리
    - 태스크트래커 : 실제 작업을 수행(map & reduce), 작업의 단위는 슬롯(slot)이며 Map과 Reduce 슬롯의 개수는 정해져 있다. 즉, 맵의 작업이 다 끝나도 리듀스의 슬롯의 갯수가 늘어나지는 않는다.

<img src="/image/hadoopv1.png" alt="hadoopv1" style="height: 300px; width:700px;"/>

- Hadoop v2(2012) : 잡트래커(Job Tracker)의 병목현상 제거를 위해 얀(YARN) 도입 
  - YARN
    - 클러스터 관리
      - 리소스매니저 : 애플리케이션의 요청에 따른 리소스 할당 [스케쥴러 + 애플리케이션 매니저 + 리소스 트래커]
      - 노드매니저 : 컨테이너의 실행, 컨테이너 리소스 사용량 모니터링, 리소스매니저에 정보 report [애플리케이션 마스터 + 컨테이너]
    - 작업관리
      - 애플리케이션 마스터 : 작업당 하나씩 생성되며, 컨테이너를 사용해 작업 모니터링과 실행을 관리
      - 컨테이너 : 작업(Task)처리의 단위. 리소스 매니저가 할다한 시스템의 자원 활용
  <aside>
  + YARN은 2006년 야후에서 개발되었고, Hadoop에 적용된 것은 2012년.
  + 또한 YARN 아키텍처에서는 MR로 구현된 작업이 아니어도 컨테이너를 할당 받아서 동작할 수 있기 때문에 Spark, HBase, Storm 등 다양한 컴포넌트들을 실행할 수 있습니다.
  </aside>

- Hadoop v3 : 
  - 이레이져 코딩(Erasure Coding) : Parity블록을 생성해 기존의 3벌복제를 통한 fault-tolerant를 개선. Hadoop v2의 3벌복제가 200%의 디스크사용량이라면 Hadoop V3의 Erasure Coding은 150%사용.
  - YARN 타임라인서비스 v2 : [The YARN Timeline Service v.2](yarn_timelinev2)
  - Namenode HA 2대 이상지원
  - Ozone

<img src="/image/erasure.png" alt="erasure_coding" style="height: 300px; width:700px;"/>

---

## Hadoop's Architecture

## HDFS
하둡 분산 파일 시스템(HDFS, Hadoop Distributed File System)은 상용 하드웨어에서 실행되도록 설계된 분산 파일 시스템이다. HDFS는 내결함성이 뛰어나며 저렴한 하드웨어에 배포되도록 설계되었습니다. HDFS는 애플리케이션 데이터에 대한 높은 처리량 액세스를 제공하며, 데이터 세트가 큰 애플리케이션에 적합합니다. HDFS는 파일 시스템 데이터에 대한 스트리밍 액세스를 가능하게 하기 위해 몇 가지 POSIX 요구 사항을 완화합니다. HDFS는 원래 아파치 너치 웹 검색 엔진 프로젝트를 위한 인프라로 구축되었다. HDFS는 이제 아파치 하둡 하위 프로젝트이다.

### 특징
- 블록 단위 저장
- 블록 복제를 이용한 장애 복구
- 읽기 중심
- 데이터 지역성


<img src="/image/hdfsarchitecture.png" alt="hdfsarchitecture.png" style="height: 300px; width:700px;"/>

- HDFS: Namenode + Datanode
  - Namenode : Metadata, Datanode 관리
    - HDFS Metadata : 이름, 크기, 생성시간, 접근권한, 소유자&그룹, 블록위치, etc
      - Fsimage : 네임스페이스와 블록 정보
      - Edits file : 파일의 생성, 삭제에 따른 트랜잭션 로그, 1. 메모리에 저장, 2. Namenode dfs.name.dir 경로에 저장
  - Datanode : 블록단위의 파일 저장

## YARN
YARN(Yet Another Resource Negotiator)은 하둡2에서 도입한 클러스터 리소스 관리 및 애플리케이션 라이프 사이클 관리를 위한 아키텍처. YARN의 기본 아이디어는 자원 관리와 작업 스케줄링/모니터링의 기능을 별도의 데몬으로 나누는 것이다.

<img src="/image/yarnarchitecture.png" alt="hdfsarchitecture.png" style="height: 300px; width:700px;"/>

- YARN : Resource Manager + Node Manager, AM(Application Master) + Container

### YARN 기능 및 특징
- 자원관리
  - Node Manager:  클러스터의 각 노드마다 실행되어 현재 노드의 자원 상태를 관리하고, Resource Manager에 현재 자원 상태를 보고합니다.
  - Resource Manager: Node Manager에서 전달받은 정보를 이용하여 클러스터 전체의 자원을 관리. 자원 사용 상태를 모니터링하고, Application Master에서 자 자원을 요청시 유휴 자원을 할당.
  - Scheduler : 자원 분배 규칙 설정
- Life cycle 관리
  1. 클라이언트가 리소스 매니저에 애플리케이션을 제출
  2. 리소스 매니저는 비어 있는 노드에서 애플리케이션 마스터를 실행. 
  3. 애플리케이션 마스터는 작업 실행을 위한 자원을 리소스 매니저에 요청하고
  4. 자원을 할당 받아서 각 노드에 컨테이너를 실행하고, 실제 작업을 진행합니다. 
  5. 컨테이너에서 작업이 종료되면 결과를 애플리케이션 마스터에게 알리고 애플리케이션 마스터는 모든 작업이 종료되면 리소스매니저에 알리고 자원을 해제합니다.

---
### reference
- [https://hadoop.apache.org/docs/stable/hadoop-yarn/hadoop-yarn-site/TimelineServiceV2.html][yarn_timelinev2]
- [https://wikidocs.net](wikidocs)

[yarn_timelinev2]: https://hadoop.apache.org/docs/stable/hadoop-yarn/hadoop-yarn-site/TimelineServiceV2.html
[wikidocs]: https://wikidocs.net/22766