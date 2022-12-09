---
layout: post
title: "Python SQLAlchemy SQL문 예시" #게시물 이름
#tags: [Data Engineering, Data Engineer, 데이터엔지니어, Big data, python, python3, ,sqlalchemy, ORM, ,dbapi, study] #태그 설정
tags: [pyhton, programming, language, 파이썬] #태그 설정
categories: python_dev #카테고리 설정
author: # 작성자
  - Byungineer
#toc : true #Table of Contents
---

### where
```
SQL : SELECT * FROM census  WHERE sex = F
SQLAlchemy : db.select([census]).where(census.columns.sex == 'F')
```

### in
```
SQL : SELECT state, sex FROM census WHERE state IN (Texas, New York)
SQLAlchemy : db.select([census.columns.state, census.columns.sex]).where(census.columns.state.in_(['Texas', 'New York']))
```

### and, or, not
```
SQL : SELECT * FROM census WHERE state = 'California' AND NOT sex = 'M'
SQLAlchemy : db.select([census]).where(db.and_(census.columns.state == 'California', census.columns.sex != 'M'))
```

### order by
```
SQL : SELECT * FROM census ORDER BY State DESC, pop2000
SQLAlchemy : db.select([census]).order_by(db.desc(census.columns.state), census.columns.pop2000)
```

### functions(avg, count, min, max…)
```
SQL : SELECT SUM(pop2008) FROM census
SQLAlchemy : db.select([db.func.sum(census.columns.pop2008)])
```

### group by
```
SQL : SELECT SUM(pop2008) as pop2008, sex FROM census
SQLAlchemy : db.select([db.func.sum(census.columns.pop2008).label('pop2008'), census.columns.sex]).group_by(census.columns.sex)
```

### distinct
```
SQL : SELECT DISTINCT state FROM census
SQLAlchemy : db.select([census.columns.state.distinct()])
```

### join
```
# Automatic Join
query = db.select([table1.columns.column_name, table2.columns.column_name])
result = connection.execute(query).fetchall()

# Manual Join
query = db.select([table1, table2])
query = query.select_from(table1.join(table2, table1.columns.column_name == table2.columns.column_name))
```

### Updating data in Databases
```
db.update(table_name).values(attribute = new_value).where(condition)
```

### Delete Table
```
db.delete(table_name).where(condition)
```

### Dropping a Table
```
table_name.drop(engine) #drops a single table
metadata.drop_all(engine) #drops all the tables in the database
```
# fetchall() 함수. 레코드를 배열 형식으로 저장, 만약 메모리가 부족할 때는?
# fetchmany() 데이터가 커서 OOM이 일어날 수 있을 때는, 최적화된 갯수의 열만 가져옴
---

### reference

https://towardsdatascience.com/sqlalchemy-python-tutorial-79a577141a91