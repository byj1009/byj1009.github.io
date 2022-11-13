---
layout: post
title: "Self Signed TLS" #게시물 이름
tags: [Self Signed TLS, TLS, SSL, Certificate, 인증서, Certificate Authority, CA, 인증기관] #태그 설정
categories: Study #카테고리 설정
author: # 작성자
  - Byungineer
#toc : true #Table of Contents
---

# Self signed SSL

인증서(digital certificate)는 개인키 소유자의 공개키(public key)에 인증기관의 개인키로 전자서명한 데이터다.
모든 인증서는 발급기관(CA) 이 있어야 하나 최상위에 있는 인증기관(root ca)은 서명해줄 상위 인증기관이 없으므로 root ca의 개인키로 스스로의 인증서에 서명하여 최상위 인증기관 인증서를 만든다. 이렇게 스스로 서명한 ROOT CA 인증서를 Self Signed Certificate 라고 부른다.
IE, FireFox, Chrome 등의 Web Browser 제작사는 VeriSign이나 comodo 같은 유명 ROOT CA 들의 인증서를 신뢰하는 CA로 미리 등록해 놓으므로 저런 기관에서 발급된 SSL 인증서를 사용해야 browser 에서는 해당 SSL 인증서를 신뢰할수 있는데 OpenSSL 로 만든 ROOT CA와 SSL 인증서는 Browser가 모르는 기관이 발급한 인증서이므로 보안 경고를 발생시킬 것이나 테스트 사용에는 지장이 없다.
ROOT CA 인증서를 Browser에 추가하여 보안 경고를 발생시키지 않으려면 Browser 에 SSL 인증서 발급기관 추가하기를 참고하자.

성능향상을 위해서는 KDC와 LDAP을 같은 노드에 셋업하는게 유리하다.

- SSL 인증서 종류
1. [.pem]
PEM (Privacy Enhanced Mail)은 Base64 인코딩된 ASCII 텍스트 이다. 파일 구분 확장자로 .pem 을 주로 사용한다. 노트패드에서 열기/수정도 가능하다. 개인키, 서버인증서, 루트인증서, 체인인증서 및 SSL 발급 요청시 생성하는 CSR 등에 사용되는 포맷이며, 가장 광범위하고 거의 99% 대부분의 시스템에 호환되는 산업 표준 포맷이다. (대부분 텍스트 파일)
2. [.crt]
거의 대부분 PEM 포맷이며, 주로 유닉스/리눅스 기반 시스템에서 인증서 파일임을 구분하기 위해서 사용되는 확장자 이다. 다른 확장자로 .cer 도 사용된다. 파일을 노트패드 등으로 바로 열어 보면 PEM 포맷인지 바이너리 포맷인지 알수 있지만 99% 는 Base64 PEM 포맷이라고 봐도 무방하다. (대부분 텍스트 파일)
3. [.cer]
거의 대부분 PEM 포맷이며, 주로 Windows 기반에서 인증서 파일임을 구분하기 위해서 사용되는 확장자 이다. crt 확장자와 거의 동일한 의미이며, cer 이나 crt 확장자 모두 윈도우에서는 기본 인식되는 확장자이다. 저장할때 어떤 포맷으로 했는지에 따라 다르며, 이름 붙이기 나름이다.
4. [.csr]
Certificate Signing Request 의 약자이며 거의 대부분 PEM 포맷이다. SSL 발급 신청을 위해서 본 파일 내용을 인증기관 CA 에 제출하는 요청서 파일임을 구분하기 위해서 붙이는 확장자 이다. (대부분 텍스트 파일)
5. [.der]
Distinguished Encoding Representation (DER) 의 약자이며, 바이너리 포맷이다. 노트패드등으로 열어 봐서는 알아 볼수 없다. 바이너리 인코딩 포맷을 읽을수 있는 인증서 라이브러리를 통해서만 내용 확인이 가능하다. 사설 또는 금융등 특수 분야 및 아주 오래된 구형 시스템을 제외하고는, 최근 웹서버 SSL 작동 시스템 에서는 흔히 사용되는 포맷은 아니다. (바이너리 이진 파일)
6. [.pfx / .p12]
PKCS#12 바이너리 포맷이며, Personal Information Exchange Format 를 의미한다. 주로 Windows IIS 기반에서 인증서 적용/이동시 활용된다. 주요 장점으로는 개인키,서버인증서,루트인증서,체인인증서를 모두 담을수 있어서 SSL 인증서 적용이나 또는 이전시 상당히 유용하고 편리하다. Tomcat 등 요즘에는 pfx 설정을 지원하는 서버가 많아지고 있다. (바이너리 이진 파일)
7. [.key]
주로 openssl 및 java 에서 개인키 파일임을 구분하기 위해서 사용되는 확장자이다. PEM 포맷일수도 있고 DER 바이너리 포맷일수도 있으며, 파일을 열어봐야 어떤 포맷인지 알수가 있다. 저장할때 어떤 포맷으로 했는지에 따라 다르며, 확장자는 이름 붙이기 나름이다.
8. [.jks]
Java Key Store의 약자이며, Java 기반의 독자 인증서 바이너리 포맷이다. pfx 와 마찬가지로 개인키, 서버인증서, 루트인증서, 체인인증서를 모두 담을 수 있어서 SSL 인증서 파일 관리 시 유용하다. Tomcat에서 SSL 적용시 가장 많이 사용되는 포맷이다. (바이너리 이진 파일)

