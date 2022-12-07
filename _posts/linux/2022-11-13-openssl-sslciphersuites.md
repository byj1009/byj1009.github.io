


```
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




  791  openssl s_client -connect shtest03.goodmit.co.kr:8888
  792  openssl s_client -connect https://shtest03.goodmit.co.kr:8888 -cipher DES3
  793  openssl s_client -connect https://shtest03.goodmit.co.kr:8888
  794  openssl s_client -connect shtest03.goodmit.co.kr:8888
  795  openssl s_client -connect shtest03.goodmit.co.kr:8888 -cipher DES-CBC3-SHA
  796  openssl s_client -connect shtest03.goodmit.co.kr:8888 -cipher aes256
  797  openssl s_client -connect shtest03.goodmit.co.kr:8888 -cipher AES256
  798  openssl s_client -connect shtest03.goodmit.co.kr:8888 -cipher DES3
  799  openssl s_client -connect shtest03.goodmit.co.kr:8888 -cipher 3DES
  800  openssl s_client -connect shtest03.goodmit.co.kr:8888 -showcerts
  801  openssl s_client -connect shtest03.goodmit.co.kr:8888 -cipher DES-CBC3-SHA
  802  openssl s_client -connect shtest03.goodmit.co.kr:8888 -cipher AES256
  803  openssl s_client -connect shtest03.goodmit.co.kr:8888 -cipher DES-CBC3-SHA
  804  openssl s_client -connect shtest03.goodmit.co.kr:8888 -cipher des-ede3-cbc
  805  openssl s_client -connect 10.200.101.176:8888 -cipher des-ede3-cbc
  806  openssl s_client -connect shtest03.goodmit.co.kr:8888 -cipher AES256
  807  openssl s_client -connect shtest03.goodmit.co.kr:8888 -cipher AES256 -brief
