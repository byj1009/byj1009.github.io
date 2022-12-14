---
layout: post
title: "SSLCipherSuites" #게시물 이름
tags: [Self Signed TLS, TLS, SSL, Certificate, ciphersuites, sslciphersuites] #태그 설정
categories: Study #카테고리 설정
author: # 작성자
  - Byungineer
#toc : true #Table of Contents
---

# SSLCipherSuites이란?

TLS 통신의 원리를 들여다 보면 "TLS Handshake"를 통해서 클라이언트와 서버가 통신하기 위한 협의를 하게 된다.
이때, 암호화된 통신에는 어떤 프로토콜을 사용해야 할지, 어떻게 통신을 할지에 대한 정보를 주고받게 되는데, 그 과정에서 Cipher Suites또한 주고받게 된다.

<img src="/image/sslciphersuites.png" alt="bash shell script" style="height: 339px; width:881px;"/>



openssl 명령어를 통해 대상 서버의 sslciphersuites 허용 테스트를 할 수 있다.
```bash
openssl s_client -connect 10.200.101.176:8888 -cipher des-ede3-cbc
openssl s_client -connect 10.200.101.176:8888 -cipher des-ede3-cbc
openssl s_client -connect 10.200.101.176:8888 -cipher des-ede3-cbc
openssl s_client -connect shtest03.goodmit.co.kr:8888 -cipher AES256
openssl s_client -connect shtest03.goodmit.co.kr:8888 -cipher AES256 -brief
```

```bash
#!/bin/bash
SERVER=$1
DELAY=1
ciphers=$(openssl ciphers 'ALL:eNULL' | sed -e 's/:/ /g')

echo Enum cipher list from $(openssl version).
echo "========================"

for cipher in ${ciphers[@]}
do
result=$(echo -n | openssl s_client -cipher "$cipher" -connect $SERVER 2>&1)
if [[ "$result" =~ ":error:" ]] ; then
    a=1
else
  if [[ "$result" =~ "Cipher is ${cipher}" || "$result" =~ "Cipher    :" ]] ; then
    echo ${cipher}
  fi
fi
sleep $DELAY
done
```


---
### reference

[https://aws-hyoh.tistory.com/](aws-hyoh.tistory)
[aws-hyoh.tistory]: https://aws-hyoh.tistory.com/entry/HTTPS-%ED%86%B5%EC%8B%A0%EA%B3%BC%EC%A0%95-%EC%89%BD%EA%B2%8C-%EC%9D%B4%ED%95%B4%ED%95%98%EA%B8%B0-3SSL-Handshake