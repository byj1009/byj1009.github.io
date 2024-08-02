---
layout: post
title: "[Python] 2의 보수 활용하기" #게시물 이름
tags: [python, complemention, 보수, binary] #태그 설정
categories: python #카테고리 설정
author: # 작성자
  - Byungineer
#toc : true #Table of Contents
---

'''
https://en.wikipedia.org/wiki/Two%27s_complement

hex_n = (n + (1 << 2**(nbit+1))) % (1 << 2**(nbit+1))


n >> x     =     n * 2**x
1 >> 2     =     1 * 2**2
1 -> 100   =       4



n = 1
nbit = 4
hex_n = (n + (1 << 2**(nbit+1))) % (1 << 2**(nbit+1))

hex_n = (1 + (1 << 2**(5))) % (1 << 2**(5))
hex_n = (1 + (1 << 32)) % (1 << 32)
hex_n = (1 + 1/0000/0000/0000/0000/0000/0000/0000/0000) % (1/0000/0000/0000/0000/0000/0000/0000/0000)
hex_n = (1/0000/0000/0000/0000/0000/0000/0000/0001) % (1/0000/0000/0000/0000/0000/0000/0000/0000)
