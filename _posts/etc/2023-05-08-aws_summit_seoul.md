---
layout: post
title: "[etc] AWS Summit Seoul 2023 day2 후기" #게시물 이름
tags: [AWS, summit, review, 후기] #태그 설정
categories: ETC #카테고리 설정
author: # 작성자
  - Byungineer
#toc : true #Table of Contents
---

2023-05-04 목요일, 코엑스 컨벤션 센터에서 진행하는 `AWS Summit Seoul 2023`에 다녀왔다.   
코로나 바이러스로 인해 2019년 이후 3년만에 진행되는 오프라인 행사로, 국내 최대 규모의 IT 컨퍼런스라고 한다. 05/03 ~ 05/04, 총 2일간 진행되었으며, 회사 업무 일정상 Summit 2일차 `기술 주제별 강연`에만 참여할 수 있었다.


## AWS SUMMIT SEOUL Day2

<img src="/image/AWS_Summit_Seoul_2023_Agenda.png" alt="agenda" style="height: 1200px; width:1200px;"/>

`AWS Summit Seoul`은 09:30 ~ 18:00 까지 진행되었으며 세션 당 30~40분 정도로 내가 듣고자 하는 강연을 들을 수 있다.   
세션 간 쉬는시간 30분동안 참여하고자 하는 장소로 이동해 대기 줄을 서야 했는데, 인기가 많은 주제는 만석으로 강연을 들을 수 없는 경우도 있다.   

또한, 취업박람회 처럼 AWS를 스폰하는 다양한 기업들의 기술 & 솔루션을 체험할 수 있는 `AWS EXPO`도 있었는데, 다양한 경품도 수령하고 현장에서의 미니 세션을 통해 솔루션을 체험할 수 있는 장소도 있다.

09:30 부터 18:00 까지, 기조연설을 포함한 총 7가지의 세션 중 내가 참여한 세션은 다음과 같다.
- 09:30 ~ 10:40 : 기조연설
- 11:10 ~ 11:50 : "오픈소스 데이터베이스로 탈 오라클! Why not?"
        +++ 중식 +++
- 13:10 ~ 13:50 : "데이터 공유와 활용! 전사 데이터 거버넌스를 위한 3가지 비밀 무기"
- 14:20 ~ 14:50 : "Confluent와 함께하는 실시간 데이터와 클라우드 여정"
- 15:20 ~ 16:00 : "12가지 디자인 패턴으로 알아보는 클라우드 네이티브 마이크로 서비스 아키텍처"
- 16:20 ~ 16:50 : AWS EXPO 참여 (세션장 만석으로 못 들어감...)
- 17:20 ~ 18:00 : "실시간 CDC 데이터 처리! Modern Transactional Data Lake 구축하기"


### 기조연설
09:30 ~ 10:40, 약 1시간동안 진행 된 기조연설에서는 Amazon의 CTO, AWS 서버리스 컴퓨팅의 부사장 등, Cloud 오피니언 리더들과의 인터뷰를 통해 최신 기술 주제들에 대한 이야기를 하는 시간이었다. 특히, 스타트업(flitto)의 CTO, 엔터프라이즈(LGU+)의 연구위원들의 글로벌 서비스 구축 경험을 기반으로 한 대담은 매우 인상적이었다.   

_개인적으로, LGU+의 연구위원이신 송주영님의 "탄탄한 기초의 중요성"은 많은 것을 생각하게 하는 중요한 워딩이었던 것 같다._

---


<img src="/image/IMG_6242.JPEG" alt="agenda" style="height:600px; width:800px;"/>


기조연설이 끝난 후, 다음 세션으로 이동하기 전에 로비를 촬영한 사진.   
점심 이후로는 사람이 많아서 바글바글 했다.

### 오픈소스 데이터베이스로 탈 오라클! Why not?
AWS SUMMIT SEOUL 2023 Day2, 내가 처음으로 참가한 세션은 오라클DB에서의 AWS 서비스로의 이관을 주제로 하는 강연이었다. 관리와 비용의 문제로 탈 오라클을 외치는 엔터프라이즈(대기업)들이 늘어나고 있음을 빅데이터 플랫폼 구축 프로젝트에서 느낄 수 있었는데, Cloud로의 Migration을 통해 얻을 수 있는 이점이 무엇이 있을지 궁금해 선택하게 된 강연이었다.


기존의 RDB를 AWS의 관리형 서비스로 전환하기 위한 선택지는 다음과 같다. 
- 자체 관리형 DB-> AWS 관리형 DB
  - Amazon Aurora
  - Amazon RDS
  - Amazon DocumentDB
  - Amazon ElastiCache
  - Amazon MemoryDB
- 상용 DB -> 오픈소스 DB
  - Amazon Aurora
  - Amazon RDS
- 모놀리식 -> 마이크로 서비스
  - Amazon DynamoDB
  - Amazon ElstiCache
  - Amazon Neptune
  - Amazon DocumentDB
  - Amazon Timestream

이 외에도 EC2에 Opensource RDBMS를 자체 구축하여 운영할 수 있다.



### 중식

### 데이터 공유와 활용! 전사 데이터 거버넌스를 위한 3가지 비밀 무기

### Confluent와 함께하는 실시간 데이터와 클라우드 여정

### 12가지 디자인 패턴으로 알아보는 클라우드 네이티브 마이크로 서비스 아키텍처

### AWS EXPO 참여 (세션장 만석으로 못 들어감...)

### 실시간 CDC 데이터 처리! Modern Transactional Data Lake 구축하기

