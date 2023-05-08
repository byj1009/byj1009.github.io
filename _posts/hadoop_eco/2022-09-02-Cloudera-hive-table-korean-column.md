---
layout: post
title: "Hive table에서 한글 컬럼명, 코멘트 사용하기" #게시물 이름
tags: [Apache, Clouder, CDP, Hive, table, metastore, study] #태그 설정
categories: Hadoop #카테고리 설정
author: # 작성자
  - Byungineer
#toc : true #Table of Contents
---

Mysql에 Hive metastore DB를 생성하여 hive table을 관리하면, 기본적으로 한글을 사용할 수(글자가 ???로 나옴) 없습니다.

이러한 문제를 해결하기 위해서는 Default Charater set을 latin1에서 UTF8로 변경해야 합니다.

다음의 과정은

[https://heum-story.tistory.com/34][heum-story]


```
alter table COLUMNS_V2 modify COMMENT varchar(256) character set utf8 collate utf8_general_ci;
alter table TABLE_PARAMS modify PARAM_VALUE mediumtext character set utf8 collate utf8_general_ci;
alter table SERDE_PARAMS modify PARAM_VALUE mediumtext character set utf8 collate utf8_general_ci;
alter table SD_PARAMS modify PARAM_VALUE mediumtext character set utf8 collate utf8_general_ci;
alter table PARTITION_PARAMS modify PARAM_VALUE varchar(4000) character set utf8 collate utf8_general_ci;
alter table PARTITION_KEYS modify PKEY_COMMENT varchar(4000) character set utf8 collate utf8_general_ci;
alter table INDEX_PARAMS modify PARAM_VALUE varchar(4000) character set utf8 collate utf8_general_ci;
alter table DATABASE_PARAMS modify PARAM_VALUE varchar(4000) character set utf8 collate utf8_general_ci;
alter table DBS modify `DESC` varchar(4000) character set utf8 collate utf8_general_ci;
```

```
alter table COLUMNS_V2 modify COLUMN_NAME varchar(767) character set utf8 collate utf8_general_ci;
alter table TABLE_PARAMS modify PARAM_KEY varchar(256) character set utf8 collate utf8_general_ci;
alter table SERDE_PARAMS modify PARAM_KEY varchar(256) character set utf8 collate utf8_general_ci;
alter table SD_PARAMS modify PARAM_KEY varchar(256) character set utf8 collate utf8_general_ci;
alter table PARTITION_PARAMS modify PARAM_KEY varchar(256) character set utf8 collate utf8_general_ci;
alter table PARTITION_KEYS modify PKEY_NAME varchar(128) character set utf8 collate utf8_general_ci;
alter table PARTITION_KEYS modify PKEY_TYPE varchar(767) character set utf8 collate utf8_general_ci;
alter table INDEX_PARAMS modify PARAM_KEY varchar(256) character set utf8 collate utf8_general_ci;
alter table DATABASE_PARAMS modify PARAM_KEY varchar(180) character set utf8 collate utf8_general_ci;
alter table DBS modify `NAME` varchar(128) character set utf8 collate utf8_general_ci;

alter table TAB_COL_STATS modify `TABLE_NAME` varchar(256) character set utf8 collate utf8_general_ci;
alter table TAB_COL_STATS modify `COLUMN_NAME` varchar(640) character set utf8 collate utf8_general_ci;
```






```show full columns from AUX_TABLE;
show full columns from BUCKETING_COLS;               
show full columns from CDH_VERSION;              
show full columns from CDS;
show full columns from COLUMNS_V2;
show full columns from COMPACTION_QUEUE;
show full columns from COMPLETED_COMPACTIONS;
show full columns from COMPLETED_TXN_COMPONENTS;
show full columns from CTLGS;
```


---
### reference
- [https://heum-story.tistory.com/34][heum-story]
[heum-story]: https://heum-story.tistory.com/34