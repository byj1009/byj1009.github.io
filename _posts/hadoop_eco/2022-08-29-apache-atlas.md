---
layout: post
title: "Apache Atlas 개념 정리" #게시물 이름
tags: [Apache, Atlas, study] #태그 설정
categories: Hadoop #카테고리 설정
author: # 작성자
  - Byungineer
#toc : true #Table of Contents
---
## Apache Atlas
Atlas는 기본적으로 Hadoop 스택 내부 및 외부에서 다른 툴 및 프로세스와 메타데이터를 교환할 수 있어 플랫폼에 상관없이 거버넌수 제어가 가능하므로 규제 준수 요구 사항에 효과적으로 대응할 수 있습니다.

---

## Atlas 
Atlas 작동 원리
Apache Atlas는 기본적으로 Hadoop 및 광범위한 데이터 에코시스템 내에서 메타데이터를 효과적으로 교환할 수 있습니다. Atlas의 적응형 모델은  기존 메타데이터와  업계별  분류  방식을 활용하여 규제 준수 소요 시간을 단축합니다.또한 Atlas를 통해 데이터 관리자와 책임자는 데이터세트와 기본 요소(예: 소스, 대상 및 파생 프로세스 등) 간의 관계 포착을 정의하고, 주석을 달며, 자동화할 수 있습니다.

또한 Atlas는 기업이 타사 시스템으로 메타데이터를 손쉽게 내보낼 수 있도록 지원하여 에코시스템 전반에서 다운스트림 메타데이터의 일관성을 보장합니다.

## Data Lineage 기사
[data_lineage_news1]
[data_lineage_news2]


Apache Atlas는 메타데이터 기반의 Enterprise Hadoop를 위한 확장 가능한 거버넌스를 제공합니다. Atlas의 핵심은 새로운 비즈니스 프로세스와 데이터 자산을 민첩하고 손쉽게 모델링할 수 있다는 것입니다. 이 유연한 형식 시스템을 통해 Hadoop 스택 내부 및 외부에서 다른 툴 및 프로세스와 메타데이터를 교환할 수 있어 플랫폼에 상관없이 거버넌스 제어가 하므로 규제 준수 요구 사항에 효과적으로 대할 수 있습니다.

Apache Atlas는 다음 두 가지 원칙을 토대로 개발되었습니다.

Hadoop의 메타데이터 정보: Atlas는 Hadoop에서 진정한 가시성을 제공합니다. Atlas는 Hadoop 구성요소와의 네이티브 커넥터를 사용하여 비즈니스 분류 메타데이터로 강화된 기술 및 운영 추적 기능을 제공합니다. Atlas는 모든 메타데이터 소비자가 공통 메타데이터 스토어를 공유하여 여러 메타데이터 제작자 간의 상호 운용성을 촉진함으로써 메타데이터를 손쉽게 교환할 수 있도록 해줍니다.
개방형으로 개발: Aetna, Merck, SAS, Schlumberger, Target의 엔지니어들은 Hadoop을 사용하는 광범위한 산업 전반에서 실제 데이터 거버넌스 문제를 해결하려는 목적으로 Atlas를 구축하기 위해 협력하고 있습니다. 이러한 접근법은  데이터 퍼스트 기업의 제품 성숙도와 가치 창출 시간을 가속할 수 있는 오픈소스 커뮤니티 혁신의 한 예입니다.

Apache Atlas를 통해 기업은 확장 가능한 일련의 핵심 거버넌스 서비스 전반을 통해 규제 준수 요구 사항에 효율적으로 대응할 수 있습니다. 서비스의 내용은 다음과 같습니다.

데이터 계보: 플랫폼 수준에서 Hadoop 구성요소 전반의 계보 포착
민첩한 데이터 모델링: 유형 시스템은 계층 구조 분류에서 맞춤형 메타데이터 구조 지원
REST API: Atlas 서비스, HDP 구성요소, UI 및 외부 툴에 유연성 높은 최신 방식으로 액세스
메타데이터 교환: 기존 메타데이터/모델을 현재 툴에서 가져와 활용. 메타데이터를 다운스트림 시스템으로 내보내기

---

[data_lineage]


 

<img src="/image/atlas-banner.png" alt="test" style="height: 512px; width:512px;"/>



 
[data_lineage]: https://en.wikipedia.org/wiki/Data_lineage
[data_lineage_news1] : http://www.itdaily.kr/news/articleView.html?idxno=204141
[data_lineage_news2] : http://www.itdaily.kr/news/articleView.html?idxno=204142
