---
layout: post
title: "GCP Kubernetes 공부" #게시물 이름
tags: [Apache, Cloudera, CDP, AWS, VPC, EC2, Instance, Public Cloud, study] #태그 설정
categories: Study #카테고리 설정
author: # 작성자
  - Byungineer
#toc : true #Table of Contents
---

서비스(Service)란?
쿠버네티스 환경에서 서비스(Service)는 파드들을 통해 실행되고 있는 애플리케이션을 네트워크에 노출(expose)시키는 가상의 컴포넌트다. 쿠버네티스 내부의 다양한 객체들이 애플리케이션과, 그리고 애플리케이션이 다른 외부의 애플리케이션이나 사용자와 연결될 수 있도록 도와주는 역할을 한다.

왜 서비스란 것이 필요하게 되었을까? 클러스터 안에서 애플리케이션을 구동시키는 데에 쓰이는 파드들의 반영속적인(ephemeral) 특성 때문이다. 파드를 소개했던 지난 글의 내용처럼, 쿠버네티스에서의 파드는 무언가가 구동 중인 상태를 유지하기 위해 동원되는 일회성 자원으로 언제든 다른 노드로 옮겨지거나 삭제될 수 있다. 또한 파드는 생성될 때마다 새로운 내부 IP를 받게 되므로, 이것만으로 클러스터 내/외부와 통신을 계속 유지하기는 어렵다.

따라서 쿠버네티스에서는 파드가 외부와 통신할 수 있도록 클러스터 내부에서 고정적인 IP를 갖는 서비스(Service)를 이용하도록 하고 있다. 서비스는 또한 디플로이먼트나 스테이트풀셋처럼 같은 애플리케이션을 구동하도록 구성된 여러 파드들에게 단일한 네트워크 진입점을 부여하는 역할도 한다.

서비스를 정의하고 생성할 때에는 spec.ports 아래에 연결하고자 하는 항목 별로 각각 2개씩의 포트가 지정되어야 한다. 아래의 항목 명칭은 클러스터 안에서 트래픽을 중계하는 서비스의 입장에서 기술된 것임을 이해하자.

targetPort : 파드의 애플리케이션 쪽에서 열려있는 포트를 의미한다. 서비스로 들어온 트래픽은 해당 파드의 <클러스터 내부 IP>:<targetPort>로 넘어가게 된다.
port : 서비스 쪽에서 해당 파드를 향해 열려있는 포트를 의미한다.
서비스의 유형
쿠버네티스에서 서비스의 유형은 크게 4가지로 분류된다. 명세(spec) 상에 type가 별도로 지정되지 않았다면 ClusterIP로 고정된다.

ClusterIP (기본 형태)
NodePort
LoadBalancer
ExternalName
1. ClusterIP (기본 형태)
ClusterIP는 파드들이 클러스터 내부의 다른 리소스들과 통신할 수 있도록 해주는 가상의 클러스터 전용 IP다. 이 유형의 서비스는 <ClusterIP>로 들어온 클러스터 내부 트래픽을 해당 파드의 <파드IP>:<targetPort>로 넘겨주도록 동작하므로, 오직 클러스터 내부에서만 접근 가능하게 된다. 쿠버네티스가 지원하는 기본적인 형태의 서비스다.

ClusterIP 유형의 서비스 구조 (이미지 출처 : Google Cloud) https://medium.com/google-cloud/kubernetes-nodeport-vs-loadbalancer-vs-ingress-when-should-i-use-what-922f010849e0
ClusterIP 유형의 서비스 구조 (이미지 출처 : Google Cloud)
Selector를 포함하는 형태
TCP 포트 9376을 수신 대기(listen)하며 app=myapp, type=frontend라는 레이블을 공유하는 파드들에게 myapp-service라는 이름으로 접근할 수 있게 해주는 ClusterIP 유형의 서비스를 정의하면 다음과 같다.

apiVersion: v1
kind: Service
metadata:
  name: myapp-service
spec:
  type: ClusterIP		# 생략 가능
  ports:
  - protocol: TCP
    targetPort: 9376	# 애플리케이션(파드)을 노출하는 포트
    port: 80			# 서비스를 노출하는 포트
  selector:				# 이 서비스가 적용될 파드 정보를 지정 (선택이나 권장 사항)
    app: myapp
    type: frontend
