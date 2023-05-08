---
layout: post
title: "Self Signed TLS" #게시물 이름
tags: [Self Signed TLS, TLS, SSL, Certificate, 인증서, Certificate Authority, CA, 인증기관] #태그 설정
categories: Linux #카테고리 설정
author: # 작성자
  - Byungineer
#toc : true #Table of Contents
---

# Self signed SSL



## 1. Pre-config
Configure environment to set JAVA_HOME to the Oracle JDK (ALL host)
Java Home 경로가 설정되어 있는 경우에는 해당 과정을 스킵하면 된다.
설치한 Oracle Jdk or Open JDK에 맞는 경로로 경로를 설정해주면 된다.

```bash
vi ~/.bashrc
export JAVA_HOME=/usr/java/jdk1.8.0_232-cloudera
export PATH=$JAVA_HOME/bin:$PATH

#Directory 생성 ( Rootca Directory )
mkdir -p /opt/security/pki/ca
```

```bash
#CRT(인증서)생성에 필요한 configuration 파일 생성
vi /opt/security/pki/ca/rootca.cnf

[ req ]
default_bits = 2048
default_md = sha1
default_keyfile = rootca.key
distinguished_name = req_distinguished_name
extensions = v3_ca
req_extensions = v3_ca

[ v3_ca ]
basicConstraints = critical, CA:TRUE, pathlen:0
subjectKeyIdentifier = hash
##authorityKeyIdentifier = keyid:always, issuer:always
keyUsage = keyCertSign, cRLSign
nsCertType = sslCA, emailCA, objCA

[req_distinguished_name ]
countryName = Country Name (2 letter code)
countryName_default = KR
countryName_min = 2
countryName_max = 2
# 회사명 입력
organizationName = Organization Name (eg, co.krpany)
organizationName_default = Example Inc.
# 부서 입력
#organizationalUnitName = Organizational Unit Name (eg, section)
#organizationalUnitName_default = Condor Project
# SSL 서비스할 domain 명 입력
co.krmonName = co.krmon Name (eg, your name or your server's hostname)
co.krmonName_default = Example's Self Signed CA
co.krmonName_max = 64
```

```bash
vi /opt/security/pki/ca/openssl_host.cnf

[ req ]
default_bits = 2048
distinguished_name = req_distinguished_name
string_mask = utf8only
default_md = sha256
x509_extensions = server_cert

[ req_distinguished_name ]
countryName = Country Name (2 letter code)
stateOrProvinceName = State or Province Name
localityName = Locality Name
0.organizationName = Organization Name
organizationalUnitName = Organizational Unit Name
co.krmonName = co.krmon Name
emailAddress = Email Address
countryName_default = KR
stateOrProvinceName_default = Seoul
localityName_default = mapo #지역구
0.organizationName_default = example #회사이름
organizationalUnitName_default = bigdata #조직이름
emailAddress_default = test@example.co.kr

[ v3_ca ]
subjectKeyIdentifier = hash
authorityKeyIdentifier = keyid:always,issuer
basicConstraints = critical, CA:true
keyUsage = critical, ditestalSignature, cRLSign, keyCertSign

[ server_cert ]
basicConstraints = CA:FALSE
nsco.krment = "OpenSSL Generated Server Certificate"
subjectKeyIdentifier = hash
authorityKeyIdentifier = keyid,issuer
keyUsage = nonRepudiation, ditestalSignature, keyEncipherment
extendedKeyUsage = serverAuth, clientAuth
subjectAltName = @alt_names

[ alt_names ]
DNS.1 = example.co.kr
DNS.2 = *.example.co.kr
DNS.3 = test01.example.co.kr
DNS.4 = *.test01.example.co.kr
```

  <aside>
  💡 #Rootca.cnf 내용
  ● [ CA_default ] 는 기본값
  ● [ policy_strict ] 는 Root CA 사인에 적용할 정책
  ● [ policy_loose ] 는 Intermediate CA 사인에 적용할 정책
  ● [ req ] 는 인증서나 인증서 서명 요청서를 만들때 적용
  ● [ req_distinguished_name ] 는 인증서 서명 요청서의 필요한 정보를 선언, 일부 기본값을 지정
  ● [ v3_ca ] 는 Root 인증서를 만들때 확장 옵션 적용
  ● [ v3_intermediate_ca ] 는 Intermediate 인증서를 만들때 확장 옵션 적용, pathlen:0 는 중간 CA아래에 더 이상의 인증 기관이 존재할 수 없도록 보장
  ● [ usr_cert ] 는 클라이언트 인증서에 서명 할 때이 확장 옵션 적용
  ● [ server_cert ] 는 서버 인증서에 서명 할 때이 확장 옵션 적용
  ● [ crl_ext ] 는 인증서 폐기 목록을 만들때 확장 옵션 적용
  ● [ ocsp ] 는 온라인 인증서 상태 프로토콜 인증서에 확장 옵션 적용

  </aside>

