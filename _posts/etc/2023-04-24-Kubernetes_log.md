---
layout: post
title: "[kubernetes] Kubernetes Pods Log" #게시물 이름
tags: [Linux, kubernetes, log] #태그 설정
categories: Study #카테고리 설정
author: # 작성자
  - Byungineer
#toc : true #Table of Contents
---

Kubernetes의 특정 Pods의 로그를 파일로 저장하는 방법을 공부한 내용을 정리한다.   
필자가 테스트하고 있는 환경은 Cloudera의 Cloudera Data Science Workbench(CDSW)에 내장되어 있는 K8s이며,   
보통의 `kubernetes.io` 를 통해 다운로드 가능한 opensource k8s의 pods 로그는   

"/var/log/pods/{namespace}_{pod_name}/{container-name}/{count-number}.log" 에 있다.

하지만, Cloudera의 CDSW default아래의 Pods들은 해당 경로에 로그를 남기지 않기 때문에, `kubectl logs` 명령어를 통해 저장해야 한다.


## Kubernetes Pods log 추출

CDSW는 K8s, Docker로 구성된 서비스로, default 네임스페이스에 서비스 운영에 필요한 pods들이 서비스 시작과 함께 자동 생성된다.   
ex) database / web / registry / livelog / etc...

### 1. log 추출
해당 Pods의 로그를 Linux Local 파일로 저장하는 명령어는 다음과 같다.   
```bash
# RBAC(Role-Based Access Control)으로 CDSW 기본 Pods들에는 Role이 바인딩 되어 있습니다.
# 총 3개의 web pods 가 뜨기 때문에, jsonpath='{.items[0].metadata.name} 를 통한 pods 구분
$ cat cdsw_weblog_create_command.sh 
kubectl logs -f $(kubectl get pods -l role=web -o jsonpath='{.items[0].metadata.name}')  >  $PWD/cdsw_web1.log & \
kubectl logs -f $(kubectl get pods -l role=web -o jsonpath='{.items[1].metadata.name}')  >  $PWD/cdsw_web2.log & \
kubectl logs -f $(kubectl get pods -l role=web -o jsonpath='{.items[2].metadata.name}')  >  $PWD/cdsw_web3.log

$ nohup sh cdsw_weblog_create_command.sh &
```   
  <aside>
  💡 Web pod의 로그가 실시간을 계속 저장되고 있기 때문에, Background에서 명령어가 실행 될 수 있도록 위의 설정을 했다.
  </aside>  

**kubernetes_jsonpath활용하기**
kubectl get 명령어를 통해 얻을 수 있는 정보들을 사용자의 요구조건에 따라 조회하기 위해 JSONPath 템플릿을 활용할 수 있다. 관련 내용은 다음 포스팅에서 자세하게 다뤄보도록 하겠다.   

```
kubectl get pods -l role=web -o jsonpath='{.items[0].metadata.name}
```
현재, `kubectl get pods -l role=web` 명령어를 통해 나오는 출력물은 다음과 같다.

```bash
NAME                   READY   STATUS    RESTARTS   AGE
web-684c989f75-7tjtb   1/1     Running   0          45h
web-684c989f75-9ddhc   1/1     Running   0          45h
web-684c989f75-hpzjz   1/1     Running   0          45h
```

`kubectl get pods -l role=web -o json` 명령어를 통해 확인한 json 포멧 구조는 다음과 같다.
```
{
    "apiVersion": "v1",
    "items": [
        {
            "apiVersion": "v1",
            "kind": "Pod",
            "metadata": {
                "creationTimestamp": "2023-04-24T04:14:54Z",
                "generateName": "web-684c989f75-",
                "labels": {
                    "app": "web",
                    "hash": "f260849",
                    "pod-template-hash": "684c989f75",
                    "role": "web",
                    "version": "f260849"
                },
                "name": "web-684c989f75-7tjtb",
                "namespace": "default",
                "ownerReferences": [
                    {
                        "apiVersion": "apps/v1",
                        "blockOwnerDeletion": true,
                        "controller": true,
                        "kind": "ReplicaSet",
                        "name": "web-684c989f75",
                        "uid": "e0d9dd0d-563f-4bc6-bd77-dc0124bffa07"
                    }
                ],
                "resourceVersion": "2400",
                "selfLink": "/api/v1/namespaces/default/pods/web-684c989f75-7tjtb",
                "uid": "197aab3a-7eb3-4ea6-ac61-8bd52ad49311"
            },

### ~~~ 이하 생략
```
json 형태의 출력값을 보면 `items [ metadata { name }]` 이러한 구조로 값이 출력이 되고, 우리는 원하는 출력값을 얻기 위해   
`.items[0].metadata.name` 형태로 jsonpath를 설정할 수 있다.   

items[0~2] 의 숫자는 items list의 순서가 된다.