위에서 spec.selector에서 지정된 레이블로 여러 파드들이 존재할 경우, 서비스는 그 파드들을 외부 요청(request)을 전달할 엔드포인트(endpoints)로 선택하여 트래픽을 분배하게 된다. 이를 이용하여 한 노드 안에 여러 파드, 또는 여러 노드에 걸쳐 있는 여러 파드에 동일한 서비스를 적용할 수 있다.

때로는 여러 포트들의 연결이 필요할 때도 있다. (예: HTTP/HTTPS) 이럴 땐 spec.ports에 리스트 형태로 name 값을 부여하여 각각 추가해주면 된다. 이때 name 필드에 들어가는 값은 반드시 영문/소문자 및 숫자와 -로만 이루어져야 하며, 첫 글자와 마지막 글자는 반드시 영문/소문자 및 숫자로만 쓰여야 한다.

apiVersion: v1
kind: Service
metadata:
  name: myapp-service
spec:
  type: ClusterIP
  ports:
  - name: http
    protocol: TCP
    targetPort: 9376
    port: 80
  - name: https
    protocol: TCP
    targetPort: 9377
    port: 443
  selector:
    app: myapp
    type: frontend
Selector가 제외된 형태
필요에 따라 엔드포인트(Endpoints)를 수동으로 직접 지정해줘야 할 때가 있다. 테스트 환경과 상용 환경의 설정이 서로 다르거나, 다른 네임스페이스 또는 클러스터에 존재하는 파드와의 네트워크를 위해 서비스-서비스 간의 연결을 만들어야 하는 상황 등이 있다.

이런 경우에는 spec.selector 없이 서비스를 만들고, 해당 서비스가 가리킬 엔드포인트(Endpoints) 객체를 직접 만들어 해당 서비스에 맵핑하는 방법이 있다.

apiVersion: v1
kind: Service
metadata:
  name: myapp-service
spec:
  ports:
    - protocol: TCP
      port: 80
      targetPort: 9376
apiVersion: v1
kind: Endpoints
metadata:
  name: myapp-service		# 연결할 서비스와 동일한 name을 메타데이터로 입력
subsets:					# 해당 서비스로 가리킬 endpoint를 명시
  - addresses:
      - ip: 192.0.2.42
    ports:
      - port: 9376
이때 주의해야 할 점은, 엔드포인트로 명시할 IP는 loopback(127.0.0.0/8) 또는 link-local(169.254.0.0/16, 224.0.0.0/24) 이어서는 안 된다는 것이다. 이에 대한 자세한 내용은 쿠버네티스 공식 메뉴얼 문서에서 확인할 수 있다.

2. NodePort
NodePort는 외부에서 노드 IP의 특정 포트(<NodeIP>:<NodePort>)로 들어오는 요청을 감지하여, 해당 포트와 연결된 파드로 트래픽을 전달하는 유형의 서비스다. 이때 클러스터 내부로 들어온 트래픽을 특정 파드로 연결하기 위한 ClusterIP 역시 자동으로 생성된다.

NodePort 유형의 서비스 구조 (이미지 출처 : Google Cloud) https://medium.com/google-cloud/kubernetes-nodeport-vs-loadbalancer-vs-ingress-when-should-i-use-what-922f010849e0
NodePort 유형의 서비스 구조 (이미지 출처 : Google Cloud)
이 유형의 서비스에서는 spec.ports 아래에 nodePort를 추가로 지정할 수 있다. nodePort는 외부에서 노드 안의 특정 서비스로 접근할 수 있도록 지정된 노드의 특정 포트를 의미한다. nodePort로 할당 가능한 포트 번호의 범위는 30000에서 32767 사이이며, 미지정시 해당 범위 안에서 임의로 부여된다.

apiVersion: v1
kind: Service
metadata:
  name: myapp-service