## 2. RootCA생성

- Keytool을 이용한 jks(java key store) 파일 생성 // 공개키, 개인키, 인증서 발급까지 가능한 java에서 사용하는 키 저장소 방식. 내용 추출까지 가능하므로 csr key파일로 뽑아서 사용
- keytool을 이용한 java keystore와 CSR 생성 (비밀번호는 무조건 같아야 함, 다르면 CM 에러 발생)
    
### 1. test-rootca.jks 생성
    
  <aside>
  💡 SAN certificates
  Subject Alternative Name은 하나의 인증서로 여러개의 도메인을 등록하기 위해서 사용한다. 최대 100개의 도메인을 커버 할 수 있으며 그 사용의 예는 다음과 같다.
  SAN 1: DNS Name=example.co.kr
  
  SAN 2: DNS Name=www.example.co.kr
  
  SAN 3: DNS Name=example.net
  
  SAN 4: DNS Name=mail.example.co.kr
  
  SAN 5: DNS Name=support.example.co.kr
  
  SAN 6: DNS Name=example2.co.kr
  
  SAN 7: IP Address=93.184.216.34\
  
  SAN 8: IP Address= 2606:2800:220:1:248:1893:25c8:1946
  
  </aside>  

```bash
$JAVA_HOME/bin/keytool -genkeypair -alias test-rootca -keyalg RSA -keystore /opt/security/pki/ca/test-rootca.jks -keysize 2048 -dname "CN=test-rootca,OU=Bigdata_Team,O=Exapmle,L=MapoGu,ST=Seoul,C=KR

$JAVA_HOME/bin/keytool -genkeypair -alias test-rootca -keyalg RSA -keystore /opt/security/pki/ca/test-rootca.jks -keysize 2048 -dname "CN=test-rootca,OU=Bigdata_Team,O=test,L=MapoGu,ST=Seoul,C=KR" -ext san=dns:test01.example.co.kr
```

### 2. test-rootca.csr 생성

```bash
$JAVA_HOME/bin/keytool -certreq -alias test-rootca -keystore /opt/security/pki/ca/test-rootca.jks -file /opt/security/pki/ca/test-rootca.csr -ext san=dns:test01.example.co.kr -ext EKU=serverAuth,clientAuth
```

### 3. Jks로 pkcs #12 파일 생성

```bash
$JAVA_HOME/bin/keytool -importkeystore -srckeystore /opt/security/pki/ca/test-rootca.jks -destkeystore /opt/security/pki/ca/test-rootca.p12 -deststoretype PKCS12 -srcalias test-rootca
```

### 4. pkcs #12를 openssl로 key파일 생성(PEM형식)

```bash
openssl pkcs12 -in /opt/security/pki/ca/test-rootca.p12 -nocerts -out /opt/security/pki/ca/test-rootca.key
openssl pkcs12 -in /opt/security/pki/ca/test-rootca.p12 -nocerts -out /opt/security/pki/ca/test-rootca.key.pem
```

### 5. crt 인증서 생성

```bash
openssl x509 -req -days 3650 -extensions v3_ca -set_serial 1 -sha256 -in /opt/security/pki/ca/test-rootca.csr -signkey /opt/security/pki/ca/test-rootca.key -out /opt/security/pki/ca/test-rootca.crt -extfile /opt/security/pki/ca/openssl_rootca.cnf

openssl x509 -req -days 3650 -extensions v3_ca -set_serial 1 -sha256 -in /opt/security/pki/ca/test-rootca.csr -signkey /opt/security/pki/ca/test-rootca.key -out /opt/security/pki/ca/test-rootca.crt.pem -extfile /opt/security/pki/ca/openssl_rootca.cnf
```

# 외부 접근 및 수정을 방지를 위한 권한 변경

```bash
chmod 600 /opt/security/pki/ca/test-rootca.*
```

## 3.	Host 인증서 생성

1. CSR생성

