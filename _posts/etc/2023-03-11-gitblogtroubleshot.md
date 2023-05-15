---
layout: post
title: "[GitBlog] github-pages build with Jekyll failed (Liquid Exception: Liquid syntax error)" #게시물 이름
tags: [gitblog, pages build, trouble shoot, ] #태그 설정
categories: BLOG #카테고리 설정
author: # 작성자
  - Byungineer
#toc : true #Table of Contents
---

블로그에 글을 포스팅하다 보면, commit을 했는데도 불구하고 포스팅이 정상적으로 되지 않는 일이 있거나, 업로드 반영이 늦게 되는 경우가 있었다.   
최근에는 포스팅한 글이 업로드가 되지않는 Liquid syntax error를 Trouble shooting 하면서 Github Blog & Jekyll 에 대해 공부를 하자고 생각했다.   

포스팅하다 마주친 에러...
```
Error: YAML Exception reading /github/workspace/_posts/python/2022-11-28-python-sql.md: (<unknown>): did not find expected node content while parsing a flow node at line 4 column 52

Liquid Exception: Liquid syntax error (line 99): Variable '{% raw %} {{a1}' was not properly terminated with regexp: /\}\}/ in /github/workspace/_posts/python/2023-02-15-pythonalgorithm.md

github-pages 228 | Error:  Liquid syntax error (line 99): Variable '{{a1}' was not properly terminated with regexp: /\}\}/{% endraw %}
```
관련 에러를 trouble shootting한 내역을 다음 포스팅에 다뤄 보겠다.


static website generator

static website

github page

html css javascrpits 

https://han-joon-hyeok.github.io/posts/jekyll-liquid-syntax-error-curly-braces/