## 1. Pre-config

Configure environment to set JAVA_HOME to the Oracle JDK (ALL host)

```bash
vi .bashrc
export JAVA_HOME=/usr/java/jdk1.8.0_232-cloudera
export PATH=$JAVA_HOME/bin:$PATH
pscp -h /root/allnodes /root/.bashrc /root/.bashrc
pssh -h /root/allnodes source .bashrc

#Directory 생성 ( Rootca Directory )
mkdir -p /opt/cloudera/security/pki/ca
pssh -h /root/nodes mkdir -p /opt/cloudera/security/pki/
```

```bash
#CRT(인증서)생성에 필요한 configuration 파일 생성
vi /opt/cloudera/security/pki/ca/rootca.cnf

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
organizationName = Organization Name (eg, company)
organizationName_default = GIT Inc.
# 부서 입력
#organizationalUnitName = Organizational Unit Name (eg, section)
#organizationalUnitName_default = Condor Project
# SSL 서비스할 domain 명 입력
commonName = Common Name (eg, your name or your server's hostname)
commonName_default = GIT's Self Signed CA
commonName_max = 64
```

```bash
vi /opt/cloudera/security/pki/ca/openssl_host.cnf

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
commonName = Common Name
emailAddress = Email Address
countryName_default = KR
stateOrProvinceName_default = Seoul
localityName_default = Mapo-Gu
0.organizationName_default = GIT
organizationalUnitName_default = Biadata Team
emailAddress_default = [yjbyun@goodmit.co.kr](mailto:yjbyun@goodmit.co.kr)

[ v3_ca ]
subjectKeyIdentifier = hash
authorityKeyIdentifier = keyid:always,issuer
basicConstraints = critical, CA:true
keyUsage = critical, digitalSignature, cRLSign, keyCertSign

[ server_cert ]
basicConstraints = CA:FALSE
nsComment = "OpenSSL Generated Server Certificate"
subjectKeyIdentifier = hash
authorityKeyIdentifier = keyid,issuer
keyUsage = nonRepudiation, digitalSignature, keyEncipherment
extendedKeyUsage = serverAuth, clientAuth
subjectAltName = @alt_names

[ alt_names ]
DNS.1 = goodmit.co.kr
DNS.2 = *.goodmit.co.kr
DNS.3 = cdsw01.[goodmit.co](http://goodmit.com/).kr
DNS.4 = *.cdsw01.[goodmit.co](http://goodmit.com/).kr
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
    
    ### 1. git-rootca.jks 생성
    
    <aside>
    💡 SAN certificates
    Subject Alternative Name은 하나의 인증서로 여러개의 도메인을 등록하기 위해서 사용한다. 최대 100개의 도메인을 커버 할 수 있으며 그 사용의 예는 다음과 같다.
    SAN 1: DNS Name=example.com
    
    SAN 2: DNS Name=www.example.com
    
    SAN 3: DNS Name=example.net
    
    SAN 4: DNS Name=mail.example.com
    
    SAN 5: DNS Name=support.example.com
    
    SAN 6: DNS Name=example2.com
    
    SAN 7: IP Address=93.184.216.34\
    
    SAN 8: IP Address= 2606:2800:220:1:248:1893:25c8:1946
    
    </aside>
    
    [test](https://www.notion.so/test-117ee6ca4f7c4c12a053fc37a810c36f)
    

```bash
$JAVA_HOME/bin/keytool -genkeypair -alias git-rootca -keyalg RSA -keystore /opt/cloudera/security/pki/ca/git-rootca.jks -keysize 2048 -dname "CN=git-rootca,OU=Bigdata_Team,O=GIT,L=MapoGu,ST=Seoul,C=KR
$JAVA_HOME/bin/keytool -genkeypair -alias git-rootca -keyalg RSA -keystore /opt/cloudera/security/pki/ca/git-rootca.jks -keysize 2048 -dname "CN=git-rootca,OU=Bigdata_Team,O=GIT,L=MapoGu,ST=Seoul,C=KR" -ext san=dns:yjbyun01.goodmit.com
```

### 2. git-rootca.csr 생성

```bash
$JAVA_HOME/bin/keytool -certreq -alias git-rootca -keystore /opt/cloudera/security/pki/ca/git-rootca.jks -file /opt/cloudera/security/pki/ca/git-rootca.csr -ext san=dns:yjbyun01.goodmit.com -ext EKU=serverAuth,clientAuth
```

### 3. Jks로 pkcs #12 파일 생성

```bash
$JAVA_HOME/bin/keytool -importkeystore -srckeystore /opt/cloudera/security/pki/ca/git-rootca.jks -destkeystore /opt/cloudera/security/pki/ca/git-rootca.p12 -deststoretype PKCS12 -srcalias git-rootca
```

### 4. pkcs #12를 openssl로 key파일 생성(PEM형식)

```bash
openssl pkcs12 -in /opt/cloudera/security/pki/ca/git-rootca.p12 -nocerts -out /opt/cloudera/security/pki/ca/git-rootca.key
openssl pkcs12 -in /opt/cloudera/security/pki/ca/git-rootca.p12 -nocerts -out /opt/cloudera/security/pki/ca/git-rootca.key.pem
```

### 5. crt 인증서 생성

```bash
openssl x509 -req -days 3650 -extensions v3_ca -set_serial 1 -sha256 -in /opt/cloudera/security/pki/ca/git-rootca.csr -signkey /opt/cloudera/security/pki/ca/git-rootca.key -out /opt/cloudera/security/pki/ca/git-rootca.crt -extfile /opt/cloudera/security/pki/ca/openssl_rootca.cnf
openssl x509 -req -days 3650 -extensions v3_ca -set_serial 1 -sha256 -in /opt/cloudera/security/pki/ca/git-rootca.csr -signkey /opt/cloudera/security/pki/ca/git-rootca.key -out /opt/cloudera/security/pki/ca/git-rootca.crt.pem -extfile /opt/cloudera/security/pki/ca/openssl_rootca.cnf
```

# 외부 접근 및 수정을 방지를 위한 권한 변경

```bash
chmod 600 /opt/cloudera/security/pki/ca/git-rootca.*
```

## 3.	Host 인증서 생성

1. CSR생성

```bash
$JAVA_HOME/bin/keytool -certreq -alias *[.goodmit.com](http://yjbyun0%24i.goodmit.com/) -keystore /opt/cloudera/security/pki/asterisk.goodmit.com.jks -file /opt/cloudera/security/pki/asterisk.goodmit.com.csr; done
```

1. jks >> pkcs 12

```bash
$JAVA_HOME/bin/keytool -importkeystore -srckeystore /opt/cloudera/security/pki/yjbyun0$i.goodmit.com.jks -destkeystore /opt/cloudera/security/pki/yjbyun0$i.goodmit.com.p12 -deststoretype PKCS12 -srcalias [yjbyun0$i.goodmit.com](http://yjbyun0%24i.goodmit.com/); done

```

1. pkcs 12 >>key

```bash
openssl pkcs12 -in /opt/cloudera/security/pki/yjbyun0$i.goodmit.com.p12 -nocerts -out /opt/cloudera/security/pki/yjbyun0$i.goodmit.com.key; done
```

## 4. getting CA Private key

```bash
openssl x509 -req -sha256 -days 365 -extensions server_cert -in /opt/cloudera/security/pki/yjbyun0$i.goodmit.com.csr -CA /opt/cloudera/security/pki/ca/git-rootca.crt -CAkey /opt/cloudera/security/pki/ca/git-rootca.key -CAcreateserial -out /opt/cloudera/security/pki/yjbyun0$i.goodmit.com.crt -extfile /opt/cloudera/security/pki/ca/openssl_host.cnf;done
#공개키를 대체 시스템 truststore(jssecacerts)에 import
$JAVA_HOME/bin/keytool -importcert -alias git-rootca -keystore $JAVA_HOME/jre/lib/security/jssecacerts -file /opt/cloudera/security/pki/ca/git-rootca.crt
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

# >> 명령을 통해서 git-rootca.crt의 내용을 yjbyun0$i.goodmit.com.crt 파일에 추가 하는 것.

```bash
cat /opt/cloudera/security/pki/ca/git-rootca.crt >> /opt/cloudera/security/pki/yjbyun0$i.goodmit.com.crt
```

#변경한 crt를 기반으로 jks파일 업데이트(importcert)

```bash
$JAVA_HOME/bin/keytool -importcert -alias [yjbyun0$i.goodmit.com](http://yjbyun0%24i.goodmit.com/) -file /opt/cloudera/security/pki/yjbyun0$i.goodmit.com.crt -keystore /opt/cloudera/security/pki/yjbyun0$i.goodmit.com.jks
```

<aside>
💡 #링크파일 작성
인증서 심볼릭 링크
이렇게하면 각 에이전트에 대한 파일을 유지 관리하지 않고 모든 에이전트 호스트에서 동일한 /etc/cloudera-scm-agent/config.ini 파일을 사용할 수 있습니다.

ln -s /opt/cloudera/security/pki/asterisk.goodmit.com.crt /opt/cloudera/security/pki/agent.pem

#RootCA 작업한 곳에서 server.jks 만들어서 배포
ln -s /opt/cloudera/security/pki/asterisk.goodmit.com.jks /opt/cloudera/security/pki/server.jks

</aside>

```bash
$JAVA_HOME/bin/keytool -importcert -alias *[.goodmit.com](http://yjbyun0%24i.goodmit.com/) -file /opt/cloudera/security/pki/asterisk.goodmit.com.crt -keystore $JAVA_HOME/jre/lib/security/jssecacerts
```

for i in 1 2 3; do ssh root@10.200.101.17$i "ln -s /opt/cloudera/security/pki/yjbyun0$i.goodmit.com.key /opt/cloudera/security/pki/agent.key"; done 

CM에서 Configuration을 하기 위해서는 pem 형식의 파일이 필요. 따라서 Server에 대한 serverpublic.pem 파일과 serverprivate.pem파일, RootCA에 대한 rootpublic.pem파일을 생성해주어야 합니다.

#각각의 Server에 대한 public.pem 파일과 private.pem파일 생성

```bash
openssl x509 -inform PEM -in /opt/cloudera/security/pki/yjbyun0$i.goodmit.com.crt > /opt/cloudera/security/pki/serverpublic.pem
openssl rsa -in /opt/cloudera/security/pki/yjbyun0$i.goodmit.com.key -text > /opt/cloudera/security/pki/serverprivate.pem
```

- RootCA에 대한 public.pem 파일 생성 (RootCA를 생성한 호스트에서 작업 진행)
openssl x509 -inform PEM -in /opt/cloudera/security/pki/ca/git-rootca.crt > /opt/cloudera/security/pki/ca/rootpublic.pem

#truststore에 RootCA가 포함되었는지 확인

- keytool 은 외부에서 생성된 private key 를 keystore 에 import 하는 방법을 제공하지 않는다. 한 가지 방법은 JDK 6 이상부터 PKCS#12 으로 된 인증서와 개인키를 keystore 에 import 하는게 가능하므로 openssl 로 pkcs#12를 만들고 pkcs#12 를 KeyStore 로 임포트하면 된다.

```bash
keytool -list -keystore $JAVA_HOME/jre/lib/security/jssecacerts >> jssecacerts.txt
```