```bash
$JAVA_HOME/bin/keytool -certreq -alias *.example.co.kr -keystore /opt/security/pki/asterisk.example.co.kr.jks -file /opt/security/pki/asterisk.example.co.kr.csr; done
```

1. jks >> pkcs 12

```bash
$JAVA_HOME/bin/keytool -importkeystore -srckeystore /opt/security/pki/test.example.co.kr.jks -destkeystore /opt/security/pki/test.example.co.kr.p12 -deststoretype PKCS12 -srcalias test.example.co.kr; done

```

1. pkcs 12 >>key

```bash
openssl pkcs12 -in /opt/security/pki/test.example.co.kr.p12 -nocerts -out /opt/security/pki/test.example.co.kr.key; done
```

## 4. getting CA Private key

```bash
openssl x509 -req -sha256 -days 365 -extensions server_cert -in /opt/security/pki/test.example.co.kr.csr -CA /opt/security/pki/ca/test-rootca.crt -CAkey /opt/security/pki/ca/test-rootca.key -CAcreateserial -out /opt/security/pki/test.example.co.kr.crt -extfile /opt/security/pki/ca/openssl_host.cnf;done

#공개키를 대체 시스템 truststore(jssecacerts)에 import
$JAVA_HOME/bin/keytool -importcert -alias test-rootca -keystore $JAVA_HOME/jre/lib/security/jssecacerts -file /opt/security/pki/ca/test-rootca.crt
```

password : changeit (기본 설정값)

Yes

#비밀번호 변경
$JAVA_HOME/bin/keytool -storepasswd -keystore $JAVA_HOME/jre/lib/security/jssecacerts
changeit
설정할 password 입력

#jssecacerts 배포
pscp -h /root/allnodes $JAVA_HOME/jre/lib/security/jssecacerts $JAVA_HOME/jre/lib/security/jssecacerts

#RootCA를 server cert에 추가, truststore에 저장

# >> 명령을 통해서 test-rootca.crt의 내용을 test.example.co.kr.crt 파일에 추가 하는 것.

```bash
cat /opt/security/pki/ca/test-rootca.crt >> /opt/security/pki/test.example.co.kr.crt
```

#변경한 crt를 기반으로 jks파일 업데이트(importcert)

```bash
$JAVA_HOME/bin/keytool -importcert -alias test.example.co.kr -file /opt/security/pki/test.example.co.kr.crt -keystore /opt/security/pki/test.example.co.kr.jks
```

  <aside>
  💡 #링크파일 작성
  인증서 심볼릭 링크
  이렇게하면 각 에이전트에 대한 파일을 유지 관리하지 않고 모든 에이전트 호스트에서 동일한 /etc/cloudera-scm-agent/config.ini 파일을 사용할 수 있습니다.

  ln -s /opt/security/pki/asterisk.example.co.kr.crt /opt/security/pki/agent.pem

  #RootCA 작업한 곳에서 server.jks 만들어서 배포
  ln -s /opt/security/pki/asterisk.example.co.kr.jks /opt/security/pki/server.jks

  </aside>

```bash
$JAVA_HOME/bin/keytool -importcert -alias *.example.co.kr -file /opt/security/pki/asterisk.example.co.kr.crt -keystore $JAVA_HOME/jre/lib/security/jssecacerts
```

```bash
openssl x509 -inform PEM -in /opt/security/pki/test.example.co.kr.crt > /opt/security/pki/serverpublic.pem
openssl rsa -in /opt/security/pki/test.example.co.kr.key -text > /opt/security/pki/serverprivate.pem
```

- RootCA에 대한 public.pem 파일 생성 (RootCA를 생성한 호스트에서 작업 진행)
openssl x509 -inform PEM -in /opt/security/pki/ca/test-rootca.crt > /opt/security/pki/ca/rootpublic.pem

#truststore에 RootCA가 포함되었는지 확인

- keytool 은 외부에서 생성된 private key 를 keystore 에 import 하는 방법을 제공하지 않는다. 한 가지 방법은 JDK 6 이상부터 PKCS#12 으로 된 인증서와 개인키를 keystore 에 import 하는게 가능하므로 openssl 로 pkcs#12를 만들고 pkcs#12 를 KeyStore 로 임포트하면 된다.

```bash
keytool -list -keystore $JAVA_HOME/jre/lib/security/jssecacerts >> jssecacerts.txt
```




https://nuritech.tistory.com/25