---
layout: post
title: "Apache Hadoop 개념 정리" #게시물 이름
tags: [Apache, Hadoop, HDFS, 하둡, Cloudera, study] #태그 설정
categories: Study #카테고리 설정
author: # 작성자
  - Byungineer
#toc : true #Table of Contents
---

Cloudera Data Platform을 다루며, Hadoop Ecosystem의 모체가 되는 Hadoop의 구조, 특징 및 기능에 대해 개념을 확실하게 가져가기 위해 내용 정리를 해본다.

## Hadoop's Architecture
### Hadoop 버전별 특징
Apache Hadoop은 현재 Ver3로, 2011년에 Hadoop(ver1)이 정식 발표된 이후로 구조적, 기능적인 발전이 있었다. 핵심적인 버전별 특징에 대해 간략하게 정리해본다.

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





YARN 아키텍처의 작업의 처리 단위는 컨테이너입니다. 작업에 제출되면 애플리케이션 마스터가 생성되고, 애플리케이션 마스터가 리소스 매니저에 자원을 요청하여 실제 작업을 담당하는 컨테이너를 할당받아 작업을 처리합니다. 컨테이너는 작업이 요청되면 생성되고, 작업이 완료되면 종료되기 때문에 클러스터를 효율적으로 사용할 수 있습니다.



자원관리와 애플리케이션 관리의 분리를 통해 클러스터당 최대 만개의 노드를 등록할 수 있습니다.


---
### reference

[yarn_timelinev2]: https://hadoop.apache.org/docs/stable/hadoop-yarn/hadoop-yarn-site/TimelineServiceV2.html