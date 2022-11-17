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
Apache Hadoop은 현재 Ver3로, 2011년에 Hadoop(ver1)이 정식 발표된 이후로 구조적, 기능적인 발전이 있었다.

- Hadoop v1 : 병렬처리를 위해 잡트래커(Job Tracker), 태스크트래커(Task Tracker)로 구성되었다.
  - 잡트래커 : 병렬처리 중인 작업의 진행 관리, 자원 관리
  - 태스크트래커 : 실제 작업을 수행(map & reduce), 작업의 단위는 슬롯(slot)이며 Map과 Reduce 슬롯의 개수는 정해져 있다. 즉, 맵의 작업이 다 끝나도 리듀스의 슬롯의 갯수가 늘어나지는 않는다.

<img src="/image/hadoopv1.png" alt="hadoopv1" style="height: 300px; width:700px;"/>