spec:
  type: NodePort
  ports:
  - targetPort: 80		# 애플리케이션(파드)을 노출하는 포트
    port: 80			# 서비스를 노출하는 포트
    nodePort: 30008		# 외부 사용자가 애플리케이션에 접근하기 위한 포트번호(선택)
  selector:				# 이 서비스가 적용될 파드 정보를 지정
    app: myapp
    type: frontend
NodePort의 경우에도 spec.selector에 해당하는 모든 파드들에 동일한 로드 밸런싱이 적용된다. 만약 같은 레이블의 파드들이 다른 여러 노드에 걸쳐 존재한다면, 해당 노드들에도 같은 서비스가 자동으로 생성되면서 같은 번호의 노드포트를 통한 해당 파드들의 접근이 허용된다. 예를 들어 192.168.1.2 노드와 192.168.1.3 노드에 각각 같은 레이블의 파드가 존재할 경우, NodePort 서비스를 통해 192.168.1.2:<nodePort> 또는 192.168.1.3:<nodePort> 중 어떤 경로를 이용하더라도 해당되는 파드들에 연결이 가능해진다.

3. LoadBalancer
별도의 외부 로드 밸런서를 제공하는 클라우드(AWS, Azure, GCP 등) 환경을 고려하여, 해당 로드 밸런서를 클러스터의 서비스로 프로비저닝할 수 있는 LoadBalancer 유형도 제공된다.

LoadBalancer 유형의 서비스 구조 (이미지 출처 : Google Cloud) https://medium.com/google-cloud/kubernetes-nodeport-vs-loadbalancer-vs-ingress-when-should-i-use-what-922f010849e0
LoadBalancer 유형의 서비스 구조 (이미지 출처 : Google Cloud)
이 유형은 서비스를 클라우드 제공자 측의 자체 로드 밸런서로 노출시키며, 이에 필요한 NodePort와 ClusterIP 역시 자동 생성된다. 이때 프로비저닝된 로드 밸런서의 정보는 서비스의 status.loadBalancer 필드에 게재된다.

apiVersion: v1
kind: Service
metadata:
  name: myapp-service
spec:
  type: LoadBalancer
  ports:
    - protocol: TCP
      port: 80				# 서비스를 노출하는 포트
      targetPort: 80		# 애플리케이션(파드)를 노출하는 포트
  clusterIP: 10.0.171.239	# 클러스터 IP
  selector:
    app: myapp
    type: frontend
status:
  loadBalancer:				# 프로비저닝된 로드 밸런서 정보
    ingress:
    - ip: 192.0.2.127
이렇게 구성된 환경에서는, 외부의 로드 밸런서를 통해 들어온 트래픽이 서비스의 설정값을 따라 해당되는 파드들로 연결된다. 이 트래픽이 어떻게 로드 밸런싱이 될지는 클라우드 제공자의 설정에 따르게 된다.

만약 이러한 방식의 로드 밸런서 프로비저닝을 지원하지 않는 클라우드 환경(예: Virtualbox)일 경우, 이 유형으로 지정된 서비스는 NodePort와 동일한 방식으로 동작하게 된다.

4. ExternalName
서비스에 selector 대신 DNS name을 직접 명시하고자 할 때에 쓰인다. spec.externalName 항목에 필요한 DNS 주소를 기입하면, 클러스터의 DNS 서비스가 해당 주소에 대한 CNAME 레코드를 반환하게 된다.

apiVersion: v1
kind: Service
metadata:
  name: myapp-service
  namespace: prod
spec:
  type: ExternalName
  externalName: my.database.example.com
CLI 명령어로 파드에 서비스 적용하기
서비스는 YAML 형태로 정의하는 것이 좋지만, 생성된 파드를 간단히 외부에 노출시키고자 할 때에는 CLI 명령어로 보다 간편하게 수행할 수도 있다. kubectl create service <서비스유형> ... 형태로 할 수도 있지만, 특정 리소스에 한해 즉시 노출시키고자 한다면 kubectl expose 명령을 이용하여 서비스 배포와 노출을 동시에 진행 가능하다.

# Create a new pod called custom-nginx using the nginx image and expose it on container port 8080.
kubectl run custom-nginx --image=nginx --port=8080 && kubectl expose pod custom-nginx
예를 들어 redis라는 파드의 6379 포트를 ClusterIP로 클러스터에 노출시켜야 한다고 가정해보자. 서비스를 직접 생성하여 연결하려면 아래와 같은 명령을 생각해 볼 수 있다.

