---
layout: post
title: "[Kubernetes] Postgresql pods, Query 실행하기" #게시물 이름
tags: [kubernetes, k8s, pod, postgresql, psql] #태그 설정
categories: Kubernetes #카테고리 설정
author: # 작성자
  - Byungineer
#toc : true #Table of Contents
---

Cloudera의 Cloudera Data Science Workbench(CDSW)를 유지보수 하며, CDSW에 내장된 Database(Postgresql) 사용에 도움이 되었던 명령어들을 정리해 본다.   

## Kubernetes pods & namespace

CDSW는 K8s 환경에서, 분석가들이 WebUI를 통해 분석 Session을 생성하면, 할당한 자원과 Docker image로 Pods가 생성된다.   
`cdsw status`라는 명령어를 사용하면, CDSW 서비스 구성에 필요한 Pods들의 상태와 리스트가 출력되며, `default` namespace에 생성이 되어 있다.

### Kubectl get pods
```
# Default namespace pods 출력
kubectl get pods   

#모든 Pods 출력
kubectl get pods -A

# 특정 namespace의 pods 출력
kubectl get pods -n [namespace]
```

### kubernetes exec

`exec` 명령어를 통해서 현재 `Running` STATUS인 K8s Pod에 접근이 가능하다(bash terminal).
- -i, --stdin=false: Pass stdin to the container
    ex) kubectl exec -i container command < file.stdin
  
  
- -t, --tty=false: Stdin is a TTY
    Stdin, 입력을 TTY(teletypewriter) 가상 콘솔,터미널을 열기 위한 옵션


kubectl exec 명령어의 사용 예시는 아래와 같다.   
```
# bash shell로 terminal 열기
kubectl exec -it [pods name] /bin/bash

# Container가 복수일 때
kubectl exec -it [pods name] -c [container name] /bin/bash
```

## Postgresql on Kubernetes pods

### Kubernetes Postgresql 접근 및 명령어 사용

Cloudera CDSW에서는 Pods 이름이 Service 재시작 과정에서 변경될 수 있기 때문에 아래의 명령어를 참고해 조회할 수 있다. 
```
kubectl exec -it [pods name] -- psql -U [User name]
# CDSW DB, role이라는 태그로 필터링
kubectl exec $(kubectl get pods --selector=role=db --namespace=default -o jsonpath='{.items[*].metadata.name}') -it -- psql -U sense

# CDSW의 DB user 정보를 조회하는 방법 / base64 : binary -> text
kubectl get secrets/internal-secrets --namespace=default -o 'go-template={{index .data "postgresql.user"}}' | base64 -d

```

### kubernetes pods에 파일 CP
Kubernetes pods에 파일을 넣거나, 복사해올 때 사용되는 명령어는 아래와 같다.   
postgresql에서 사용할 query문을 -f 옵션을 통해 실행하고자 해당 명령어를 사용했다.

```
# pods 내 저장위치 확인하기
kubectl exec -i [pods name] ls /
# 직접 들어가서 명령어 사용
kubectl exec -it [pods name]
$ls
```

파일 복사하기
```
# local to k8s pods
kubectl cp [local file] [pods name]:[pod내 저장 directory 및 파일]
# k8s pods to local
kubectl cp [pods name]:[pod내 저장 directory 및 파일] [local file]
```

sql 파일을 이용해 postgresql query 실행하기
```
kubectl exec [pods name] -- psql -U [user name] -f /tmp/query.sql
```


---
### Reference