kubectl create service clusterip redis --tcp=6379:6379
그러나 위와 같은 접근법에는 문제가 하나 있다. 명령어를 통한 서비스 생성시 spec.selector는 app=redis로 고정되며, 따로 YAML로 빼서 다시 수정하지 않는 이상 실제 연결하고자 하는 파드의 레이블 정보를 반영할 수 없다. 따라서 이런 경우에는 서비스를 직접 만들기보다는, 다음과 같이 kubectl expose pod 명령을 사용하는 것이 좋다.

kubectl expose pod redis --port=6379 --name redis-service
맺음말
이상으로 ClusterIP, NodePort, LoadBalancer, ExternalName의 네 종류로 구성된 쿠버네티스의 서비스 종류를 살펴보았다.

서비스는 파드 또는 파드들의 그룹을 통해 구동되는 애플리케이션에게 고정적인 네트워크 접근점을 만들어 주는 객체다. 실제 쿠버네티스 클러스터를 통해 여러 애플리케이션으로 구성된 시스템을 구축하려면, 위와 같은 서비스들의 유형과 용도를 명확히 이해하는 것이 필요하다.

ReplicaSet 컨트롤러는 모두 동일한 포드 그룹이 동시에 실행되도록 합니다. 배포를 통해 ReplicaSet 및 Pods에 대한 선언적 업데이트를 수행할 수 있습니다. 실제로 배포는 사용자가 지정한 선언적 목표를 달성하기 위해 자체 복제 세트를 관리하므로, 가장 일반적으로 배포 개체로 작업할 수 있습니다.

배포를 사용하면 필요에 따라 ReplicaSet을 사용하여 포드를 생성, 업데이트, 롤백 및 확장할 수 있습니다. 예를 들어, 배포의 롤링 업그레이드를 수행할 때 배포 개체는 두 번째 ReplicaSet을 작성한 다음 원래 ReplicaSet의 포드 수를 줄일 때 새 ReplicaSet의 포드 수를 늘립니다.

복제 컨트롤러는 ReplicaSet 및 배포의 조합과 유사한 역할을 수행하지만 더 이상 사용하지 않는 것이 좋습니다. 배포는 ReplicaSets에 유용한 "프런트 엔드"를 제공하기 때문에 이 교육 과정은 주로 배포에 중점을 둡니다.

로컬 상태를 유지하는 애플리케이션을 배포해야 하는 경우 StatefulSet이 더 나은 옵션입니다. 상태 저장 집합은 포드가 동일한 컨테이너 규격을 사용한다는 점에서 배포와 유사합니다. 그러나 Deployment를 통해 생성된 포드에는 영구 ID가 부여되지 않습니다. 대조적으로 StatefulSet을 사용하여 생성된 포드에는 안정적인 네트워크 ID와 영구 디스크 스토리지가 있는 고유한 영구 ID가 있습니다. 

클러스터 내의 모든 노드 또는 선택한 노드에서 특정 포드를 실행해야 하는 경우 DaemonSet을 사용하십시오. DaemonSet은 특정 포드가 노드의 모든 부분 집합 또는 일부 부분 집합에서 항상 실행되도록 합니다. 새 노드가 추가되면 DaemonSet은 자동으로 필요한 사양의 해당 노드에 Pods를 설정합니다. 데몬(daemon)은 컴퓨터 과학 용어로서, 다른 프로세스에 유용한 서비스를 제공하는 비인터랙티브 프로세스를 의미한다. Kubernetes 클러스터는 DaemonSet을 사용하여 fluentd와 같은 로깅 에이전트가 클러스터의 모든 노드에서 실행되도록 할 수 있습니다.

작업 컨트롤러는 태스크를 실행하는 데 필요한 하나 이상의 포드를 생성합니다. 작업이 완료되면 Job은 모든 Pods를 종료합니다. 관련 컨트롤러로는 시간 기반 일정에 따라 팟을 실행하는 크론잡(CronJob)이 있다.

